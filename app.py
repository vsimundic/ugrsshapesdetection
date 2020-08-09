import os
import sys

os.chdir(os.environ['DARKNET_PATH'])  # change to where darknet is

from .yolodetection import yolo
from .cameramanipulation import webcam
from .colordetermination import colordeterminator as clrd
from .uartcommunication import communicationhandler as uartcom
# from .lcd import lcddriver, i2c_lib

import cv2
from time import sleep

CAM_NUMBER = 2
show_images_flag = True
lcd_flag = False
determine_color_flag = False
offset_color = 5


def run():
    print("Krenio")

    # initialize serial
    uarthandler = uartcom.SerialHandler(port='/dev/ttyAMA0', baud_rate=9600)

    # find ids for cameras
    id_cam2 = -1
    id_cam1 = webcam.findCamID(-5)
    print(id_cam1)
    if CAM_NUMBER == 2:
        id_cam2 = webcam.findCamID(id_cam1)
        print(id_cam2)

    # write how many images to detect based on the number of cameras
    with open("frames.txt", 'w') as f:
        for i in range(CAM_NUMBER):
            f.write("frame{}.jpg\n".format(i))

    # looping
    while True:
        # initialize cameras
        cam1 = webcam.Webcam(id_cam1)
        # cam1.setResolution(width=525, height=525)
        cam2 = None
        if CAM_NUMBER == 2:
            cam2 = webcam.Webcam(id_cam2)

        # waiting for data
        print("Waiting for data")
        line_from_stm = uarthandler.read_line()

        # if there comes a trigger word
        if "start" in line_from_stm:
            print("Primio podatak")

            while True:
                # get frames from cameras
                ret1, frame1 = False, None
                for k in range(10):
                    ret1, frame1 = cam1.getFrame()

                if frame1 is None and not ret1:
                    cam1.releaseCamera()
                    id_cam1 = webcam.findCamID(-5)
                    cam1 = webcam.Webcam(id_cam1)
                else:
                    break

            while True:
                if CAM_NUMBER == 2:
                    ret2, frame2 = False, None
                    for k in range(10):
                        ret2, frame2 = cam2.getFrame()

                    if frame2 is None and not ret2:
                        cam2.releaseCamera()
                        id_cam2 = webcam.findCamID(id_cam1)
                        cam2 = webcam.Webcam(id_cam2)
                    else:
                        break

            # save images as .jpg for detection
            if ret1:
                cam1.saveFrame(grayscale=True, path=os.getcwd() + "/frame0.jpg")
                if CAM_NUMBER == 2 and ret2:
                    cam2.saveFrame(grayscale=True, path=os.getcwd() + "/frame1.jpg")
            else:
                print("No frame!!")
                uarthandler.write_line("none\r\n")
                cam1.releaseCamera()
                if CAM_NUMBER == 2:
                    cam2.releaseCamera()
                continue

            # release cameras (needed because it wouldn't get right frames)
            cam1.releaseCamera()
            if CAM_NUMBER == 2:
                cam2.releaseCamera()

            if show_images_flag:
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
                uarthandler.write_line("none\r\n")
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
                    # print(frame_object)
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

            if determine_color_flag:
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
                area_for_color = frame_for_color[center_y - offset_color:center_y + offset_color,
                                 center_x - offset_color:center_x + offset_color,
                                 :].copy()
                COLOR_NAME = clrd.detectLABColorArea(area=area_for_color, bgr=True)

                print(CLASS_NAME, COLOR_NAME)

                if show_images_flag:
                    top_left_corner = yolo.getTopLeftCorner(center_x, center_y, width, height)

                    prediction_image = cv2.imread("predictions.jpg", cv2.IMREAD_GRAYSCALE)
                    prediction_image = cv2.cvtColor(prediction_image, cv2.COLOR_GRAY2BGR)

                    prediction_image[center_y - offset_color:center_y + offset_color, center_x - offset_color:center_x + offset_color, :] = area_for_color.copy()

                    cv2.imshow("Detection", prediction_image)
                    cv2.imshow("Color determining area", area_for_color)
                    cv2.waitKey(0)
                    cv2.destroyAllWindows()

            # send feedback
            uarthandler.write_line(CLASS_NAME + "\r\n")
            sleep(0.05)

            if determine_color_flag:
                uarthandler.write_line(COLOR_NAME + "\r\n")

            print("Poslo podatke")

            # if lcd_flag:
            #     print("Cekam za lcd")
            #
            #     while True:
            #         line_from_stm = uarthandler.read_line()
            #
            #         # string from uart needs to start with 'lcd-'
            #         if line_from_stm.startswith("lcd-"):
            #             display.lcd_clear()
            #
            #             num_items_in_boxes = line_from_stm.split("lcd-")[1].split("/")
            #
            #             # display numbers of items in boxes
            #             display.lcd_display_string(' '.join(num_items_in_boxes), 1)
            #
            #             break
