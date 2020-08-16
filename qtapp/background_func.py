import os
import sys
from ..yolodetection import yolo
from ..cameramanipulation import webcam
from ..colordetermination import colordeterminator as clrd
from ..uartcommunication import communicationhandler as uartcom
from ..definitions import *
import cv2
from time import sleep

os.chdir(ROOT_DIR)  # change to where darknet is


def run_detection():
    print("Krenio")

    # initialize serial
    uarthandler = uartcom.SerialHandler(port='/dev/ttyUSB0', baud_rate=9600)

    # camera stuff
    ids_cams = [-7, -6, -5]
    cams = [None, None, None]

    # find ids for cameras
    for i in range(CAM_NUMBER):
        ids_cams[i] = webcam.findCamID(ids_cams)
    print(ids_cams)

    # write how many images to detect based on the number of cameras
    with open(os.path.join(ROOT_DIR, "data", "yolo_config_files", "frames.txt", ), 'w') as f:
        for i in range(CAM_NUMBER):
            f.write(os.path.join("data", "yolo_config_files", "frame{}.jpg".format(i), "\n"))
            # f.write("data/yolo_config_files/frame{}.jpg\n".format(i))

    # looping
    while True:
        # initialize cameras
        print(CAM_NUMBER)
        for i in range(CAM_NUMBER):
            cams[i] = webcam.Webcam(ids_cams[i])

        # waiting for data
        print("Waiting for data")
        line_from_stm = uarthandler.read_line()

        # if there comes a trigger word
        if "start" in line_from_stm:
            print("Primio podatak")

            # Initialize frames for every camera
            rets_frames = [[False, None], [False, None], [False, None]]
            for i in range(CAM_NUMBER):
                while True:
                    # get frames from cameras
                    for k in range(10):
                        rets_frames[i][0], rets_frames[i][1] = cams[i].getFrame()

                    if rets_frames[i][1] is None and not rets_frames[i][0]:
                        cams[i].releaseCamera()
                        ids_cams[i] = webcam.findCamID(-5)
                        cams[i] = webcam.Webcam(ids_cams)
                    else:
                        break

            # save images as .jpg for detection
            flag_not_properly_saved = False
            for i in range(CAM_NUMBER):
                try:
                    cams[i].saveFrame(grayscale=True, path=os.path.join(ROOT_DIR, "data", "yolo_config_files", "frames",
                                                                        "frame{}.jpg".format(i)))
                except Exception as e:
                    print("No frame!!")
                    uarthandler.write_line("none\r\n")

                    for j in range(CAM_NUMBER):
                        cams[j].releaseCamera()

                    flag_not_properly_saved = True
                    break
            if flag_not_properly_saved:
                continue

            # release cameras (needed because it wouldn't get right frames)
            for i in range(CAM_NUMBER):
                cams[i].releaseCamera()

            if show_images_flag:
                #####################
                for i in range(CAM_NUMBER):
                    cv2.imshow("Camera {}".format(i + 1), rets_frames[i][1])

                cv2.waitKey(0)
                cv2.destroyAllWindows()
                ######################

            # perform detection and save bboxes to .json file
            yolo.detect(
                "{0}/darknet detector test {1}/obj.data {1}/yolov3-obj.cfg {1}/yolov3-obj_best.weights -ext_output -dont_show -out result.json < {1}/frames.txt ".
                format(DARKNET_PATH, 'data/yolo_config_files'))

            if not os.path.exists('../result.json'):
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

                try:
                    frame_for_color = rets_frames[frame_id - 1][1]

                except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    print("Error location: ", exc_type, fname, exc_tb.tb_lineno)
                    print("Error description: ", e)

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
                    prediction_image = cv2.imread("predictions.jpg", cv2.IMREAD_GRAYSCALE)
                    prediction_image = cv2.cvtColor(prediction_image, cv2.COLOR_GRAY2BGR)

                    prediction_image[center_y - offset_color:center_y + offset_color,
                    center_x - offset_color:center_x + offset_color, :] = frame_for_color[
                                                                          center_y - offset_color:center_y + offset_color,
                                                                          center_x - offset_color:center_x + offset_color,
                                                                          :].copy()

                    prediction_image = cv2.circle(prediction_image, (center_x, center_y), 5, (255, 0, 0), -1)

                    cv2.imshow("Detection", prediction_image)
                    cv2.waitKey(0)
                    cv2.destroyAllWindows()

            # send feedback
            uarthandler.write_line(CLASS_NAME + "\r\n")
            sleep(0.05)

            if determine_color_flag:
                uarthandler.write_line(COLOR_NAME + "\r\n")

            print("Poslo podatke")

            print("Cekam za masu i kutiju")
            while True:
                line_from_stm = uarthandler.read_line()

                mass_w_box = line_from_stm.split('show-')[1].split('/')
                mass = float(mass_w_box[0])
                box = int(mass_w_box[1])

                # send to window
