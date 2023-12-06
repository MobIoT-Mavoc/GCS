from Crypto.Cipher import AES
from pymavlink import mavutil
import serial, time
import pickle

# Connection from the mavproxy
mav_conn = mavutil.mavlink_connection('udpin:127.0.0.1:14550')

# Connection to the telemetry radio
ser = serial.Serial(
    port="/dev/tty.usbserial-D20118EB",
    baudrate=57600,
    bytesize=serial.EIGHTBITS,
)

# Wait for heartbeat message
mav_conn.wait_heartbeat()

# Send to 

print("Heartbeat from system (system %u component %u)" % (mav_conn.target_system, mav_conn.target_component))

key = b'3czZUsh9ftUqCGcu'

while 1:
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce
    
    
    msg = mav_conn.recv_match(blocking=True)
    
    # Take the pymavlink object into byte array
    msg_bytes = pickle.dumps(msg)
    
    ciphertext, tag = cipher.encrypt_and_digest(msg_bytes)
    

    ser.write(b'XXX')
    time.sleep(0.5)
    ser.write(nonce)
    ser.write(tag)
    ser.write(ciphertext + b'\r\n')
    time.sleep(0.5)

    
    cipher_new = AES.new(key, AES.MODE_EAX, nonce)
    decrypted_bytes = cipher_new.decrypt(ciphertext)
    data = pickle.loads(decrypted_bytes)
    print(type(data))


