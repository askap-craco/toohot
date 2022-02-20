# toohot
Shutdown machine when IPMI sensor is toohot

# To install
pip install toohot (or whaever)

```
sudo  docs/toohot.service to /etc/systemd/system/
service start toohot
service status toohot
```

Log output looks like
```
journalctl -u toohot
Feb 21 10:46:50 athena toohot[14747]: INFO:root:Starting TOOHOT shutdown service
Feb 21 10:46:50 athena toohot[14747]: INFO:root:Checked 32 sensors. Inlet temp=18.0 Everything is OK
```

