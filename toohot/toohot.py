#!/usr/bin/env python
"""
Template for making scripts to run from the command line

Copyright (C) CSIRO 2020
"""
import numpy as np
import os
import sys
import logging
import subprocess
import time
import pandas as pd
from io import StringIO
import math

__author__ = "Keith Bannister <keith.bannister@csiro.au>"

sensor_cmd = 'ipmi-sensors -t temperature --comma-separated-output --output-sensor-thresholds'

do_shutdown=True

def get_sensors():
    logging.debug('Running %s', sensor_cmd)
    b = subprocess.check_output(sensor_cmd, shell=True)
    s = b.decode('utf-8')
    return s

def shutdown(msg=''):
    cmd = f'shutdown --poweroff now "{msg}"'
    if do_shutdown:
        logging.debug('Running %s', cmd)
        subprocess.check_output(cmd, shell=True)
    else:
        logging.debug('Not running %s', cmd)

def is_ok(s):
    if isinstance(s, str):
        s = s.replace("'",'') # Remove quotes
        return s == 'OK' or s == 'NaN'
    if isinstance(s, float):
        return math.isnan(s)

    return False

def check_sensors(ncheck):
    s = get_sensors()
    #print(s)
    df = pd.read_csv(StringIO(s))
    #arr = np.fromstring(StringIO(s))
    do_shutdown = False
    all_warnings = []
    inlet_temp = None
    for index, row in df.iterrows():
        logging.debug('index=%s row=%s', index, row)
        event = row['Event']
        name = row['Name']
        temp = row['Reading']
        if name.strip().lower() == 'Inlet Temp'.lower():
            inlet_temp = temp
            if float(temp) > 50.0:
                meas_ok = False
        else:
            meas_ok = True
            
        temp_isok = is_ok(event) and meas_ok
        s = 'TOOHOT: Sensor %s has reading %s %s event=%s. Event OK? %s meas_ok? %s temp_ok? %s' % (name, temp, row['Units'], row['Event'], is_ok(event), meas_ok, temp_isok)
        logging.debug('s=%s event=%s is_temp_ok? %s is meas_ok? %s', s, type(event), temp_isok, meas_ok)
        if not temp_isok:
            logging.critical(s)
            all_warnings.append(s)
            do_shutdown = True

    if do_shutdown:
        msg = '\n'.join(all_warnings)
        logging.debug('Aat least one sensor is too hot.  Shutting down')
        shutdown(msg)
    else:
        if ncheck == 0:
            logging.info('Checked %s sensors. Inlet temp=%s Everything is OK', len(df), inlet_temp)

            

def _main():
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(description='Script description', formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('-v', '--verbose', action='store_true', help='Be verbose')
    parser.set_defaults(verbose=False)
    values = parser.parse_args()
    if values.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)


    logging.info('Starting TOOHOT shutdown service')
    ncheck = 0
    while True:
        check_sensors(ncheck)
        time.sleep(60)
        ncheck += 1

        
    

if __name__ == '__main__':
    _main()
