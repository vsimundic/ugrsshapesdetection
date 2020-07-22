import fcntl
import os.path, sys

# sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
os.chdir("/home/pi/UGRS_projekt/darknet_new/darknet-nnpack")  # change to where darknet is
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
                "-ext_output",
                "<",
                "frames.txt", ">", "result.txt"
                # "-out",
                # "result.json", "<", "frames.txt"
                # "frame0.jpg"
                ]

# cmdline_args_str = "./darknet detector test obj.data yolov3-tiny-prn-obj.cfg yolov3-tiny-prn-obj_best.weights frames.jpg"
cmdline_args_str = "./darknet detector test obj.data yolov3-tiny-prn-obj.cfg yolov3-tiny-prn-obj_best.weights -ext_output -dont_show -out resultz.json < frames.txt"
process = Popen(cmdline_args_str, stdout=PIPE, stderr=PIPE, shell=True)
stdout, stderr = process.communicate()
print(stdout.decode('utf-8'))
print(stderr.decode('utf-8'))
end = time.time()

print(end - start)
