import fcntl
import os.path, sys
from ugrsshapesdetection.yolodetection import yolo
import ugrsshapesdetection.definitions as definitions

# sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
# os.chdir("/home/valentin/FAKS/UGRS_projekt/alexeyAB_darknet/darknet")  # change to where darknet is
os.chdir(definitions.ROOT_DIR)  # change to where darknet is

from subprocess import Popen, PIPE
import select
# import cv2
import time
import json

yolo.detect("{0}/darknet detector test {1}/obj.data {1}/yolov3-obj.cfg {1}/yolov3-obj_best.weights -ext_output -dont_show -out result.json < {1}/frames.txt ".format(definitions.DARKNET_PATH, 'data/yolo_config_files'))

# data = yolodetection.yolo.readJSONDetections(path="/result.json")
# print(json.dumps(data, indent=4, sort_keys=True))
# object_info = yolodetection.yolo.readJSONObjects(data[0])
#
# x_center, y_center, width, height = yolodetection.yolo.readBBoxCoordinates(object_info[2])
# top_left_corner = (int(x_center - width / 2), int(y_center - height / 2))
# bottom_right_corner = (int(x_center + width / 2), int(y_center + height / 2))
#
# #
# # im = cv2.imread("frame0.jpg")
# # im = cv2.rectangle(img=im, pt1=top_left_corner, pt2=bottom_right_corner, color=(255, 0, 0))

