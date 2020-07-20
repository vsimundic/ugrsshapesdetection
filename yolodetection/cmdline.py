import fcntl
import os
from subprocess import Popen, PIPE
import select
import cv2

def detect(yolo_process, image_path):

    while True:
        stdout_buffer = ""
        select.select([yolo_process.stdout], [], [])
        stdout = str(yolo_process.stdout.read())
        stdout_buffer += stdout