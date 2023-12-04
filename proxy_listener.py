import serial, time
from Crypto.Cipher import AES

key = b"0123456789abcdef"
cipher = AES.new(key, AES.MODE_EAX)

ser = serial.Serial(port="/dev/tty.usbserial-DK0G5G11", baudrate=57600, timeout=3)

while 1:
    print("SETUP")
    time.sleep(2)
    
    preamble = ser.read_until(b'\xff')
    
    nonce = ser.readline(16)
    tag = ser.readline(16)
    ciphertext = ser.read_until(b'\x00')[:-1]

    try:
        cipher = AES.new(key, AES.MODE_EAX, nonce)
        data = cipher.decrypt_and_verify(ciphertext, tag)
        print(data)
    except ValueError:
        continue
