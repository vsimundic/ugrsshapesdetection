from ugrsshapesdetection.cameramanipulation.webcam import Webcam
import cv2

cam1 = Webcam(0)

while True:
    ret, frame = cam1.getFrame()
    if frame is not None:
        cv2.imshow("Some name", frame)
        # cv2.waitKey(1)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cam1.saveFrame(grayscale=True,
                path="/home/pi/UGRS_projekt/darknet_new/darknet-nnpack/frame0.jpg")
            # break


cam1.releaseCamera()
cv2.destroyAllWindows()
