import cv2


class Webcam:
    def __init__(self, cam_id=0):
        self.cap = cv2.VideoCapture(cam_id)
        self.last_frame = 0

    def releaseCamera(self):
        self.cap.release()

    def getFrame(self):
        ret, frame = self.cap.read()
        self.last_frame = frame

        return ret, frame

    def setResolution(self, width=640, height=480):
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    def checkIsOpened(self):
        return self.cap.isOpened()

