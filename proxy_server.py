#!/usr/local/bin/python3.8

from Crypto.Cipher import AES
from pymavlink import mavutil
import serial, time


print("START SENDING")

ser = serial.Serial(
    port="/dev/tty.usbserial-D20118EB",
    baudrate=57600,
)

conn = mavutil.mavlink_connection('udpin:127.0.0.1:14550')
conn.wait_heartbeat()
print("Heartbeat from system (system %u component %u)" % (conn.target_system, conn.target_component))

key = bytes(input("Input Encryption Key(16 characters): ").encode())
cipher = AES.new(key, AES.MODE_EAX)

while 1:    
    time.sleep(0.125)
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce
    msg = str(conn.recv_match(blocking=True))

    ciphertext, tag = cipher.encrypt_and_digest(bytes(msg, 'utf-8'))
    #print(nonce, tag, ciphertext)    
    
    ser.write(b'XXX')
    ser.write(nonce)
    ser.write(tag)
    ser.write(ciphertext + b'\r\n')
    ser.flush()
    