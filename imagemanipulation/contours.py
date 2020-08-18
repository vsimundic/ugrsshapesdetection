import sys
sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import cv2
from ..definitions import ROOT_DIR
from ..cameramanipulation import webcam
import pickle
import os

cam_ids = [1]
current_cam_id = 1
contour = []
name_dump = "variablescontour_cam0.pickle"


def mouseClick(event, x, y):
    if event == cv2.EVENT_LBUTTONUP:
        contour.append([x, y])


def findContour(cam_id, frame):
    print("What the hell")
    window_name = "Find contour on image{}".format(cam_id)
    cv2.namedWindow(window_name)
    print("Contourrrr")
    cv2.setMouseCallback(window_name, mouseClick)
    print("Contourrrr ne radi")
    while True:
        cv2.imshow(window_name, frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord(" "):
            break

    cv2.destroyAllWindows()


if __name__ == '__main__':
    for id in cam_ids:
        current_cam_id = id
        cam = webcam.Webcam(cam_id=id)
        ret, frame = cam.getFrame()
        findContour(id, frame)
        cam.releaseCamera()

        with open(os.path.join(ROOT_DIR, "data", "vars", name_dump), 'wb') as contours_file_:
            pickle.dump(contour, contours_file_)
