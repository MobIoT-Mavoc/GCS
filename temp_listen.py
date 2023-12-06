from pymavlink import mavutil
import serial, time, io
from Crypto.Cipher import AES
import pickle
import threading

key = b'3czZUsh9ftUqCGcu'


# Connection from the telemetry radio
ser = serial.Serial(
    port="/dev/tty.usbserial-DK0G5G11", 
    baudrate=57600, timeout=3,
    bytesize=serial.EIGHTBITS,
)
sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))

# Connection to mavproxy
mav_conn = mavutil.mavlink_connection('udpout:localhost:8080', source_system=1)



def send_to_mavproxy():
    


def decrypt_mavlink(nonce, tag, ciphertext):
    cipher = AES.new(key, AES.MODE_EAX, nonce)
    decrypted_bytes = cipher.decrypt_and_verify(ciphertext, tag)
    data = pickle.loads(decrypted_bytes)
    
    print(type(data))

while 1:    
    preamble = ser.read_until(b'XXX')    
    time.sleep(0.5)  
    nonce = ser.read(16)
    tag = ser.read(16)
    ciphertext = ser.read_until(b'\r\n')[:-2]    
    time.sleep(0.5)
    
    try:
        thread1 = threading.Thread(target=decrypt_mavlink(nonce, tag, ciphertext))
        thread1.start()
        thread1.join()
    except ValueError:
        print(nonce, tag, ciphertext)
        continue

        
