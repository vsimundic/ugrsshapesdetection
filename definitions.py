import os
import pickle

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

try:
    DARKNET_PATH = ""
    with open(os.path.join(ROOT_DIR, "data", "vars", "variablesdarknet.pickle"), 'rb') as darknetpath_file:
        DARKNET_PATH = pickle.load(darknetpath_file)
except:
    DARKNET_PATH = ""

try:
    SERIAL_PORT = ""
    with open(os.path.join(ROOT_DIR, "data", "vars", "variablesserialport.pickle"), 'rb') as serialport_file:
        SERIAL_PORT = pickle.load(serialport_file)
except:
    SERIAL_PORT = ""



CAM_NUMBER = 0
EMBEDDED_CAM = False
TABLE_HEADER = ['ID', 'Klasa', 'Boja', 'Masa', 'Kutija']
FLAG_RUN_ = False
flag_not_recognized = False
flag_found_nothing = False
flag_thread_alive = True

offset_color = 5
show_images_flag = True
determine_color_flag = True


def kill_thread():
    global flag_thread_alive
    flag_thread_alive = False


def savedarknetpath():
    with open(os.path.join(ROOT_DIR, "data", "vars", "variablesdarknet.pickle"), 'wb') as darknetpath_file_:
        pickle.dump(DARKNET_PATH, darknetpath_file_)


def saveserialport():
    with open(os.path.join(ROOT_DIR, "data", "vars", "variablesserialport.pickle"), 'wb') as serialport_file_:
        pickle.dump(SERIAL_PORT, serialport_file_)

def set_serial_port(port):
    global SERIAL_PORT
    SERIAL_PORT = port
    saveserialport()


def set_darknet_path(darknet_path):
    global DARKNET_PATH
    DARKNET_PATH = darknet_path
    savedarknetpath()


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


def set_flag_found_nothing(flag_found_nothing_in):
    global flag_found_nothing
    flag_found_nothing = flag_found_nothing_in
