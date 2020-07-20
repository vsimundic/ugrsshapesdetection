import fcntl
import os
from subprocess import Popen, PIPE


def initializeYOLOProcess(darknet_args=None):
    if darknet_args is None:
        darknet_args = ["/home/valentin/FAKS/UGRS_projekt/alexeyAB_darknet/darknet/darknet",
                        "detect",
                        "/home/valentin/FAKS/UGRS_projekt/alexeyAB_darknet/darknet/cfg/coco.data",
                        "/home/valentin/FAKS/UGRS_projekt/alexeyAB_darknet/darknet/yolov3-tiny-prn-obj.cfg",
                        "/home/valentin/FAKS/UGRS_projekt/alexeyAB_darknet/darknet/yolov3-tiny-prn.weights",
                        "-thresh", "0.3"]

    yolo_process = Popen(darknet_args, stdin=PIPE, stdout=PIPE)
    fcntl.fcntl(yolo_process.stdout.fileno(), fcntl.F_SETFL, os.O_NONBLOCK)

    return yolo_process
