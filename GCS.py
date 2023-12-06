#!/usr/local/bin/python3.8

import serial, time
from Crypto.Cipher import AES
from pymavlink import mavutil
import socket
import threading
​
# UDP Configuration
udp_host = '127.0.0.1' 
udp_port_in = 12345  
udp_port_out = 54321 
​
# Serial Configuration
serial_port = '/dev/tty.usbserial-DK0G5G11'  
serial_baudrate = 57600 
​
# Function to read from UDP port A and write to serial port X
def udp_to_serial():
    conn = mavutil.mavlink_connection('udpin:127.0.0.1:14550')
    conn.wait_heartbeat()
    #ADD CODE FROM proxy_server
        
​
# Function to read from serial port X and write to UDP port B
def serial_to_udp():
    #ADD CODE FROM proxy_listener
​
# Create and start the threads
udp_to_serial_thread = threading.Thread(target=udp_to_serial)
serial_to_udp_thread = threading.Thread(target=serial_to_udp)
​
udp_to_serial_thread.start()
serial_to_udp_thread.start()
​
# Threads run indefinetly
udp_to_serial_thread.join()
serial_to_udp_thread.join()

