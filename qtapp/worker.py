from PyQt5 import QtCore
# import ugrsshapesdetection.background_func as func
# from ugrsshapesdetection.qtapp.background_func import run_detection
import os
import sys
from ..yolodetection import yolo
from ..cameramanipulation import webcam
from ..colordetermination import colordeterminator as clrd
from ..uartcommunication import communicationhandler as uartcom
# from ..imagemanipulation import contours
import ugrsshapesdetection.definitions as definitions

from .workersignals import WorkerSignals
import cv2
from time import sleep, time
import platform

os.chdir(definitions.ROOT_DIR)  # change to where darknet is
CLASS_NAME = '#'
COLOR_NAME = '#'


class Worker(QtCore.QRunnable):
    """
    Worker thread
    """

    def __init__(self):
        super(Worker, self).__init__()

        self.signals = WorkerSignals()

    @QtCore.pyqtSlot()
    def run(self) -> None:
        """
        Runs everything
        :return: nothing
        """

        global CLASS_NAME
        global COLOR_NAME

        # run_detection()
        print("Krenio")

        # initialize serial
        uarthandler = uartcom.SerialHandler(port=definitions.SERIAL_PORT, baud_rate=9600, timeout=1)

        # camera stuff
        ids_cams = [-7, -6, -5]
        cams = [None, None, None]

        # find ids for cameras
        for i in range(definitions.CAM_NUMBER):
            ids_cams[i] = webcam.findCamID(ids_cams)
        print(ids_cams)

        # write how many images to detect based on the number of cameras
        with open(os.path.join(definitions.ROOT_DIR, "data", "yolo_config_files", "frames.txt", ), 'w') as f:
            for i in range(definitions.CAM_NUMBER):
                f.writelines(os.path.join(definitions.ROOT_DIR, "data", "yolo_config_files", "frames", "frame{}.jpg".format(i)) + "\n")

        # yolo command - based on type of OS
        yolo_command = "{0}/darknet{2} detector test {1}/obj.data {1}/yolov3-obj.cfg {1}/yolov3-obj_best.weights -ext_output -dont_show -out result.json < {1}/frames.txt ".format(
            definitions.DARKNET_PATH, 'data/yolo_config_files', '.exe' if 'windows' in platform.system().lower() else '')

        # load contours
        definitions.load_contours()

        # # # # # # # # # # # #
        # # # # # # # # # # # #
        # # # # LOOPING # # # #
        while definitions.flag_thread_alive:

            definitions.set_flag_found_nothing(False)
            definitions.set_flag_not_recognized(False)

            try:
                for i in range(definitions.CAM_NUMBER):
                    cams[i].releaseCamera()
            except:
                pass

            # initialize cameras
            print("Initializing webcams through IDs...")
            for i in range(definitions.CAM_NUMBER):
                print("Cam {} initialized".format(i))
                cams[i] = webcam.Webcam(ids_cams[i])

            # waiting for data
            print("Waiting for data...")
            line_from_stm = uarthandler.read_line()


            # if there comes a trigger word
            if "reset?" in line_from_stm:
                if definitions.flag_stop_sort:
                    sleep(0.2)
                    uarthandler.write_line("yes\r\n")
                    definitions.set_flag_stop_sort(False)
                    print("Sent stop")
                else:
                    sleep(0.2)
                    uarthandler.write_line("nope\r\n")
                    print("Sent go")

            elif "start" in line_from_stm:
                print("Data received...")

                print("Getting frames...")
                rets_frames = [[False, None], [False, None], [False, None]]
                for i in range(definitions.CAM_NUMBER):
                    while True:
                        # get frames from cameras
                        for k in range(3):
                            rets_frames[i][0], rets_frames[i][1] = cams[i].getFrame(contour=definitions.contours[i]) if definitions.flag_create_contour else cams[i].getFrame()

                        if rets_frames[i][1] is None and not rets_frames[i][0]:
                            cams[i].releaseCamera()
                            ids_cams[i] = webcam.findCamID(-5)
                            cams[i] = webcam.Webcam(ids_cams)
                        else:
                            break

                # save images as .jpg for detection
                print("Saving frames...")
                for i in range(definitions.CAM_NUMBER):
                    try:
                        cams[i].saveFrame(grayscale=True,
                                          path=os.path.join(definitions.ROOT_DIR, "data", "yolo_config_files", "frames",
                                                            "frame{}.jpg".format(i)))
                    except Exception as e:
                        print("Error: Couldn't save frame.")
                        uarthandler.write_line("none\r\n")

                        if definitions.flag_stop_sort:
                            sleep(0.2)
                            uarthandler.write_line("stop\r\n")
                            definitions.set_flag_stop_sort(False)
                            print("Sent stop")
                        else:
                            uarthandler.write_line("go\r\n")
                            print("Sent go")

                        definitions.set_flag_found_nothing(True)

                        for j in range(definitions.CAM_NUMBER):
                            cams[j].releaseCamera()

                        print("Couldn't save properly. Best of luck in the next loop.")
                        assert False

                self.signals.update_frame_.emit()


                # release cameras (needed because it wouldn't get right frames)
                print("Releasing cameras.")
                try:
                    for i in range(definitions.CAM_NUMBER):
                        cams[i].releaseCamera()
                except:
                    pass

                # delete result.json if exists
                try:
                    os.remove("result.json")
                except OSError:
                    pass

                # perform detection and save bboxes to .json file
                print("Performing detection!")
                start = time()
                yolo.detect(yolo_command)
                end = time()
                print("TIME ELAPSED: {}".format(end - start))

                if not os.path.exists(os.path.join(definitions.ROOT_DIR, "result.json")):
                    print("Did not find result.json. YOLO probably failed.")
                    uarthandler.write_line("none\r\n")
                    definitions.set_flag_not_recognized(True)
                    if definitions.flag_stop_sort:
                        sleep(0.2)
                        uarthandler.write_line("stop\r\n")
                        definitions.set_flag_stop_sort(False)
                        print("Sent stop")
                    else:
                        uarthandler.write_line("go\r\n")
                        print("Sent go")

                if not definitions.flag_not_recognized:
                    print("Detections successful, reading results.")
                    detections_data = yolo.readJSONDetections(path="result.json")

                    yolo.reset_class_scores()

                    # get classes and their confidences from json file
                    for detections_in_frame in detections_data:
                        objects = yolo.readJSONObjects(detections_in_frame)

                        for frame_object in objects:
                            name = frame_object["name"]
                            confidence = frame_object["confidence"]

                            yolo.add_to_class_score(name, confidence)

                    print("Getting most confident class.")
                    CLASS_NAME = yolo.get_most_confident_class()

                    # loop through detections and get coordinates
                    relative_coords = {}
                    frame_id = -1
                    for detections_in_frame in detections_data:
                        objects = yolo.readJSONObjects(detections_in_frame)

                        for frame_object in objects:
                            if CLASS_NAME in frame_object.values():
                                relative_coords = frame_object["relative_coordinates"]
                                frame_id = int(detections_in_frame["frame_id"])
                                break
                        else:
                            continue
                        break

                    # if there are no detections
                    if not relative_coords:
                        uarthandler.write_line("none\r\n")

                        if definitions.flag_stop_sort:
                            sleep(0.2)
                            uarthandler.write_line("stop\r\n")
                            definitions.set_flag_stop_sort(False)
                            print("Sent stop")
                        else:
                            uarthandler.write_line("go\r\n")
                            print("Sent go")

                        print("Relative coords empty, meaning no detection.")
                        definitions.set_flag_not_recognized(True)

                    if definitions.determine_color_flag and not definitions.flag_not_recognized:
                        print("Reading and determining color")
                        # yolo gives center coordinates and width/height
                        center_x, center_y, width, height = yolo.readBBoxCoordinates(relative_coords)
                        print("BOUNDING BOX DIMENSIONS: ", center_x, center_y, width, height)

                        frame_for_color = None
                        try:
                            if rets_frames[frame_id - 1][1] is None:
                                raise
                            print("FRAME ID: {}".format(frame_id))
                            frame_for_color = rets_frames[frame_id - 1][1]

                        except Exception as e:
                            exc_type, exc_obj, exc_tb = sys.exc_info()
                            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                            print("Error location: ", exc_type, fname, exc_tb.tb_lineno)
                            print("Error description: ", e)

                            print("No frame for color")
                            uarthandler.write_line("none\r\n")

                            if definitions.flag_stop_sort:
                                sleep(0.2)
                                uarthandler.write_line("stop\r\n")
                                definitions.set_flag_stop_sort(False)
                                print("Sent stop")
                            else:
                                uarthandler.write_line("go\r\n")
                                print("Sent go")

                            definitions.set_flag_not_recognized(True)

                        if not definitions.flag_not_recognized and frame_for_color is not None:
                            # determine color
                            scale = definitions.scale
                            area_for_color = frame_for_color[center_y - int(scale*height):center_y + int(scale*height), center_x - int(scale*width):center_x + int(scale*width), :].copy()
                            COLOR_NAME = clrd.detectLABColorArea(area=area_for_color, bgr=True)

                            prediction_image = cv2.imread(os.path.join(definitions.ROOT_DIR, "data", "yolo_config_files", "frames",  "frame{}.jpg".format(frame_id - 1)), cv2.IMREAD_GRAYSCALE)
                            prediction_image = cv2.cvtColor(prediction_image, cv2.COLOR_GRAY2BGR)
                            prediction_image[center_y - int(scale*height):center_y + int(scale*height),
                            center_x - int(scale*width):center_x + int(scale*width), :] = frame_for_color[
                                                                                                          center_y - int(scale*height):center_y + int(scale*height),
                                                                                                          center_x - int(scale*width):center_x + int(scale*width),
                                                                                                          :].copy()
                            prediction_image = cv2.rectangle(prediction_image, (int(center_x-width/2), int(center_y-height/2)), (int(center_x+width/2), int(center_y+height/2)), (255, 0, 255), 1)
                            prediction_image = cv2.circle(prediction_image, (center_x, center_y), 2, (255, 0, 0), -1)
                            cv2.imwrite(os.path.join(definitions.ROOT_DIR, "data", "yolo_config_files", "frames", "colored_area.jpg"), prediction_image)

                            self.signals.update_detection_frame_.emit()

                if not definitions.flag_not_recognized:
                    print("Sending feedback...")
                    # send feedback
                    print("CLASS NAME: ", CLASS_NAME)
                    uarthandler.write_line(CLASS_NAME.strip() + "\r\n")

                    sleep(0.2)

                    if definitions.determine_color_flag:
                        print("COLOR NAME: ", COLOR_NAME)
                        uarthandler.write_line(COLOR_NAME.strip() + "\r\n")
                        sleep(0.2)

                    if definitions.flag_stop_sort:
                        uarthandler.write_line("stop\r\n")
                        definitions.set_flag_stop_sort(False)
                        print("Sent stop")
                    else:
                        uarthandler.write_line("go\r\n")
                        print("Sent go")


                    print("Feedback sent")

                print("Waiting for mass and box data...")
                while True:
                    line_from_stm = uarthandler.read_line()

                    if 'show' in line_from_stm:
                        print("Data received")
                        mass_w_box = line_from_stm.split('show-')[1].split('/')
                        mass = float(mass_w_box[0])
                        box = int(mass_w_box[1])

                        object_to_insert = ['#', '#', mass, box]
                        if not definitions.flag_not_recognized:
                            object_to_insert = [CLASS_NAME, COLOR_NAME, mass, box]
                            print("Object to insert: {}".format(object_to_insert))

                        # send to window
                        self.signals.object_.emit(object_to_insert)

                        break
