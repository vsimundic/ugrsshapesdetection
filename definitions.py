import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

DARKNET_PATH = "/home/valentin/FAKS/UGRS_projekt/alexeyAB_darknet/darknet"
CAM_NUMBER = 0
EMBEDDED_CAM = False
TABLE_HEADER = ['ID', 'Klasa', 'Boja', 'Masa', 'Kutija']
FLAG_RUN_ = False
flag_not_recognized = False

offset_color = 5
show_images_flag = False
determine_color_flag = True


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
