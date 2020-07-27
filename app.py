import os
import sys
if os.uname()[4][:3] == 'x86':
    os.chdir("/home/valentin/FAKS/UGRS_projekt/alexeyAB_darknet/darknet")  # change to where darknet is
elif os.uname()[4][:3] == 'arm':
    os.chdir("/home/pi/UGRS_projekt/darknet_new/darknet-nnpack")  # change to where darknet is

from .yolodetection import yolo
from .cameramanipulation import frame_manipulation, initialize_camera as initcam, webcam
from .colordetermination import colordeterminator as clrd
# from .uartcommunication import communication as stmcom
import cv2
import numpy as np
from time import sleep
import serial

def run():
    print("Krenio")
    ser = serial.Serial('/dev/ttyAMA0', 9600)
    # upali kamere!
    cam1 = webcam.Webcam(0)
    print("Proso kameru")
    
    _, frame1 = cam1.getFrame()
    if frame1 is not None:
        print("Not Gut")
    
    
    # cam2 = webcam.Webcam(0)
    # if not os.path.exists("frames.txt"):
    with open("frames.txt", 'w') as f:
        f.write("frame0.jpg\n")
        # f.write("frame1.jpg\n")
    
    while True:
        print("Cekam podatke")
        # TODO - communication
        from_stm = ser.readline()
        from_stm = from_stm.decode("utf-8")
        print(from_stm)
        
        if "start" in from_stm:
            # oke, primio sam nesto - ajmo dalje
            print("Primio podatak")


            _, frame1 = cam1.getFrame()
            # _, frame2 = cam2.getFrame()

            if frame1 is not None:
                cam1.saveFrame(grayscale=True, path=os.getcwd()+"/frame0.jpg")
            #        cam2.saveFrame(grayscale=True, path=os.getcwd()+"/frame1.jpg")
            #    else:
            #        sys.exit("Couldn't get frame1.")

            #####################
            # cv2.imshow("Prva kam", frame1)
            # cv2.imshow("Druga kam", frame2)
            # cv2.waitKey(0)
            ######################

            # perform detection and save bboxes to .json file
            yolo.detect()
            if not os.path.exists('result.json'):
                sys.exit("Did not find result.json. YOLO probably failed.")
            
            print("Detektiro yole")
            detections_data = yolo.readJSONDetections(path="/result.json")

            yolo.reset_class_scores()

            objects = []
            frame_id = 0
            for detections_in_frame in detections_data:
                objects = yolo.readJSONObjects(detections_in_frame)

                for frame_object in objects:
                    name = frame_object["name"]
                    confidence = frame_object["confidence"]

                    yolo.add_to_class_score(name, confidence)

            CLASS_NAME = yolo.get_most_confident_class()
            print("Class name: {}".format(CLASS_NAME))

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

            # print(relative_coords)
            if not relative_coords:
                ser.write("none\r\n".encode('utf-8'))
                continue
            center_x, center_y, _, _ = yolo.readBBoxCoordinates(relative_coords)

            if frame_id == 1:
                frame_for_color = frame1
            elif frame_id == 2:
                frame_for_color = frame2
            else:
                sys.exit("No frame for color")

            offset = 5
            # print(frame_for_color)
            roi_for_color = frame_for_color[center_x-offset:center_x+offset, center_y-offset:center_y+offset, :].copy()

            roi_for_color = cv2.cvtColor(roi_for_color, cv2.COLOR_BGR2RGB)

            r = int(np.mean(roi_for_color[:, :, 0]))
            g = int(np.mean(roi_for_color[:, :, 1]))
            b = int(np.mean(roi_for_color[:, :, 2]))

            COLOR_NAME = min(clrd.colors.items(), key=clrd.NearestColorKey((r, g, b)))
            print(r, g, b)
            print(COLOR_NAME)

            # cv2.imshow("Detektirano", frame_for_color[center_x-offset:center_x+offset, center_y-offset:center_y+offset, :])
            # cv2.waitKey(0)

            # TODO - poslati Stambiju klasu i boju
            
            ser.write(CLASS_NAME.encode('utf-8') + "\r\n".encode('utf-8'))
            sleep(0.05)
            ser.write(COLOR_NAME[0].encode('utf-8') + "\r\n".encode('utf-8'))
            
            print("Poslo podatke")
