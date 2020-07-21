from camera.webcam import Webcam
import cv2

cam1 = Webcam(1)

for i in range(3):
    while True:
        ret, frame = cam1.getFrame()
        if frame is not None:
            cv2.imshow("Some name", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                cam1.saveFrame(grayscale=True,
                               path="/home/valentin/FAKS/UGRS_projekt/alexeyAB_darknet/darknet/frame{}.jpg".format(i))
                break


cam1.releaseCamera()
cv2.destroyAllWindows()