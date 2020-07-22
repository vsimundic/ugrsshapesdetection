import fcntl
import os.path, sys

# sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
os.chdir("/home/pi/UGRS_projekt/darknet_new/darknet-nnpack")  # change to where darknet is

from subprocess import Popen, PIPE
import select
import cv2
import time

"""
start = time.time()

cmdline_args = ["./darknet",
                "detector", "test",
                "obj.data",
                "yolov3-tiny-prn-obj.cfg",
                "yolov3-tiny-prn-obj_best.weights",
                "-dont_show",
                # "-out",
                # "result.json", "<", "frames.txt"
                # "frame0.jpg"
                ]
process = Popen(cmdline_args, stdout=PIPE, stderr=PIPE, stdin=PIPE)

stdout, stderr = process.communicate(b"frame0.jpg\n")

print(stderr.decode('utf-8'))
print(stdout.decode('utf-8'))


end = time.time()

print(end - start)
"""

cmdline_args = ["./darknet",
                "detector", "test",
                "obj.data",
                "yolov3-tiny-prn-obj.cfg",
                "yolov3-tiny-prn-obj_best.weights",
                "-dont_show",
                ]
