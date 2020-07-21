import fcntl
import os.path, sys

sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
os.chdir("/home/valentin/FAKS/UGRS_projekt/alexeyAB_darknet/darknet")  # change to where darknet is
from subprocess import Popen, PIPE
import select
import cv2
import time

start = time.time()
cmdline_args = ["./darknet",
                "detector", "test",
                "obj.data",
                "yolov3-tiny-prn-obj.cfg",
                "backup/yolov3-tiny-prn-obj_final.weights",
                "-dont_show",
                "-thresh", "0.1",
                "-ext_output", "<", "frames.txt", ">", "result.txt"
                ]

process = Popen(cmdline_args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
stdout, stderr = process.communicate()
# print(stdout)
# print(stderr)
end = time.time()

print(end - start)
