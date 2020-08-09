import cv2
import os
import sys

width = 640
height = 480

class Webcam:
    def __init__(self, cam_id=0):
        self.cap = cv2.VideoCapture(cam_id)
        self.last_frame = 0

    def releaseCamera(self):
        self.cap.release()

    def getFrame(self):
        ret, frame = self.cap.read()
        
        # frame = frame[30:height-40, 60:width-35,:]
        # try:
        #     frame = frame[0:height, 58:width-58,:]
        #
        # except Exception as e:
        #     return False, None
        
        self.last_frame = frame

        return ret, self.last_frame

    def saveFrame(self, grayscale=False, path="frame.jpg"):
        if grayscale:
            gray = cv2.cvtColor(self.last_frame, cv2.COLOR_BGR2GRAY)
            cv2.imwrite(path, gray)
        else:
            cv2.imwrite(path, self.last_frame)

    def setResolution(self, width=640, height=480):
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    def checkIsOpened(self):
        return self.cap.isOpened()


def findCamID(taken_id=-5):
    i = -1
    while True:
        i += 1
        try:
            cap = Webcam(i)
            ret, frame = cap.getFrame()
            
            if ret and frame is not None:
                if i != taken_id:
                    cap.releaseCamera()
                    findCamID.x = i
                    return i
            
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("Error location: ", exc_type, fname, exc_tb.tb_lineno)
            print("Error description: ", e)
            
            cap.releaseCamera()
            continue
