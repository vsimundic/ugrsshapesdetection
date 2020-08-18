import cv2
import os
import sys
import ugrsshapesdetection.definitions as definitions
import numpy as np

width = 640
height = 480
fill_color = [0, 0, 0]
mask_value = 255

class Webcam:
    def __init__(self, cam_id=0):
        self.cap = cv2.VideoCapture(cam_id)
        self.last_frame = 0

    def releaseCamera(self):
        self.cap.release()

    def getFrame(self, contour=None):
        if contour is None:
            contour = [[0, 0]]

        ret, frame = self.cap.read()
        
        self.last_frame = frame
        if definitions.flag_create_contour:
            stencil = np.zeros(self.last_frame.shape[:-1]).astype(np.uint8)
            cv2.fillPoly(stencil, [np.array(contour, dtype=np.int32)], mask_value)
            sel = stencil != mask_value
            self.last_frame[sel] = fill_color

        return ret, self.last_frame.copy()

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


def findCamID(taken_ids):
    i = -1
    while True:
        i += 1
        try:
            cap = Webcam(i)
            ret, frame = cap.getFrame()

            if definitions.EMBEDDED_CAM:
                if ret and frame is not None:
                    if i not in taken_ids and i != 0:
                        cap.releaseCamera()
                        return i
            else:
                if ret and frame is not None:
                    if i not in taken_ids:
                        cap.releaseCamera()
                        return i

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("Error location: ", exc_type, fname, exc_tb.tb_lineno)
            print("Error description: ", e)
            
            cap.releaseCamera()
            continue
