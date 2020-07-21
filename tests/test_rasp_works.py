from subprocess import Popen, PIPE
import threading
from time import sleep
import os, fcntl, sys

sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
os.chdir("/home/valentin/FAKS/UGRS_projekt/alexeyAB_darknet/darknet")  # change to where darknet is

import cv2
import select
import shutil
import time

yolo_args = ["./darknet",
             "detect",
             "obj.data",
             "yolov3-tiny-prn-obj.cfg",
             "backup/yolov3-tiny-prn-obj_final.weights",
             "-thresh", "0.1"
             ]

# spawn darknet process
yolo_proc = Popen(yolo_args,
                  stdin=PIPE, stdout=PIPE)

fcntl.fcntl(yolo_proc.stdout.fileno(), fcntl.F_SETFL, os.O_NONBLOCK)

stdout_buf = ""
while True:
    select.select([yolo_proc.stdout], [], [])
    stdout = yolo_proc.stdout.read()
    stdout_buf += str(stdout)

    if len(stdout.strip()) > 0:
        print('get %s' % stdout)

    if 'Enter Image Path' in stdout_buf:
        break

    stdout_buf = ""

yolo_proc.stdin.write('data/person.jpg\n')
stdout_buf = ""
while True:
    select.select([yolo_proc.stdout], [], [])
    stdout = yolo_proc.stdout.read()
    stdout_buf += stdout

    if len(stdout.strip()) > 0:
        print('get %s' % stdout)

    if 'Enter Image Path' in stdout_buf:
        try:
            im = cv2.imread('predictions.jpg')
            print(im.shape)

            cv2.imshow('yolov3-tiny', im)
            cv2.waitKey(0)
            break
        except Exception as e:
            print("Error: ", e)

    # stdout_buf = ""

"""
while True:
    try:
        select.select([yolo_proc.stdout], [], [])
        stdout = yolo_proc.stdout.read()
        stdout_buf += stdout
        
        if 'Enter Image Path' in stdout_buf:
            try:
                yolo_proc.stdin.write('data/horses.jpg\n')
                
                im = cv2.imread('predictions.png')
                print(im.shape)
            
                cv2.imshow('yolov3-tiny',im)
                cv2.waitKey(0)

            except Exception as e:
                print("Error2: ", e)
    except Exception as e:
        print("Error: ", e)
    
    if len(stdout.strip())>0:
        print('get %s' % stdout)
"""
