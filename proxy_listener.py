import serial, time
import socket
from Crypto.Cipher import AES
from pymavlink import mavutil


key = bytes(input("Input Encryption Key(16 characters): ").encode())
cipher = AES.new(key, AES.MODE_EAX)

# Telemetry Radio serial connection
ser = serial.Serial(port="/dev/tty.usbserial-DK0G5G11", baudrate=57600, timeout=3)

# MavProxy egress connection
UDP_IP = "127.0.0.1"
UDP_PORT = 8080

mav_conn = mavutil.mavlink_connection('udpout:localhost:8080', source_system=1)

mav_conn.mav.heartbeat_send(mavutil.mavlink.MAV_TYPE_GCS, mavutil.mavlink.MAV_AUTOPILOT_INVALID, 0, 0, 0)
while 1:

    time.sleep(2)
    preamble = ser.read_until(b'XXX')      
    nonce = ser.read(16)
    tag = ser.read(16)
    ciphertext = ser.read_until(b'\r\n')[:-2]

    try:
        cipher = AES.new(key, AES.MODE_EAX, nonce)
        data = cipher.decrypt_and_verify(ciphertext, tag)
        print(data)
        mav_conn.mav.statustext_send(mavutil.mavlink.MAV_SEVERITY_NOTICE,data)
        
        
    except ValueError:
        print(nonce, tag, ciphertext)
        continue
