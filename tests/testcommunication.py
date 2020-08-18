import serial
import time
# /dev/ttyACM0

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=0.1)

while True:
    # from_stm = ser.readline()
    # from_stm = from_stm.decode("ascii")
    # print(from_stm)
    #
    # if "start" in from_stm:
    print("saljem dalje")
    time.sleep(1)
    ser.write("next\r\n".encode('utf-8'))
    # time.sleep(1)

