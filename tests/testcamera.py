from camera.webcam import Webcam
import cv2

cam1 = Webcam(1)

while True:
    ret, frame = cam1.getFrame()
    cv2.imshow("Some name", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.cvtColor(frame, cv2.COLOR_Y)
        print(frame)
        break


cam1.releaseCamera()
