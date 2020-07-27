import serial
import time
# /dev/ttyACM0

ser = serial.Serial('/dev/ttyAMA0', 9600)

while True:
    from_stm = ser.readline()
    from_stm = from_stm.decode("utf-8")
    print(from_stm)
    
    if "start" in from_stm:
        print("saljem dalje")
        time.sleep(1)
        ser.write("next\r\n".encode('utf-8'))
    # time.sleep(1)

