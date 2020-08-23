import sys
from os import getcwd, uname
from ..definitions import *

if uname()[4][:3] == 'x86':
    try:
        sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
    except ValueError as e:
        print("Already not installed")

import cv2
from subprocess import Popen, PIPE
import json
import operator

classes_scores = {
    'Valjak': 0.0,
    'Piramida': 0.0,
    'Kocka': 0.0,
    'Kugla': 0.0,
    'Kvadar': 0.0,
    'Stozac': 0.0,
}


def reset_class_scores():
    for key in classes_scores:
        classes_scores[key] = 0.0


def add_to_class_score(key, value):
    classes_scores[key] += value


def get_most_confident_class():
    return max(classes_scores.items(), key=operator.itemgetter(1))[0]


def detect(cmdline_str_args="./darknet detector test obj.data yolov3-tiny-prn-obj.cfg "
                            "yolov3-tiny-prn-obj_best.weights -ext_output -dont_show -out result.json < frames.txt "):
    process = Popen(cmdline_str_args, stdout=PIPE, stderr=PIPE, shell=True)
    stdout, stderr = process.communicate()

    # print(stderr.decode('utf-8'))
    # print(stdout.decode('utf-8'))


def readJSONDetections(path="result.json"):
    if path is None:
        with open(os.path.join(ROOT_DIR, 'result.json')) as f:
            detections = json.load(f)
    else:
        with open(os.path.join(ROOT_DIR, path)) as f:
            detections = json.load(f)

    return detections


def readJSONObjects(frame_dict):
    objects = frame_dict['objects']

    # # object with max confidence
    # obj = max(objects, key=lambda detected_obj: detected_obj['confidence'])
    #
    # class_name = obj['name']
    # confidence = obj['confidence']
    # relative_coords = obj['relative_coordinates']

    return objects


def readBBoxCoordinates(relative_coords):
    width = 640
    height = 480

    center_x = int(relative_coords['center_x'] * width)
    center_y = int(relative_coords['center_y'] * height)

    width_box = int(relative_coords['width'] * width)
    height_box = int(relative_coords['height'] * height)

    return center_x, center_y, width_box, height_box


def getTopLeftCorner(x_center, y_center, width, height):
    return int(x_center - width / 2), int(y_center - height / 2)


def getBottomRightCorner(x_center, y_center, width, height):
    return int(x_center + width / 2), int(y_center + height / 2)
