import serial
import time

ser = serial.Serial('/dev/ttyUSB0', baudrate=9600)

# while True:
#     line = ser.readline().decode('utf-8')
#     print(line)



while True:
    ser.write('Napisi mi bor\n'.encode('ascii'))
    # time.sleep(1)
