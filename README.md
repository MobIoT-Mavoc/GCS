# GCS
Ground Control Station functionalities


## Drone Console

```
python3 sim_vehicle.py -v ArduCopter -N -m "--out=/dev/ttyUSB0"
```

## GCS 
```
mavproxy.py --master=/dev/tty.usbserialxxx --out=127.0.0.1:14550
```
### Then capture packets using Wireshark on the loopback interface, and start ArmPlanner2 
