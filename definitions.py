import os
import pickle

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

try:
    DARKNET_PATH = ""
    with open(os.path.join(ROOT_DIR, "data", "vars", "variables.pickle"), 'rb') as darknetpath_file:
        DARKNET_PATH = pickle.load(darknetpath_file)
except:
    DARKNET_PATH = ""


CAM_NUMBER = 0
EMBEDDED_CAM = False
TABLE_HEADER = ['ID', 'Klasa', 'Boja', 'Masa', 'Kutija']
FLAG_RUN_ = False
flag_not_recognized = False

offset_color = 5
show_images_flag = False
determine_color_flag = True


def savedarknetpath():
    with open(os.path.join(ROOT_DIR, "data", "vars", "variables.pickle"), 'wb') as darknetpath_file:
        pickle.dump(DARKNET_PATH, darknetpath_file)


def set_darknet_path(darknet_path):
    global DARKNET_PATH
    DARKNET_PATH = darknet_path


def set_cam_number(cam_number):
    global CAM_NUMBER
    CAM_NUMBER = cam_number


def set_embedded_cam(embedded_cam):
    global EMBEDDED_CAM
    EMBEDDED_CAM = embedded_cam


def set_flag_run(flag_run):
    global FLAG_RUN_
    FLAG_RUN_ = flag_run


def set_flag_not_recognized(flag_not_recognized_in):
    global flag_not_recognized
    flag_not_recognized = flag_not_recognized_in
