import os
import sys

if os.uname()[4][:3] == 'x86':
    os.chdir("/home/valentin/FAKS/UGRS_projekt/alexeyAB_darknet/darknet")  # change to where darknet is
elif os.uname()[4][:3] == 'arm':
    os.chdir("/home/pi/UGRS_projekt/darknet_new/darknet-nnpack")  # change to where darknet is

from .yolodetection import yolo
from .cameramanipulation import webcam
from .colordetermination import colordeterminator as clrd
from .uartcommunication import communicationhandler as uartcom

import cv2
import numpy as np
from time import sleep
import serial

CAM_NUMBER = 1
show_images = True

def run():
    print("Krenio")
    
    # initialize serial
    uarthandler = uartcom.SerialHandler(port='/dev/ttyAMA0', baud_rate=9600)
    
    # find ids for cameras
    id_cam2 = -1
    id_cam1 = webcam.findCamID()
    print(id_cam1)
    if CAM_NUMBER == 2:
        id_cam2 = webcam.findCamID()
        print(id_cam2)
    
    # write how many images to detect based on the number of cameras
    with open("frames.txt", 'w') as f:
        for i in range(CAM_NUMBER):
            f.write("frame{}.jpg\n".format(i))
    
    # looping
    while True:
        # initialize cameras
        cam1 = webcam.Webcam(id_cam1)
        if CAM_NUMBER == 2:
            cam2 = webcam.Webcam(id_cam2)

        # waiting for data
        print("Waiting for data")
        line_from_stm = uarthandler.read_line()
        
        # if there comes a trigger word
        if "start" in line_from_stm:
            print("Primio podatak")
            
            # get frames from cameras
            ret1, frame1 = cam1.getFrame()
            
            if CAM_NUMBER == 2:
                ret2, frame2 = cam2.getFrame()

            # save images as .jpg for detection
            if ret1:
                cam1.saveFrame(grayscale=True, path=os.getcwd()+"/frame0.jpg")
                if CAM_NUMBER == 2 and ret2:
                    cam2.saveFrame(grayscale=True, path=os.getcwd()+"/frame1.jpg")
            else:
                print("No frame!!")
                uarhtandler.write_line("none\r\n")
                cam1.releaseCamera()
                if CAM_NUMBER == 2:
                    cam2.releaseCamera()
                continue
        
            # release cameras (needed because it wouldn't get right frames)
            cam1.releaseCamera()
            if CAM_NUMBER == 2:
                cam2.releaseCamera()
            
            if show_images:
                #####################
                cv2.imshow("First camera", frame1)
                
                if CAM_NUMBER == 2:
                    cv2.imshow("Second camera", frame2)
                
                cv2.waitKey(0)
                cv2.destroyAllWindows()
                ######################

            # perform detection and save bboxes to .json file
            yolo.detect()
            if not os.path.exists('result.json'):
                print("Did not find result.json. YOLO probably failed.")
                uarhtandler.write_line("none\r\n")
                continue
            
            detections_data = yolo.readJSONDetections(path="/result.json")

            yolo.reset_class_scores()
            
            # get classes and their confidences from json file
            objects = []
            frame_id = 0
            for detections_in_frame in detections_data:
                objects = yolo.readJSONObjects(detections_in_frame)

                for frame_object in objects:
                    name = frame_object["name"]
                    confidence = frame_object["confidence"]

                    yolo.add_to_class_score(name, confidence)

            CLASS_NAME = yolo.get_most_confident_class()
            
            # loop through detections and get coordinates
            relative_coords = {}
            for detections_in_frame in detections_data:
                objects = yolo.readJSONObjects(detections_in_frame)

                for frame_object in objects:
                    print(frame_object)
                    if CLASS_NAME in frame_object.values():
                        print(frame_object)
                        relative_coords = frame_object["relative_coordinates"]
                        frame_id = detections_in_frame["frame_id"]
                        break
            
            # if there are no detections
            if not relative_coords:
                uarthandler.write_line("none\r\n")
                print("NO DETECTIONS")
                continue
            
            # yolo gives center coordinates and width/height
            center_x, center_y, width, height = yolo.readBBoxCoordinates(relative_coords)
            
            if frame_id == 1:
                frame_for_color = frame1
            elif frame_id == 2:
                frame_for_color = frame2
            else:
                print("No frame for color")
                uarthandler.write_line("none\r\n")
                continue
            
            # determine color
            offset = 15
            area_for_color = frame_for_color[center_x-offset:center_x+offset, center_y-offset:center_y+offset, :].copy()
            roi_for_color = cv2.cvtColor(area_for_color, cv2.COLOR_BGR2RGB)
            
            COLOR_NAME = clrd.detectRGBColorArea(area=area_for_color, rgb=True)
            
            print(CLASS_NAME, COLOR_NAME)
            
            if show_images:
                top_left_corner = yolo.getTopLeftCorner(center_x, center_y, width, height)
                
                cv2.imshow("Detection", frame_for_color[top_left_corner[0]:top_left_corner[0]+width, top_left_corner[1]:top_left_corner[1]+height, :])
                cv2.imshow("Color determining area", area_for_color)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
            
            # send feedback
            uarthandler.write_line(CLASS_NAME + "\r\n")
            sleep(0.05)
            uarthandler.write_line(COLOR_NAME + "\r\n")
            
            print("Poslo podatke")
