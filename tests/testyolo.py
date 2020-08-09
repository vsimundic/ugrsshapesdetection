import fcntl
import os.path, sys
import yolodetection.yolo

# sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
# os.chdir("/home/valentin/FAKS/UGRS_projekt/alexeyAB_darknet/darknet")  # change to where darknet is
os.chdir("/home/valentin/darknet2/darknet")  # change to where darknet is

from subprocess import Popen, PIPE
import select
# import cv2
import time
import json

data = yolodetection.yolo.readJSONDetections(path="/result.json")
print(json.dumps(data, indent=4, sort_keys=True))
object_info = yolodetection.yolo.readJSONObjects(data[0])

x_center, y_center, width, height = yolodetection.yolo.readBBoxCoordinates(object_info[2])
top_left_corner = (int(x_center - width / 2), int(y_center - height / 2))
bottom_right_corner = (int(x_center + width / 2), int(y_center + height / 2))

#
# im = cv2.imread("frame0.jpg")
# im = cv2.rectangle(img=im, pt1=top_left_corner, pt2=bottom_right_corner, color=(255, 0, 0))

