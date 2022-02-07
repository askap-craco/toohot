#!/usr/bin/env python

from distutils.core import setup

setup(name='toohot',
      version='1.0',
      description='Script / service to shutdown if intake temperature is too hot',
      author='Keith Bannister',
      author_email='keith.bannister@csiro.au',
      url='',
      packages=['toohot'],
      package_data={'toohot':['system_files/*']},
      install_requires=['pandas'],
      entry_points={
          'console_scripts': [
              'toohot = toohot:_main',
              ],
          },
     )
