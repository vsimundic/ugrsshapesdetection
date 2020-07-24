import cv2


def initializeCamera(id=0):
    return cv2.VideoCapture(id)


def releaseCamera(cap):
    cap.release()
