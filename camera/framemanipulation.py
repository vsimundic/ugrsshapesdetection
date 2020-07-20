import cv2


def readFrame(cap):
    returnval, frame = cap.read()
    return returnval, frame


def displayFrame(frame, camera_number=0):
    cv2.imshow("frame camera {}".format(camera_number), frame)
    cv2.waitKey(0)


def saveFrame(frame, name="default.jpg"):
    cv2.imwrite(name, frame)

def closeAllWindows():
    cv2.destroyAllWindows()
