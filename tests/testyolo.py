from yolodetection.yoloprocess import YOLOProcess
import os

# os.chdir("/home/valentin/FAKS/UGRS_projekt/alexeyAB_darknet/darknet")  # change to where darknet is

# yolo_args = ["/home/valentin/FAKS/UGRS_projekt/alexeyAB_darknet/darknet/darknet",
#              "detector", "test",
#              "/home/valentin/FAKS/UGRS_projekt/alexeyAB_darknet/darknet/cfg/coco.data",
#              "/home/valentin/FAKS/UGRS_projekt/alexeyAB_darknet/darknet/cfg/yolov3-tiny-prn.cfg",
#              "/home/valentin/FAKS/UGRS_projekt/alexeyAB_darknet/darknet/yolov3-tiny-prn.weights",
#              "-thresh", "0.3"
#              ]

yolo_args = ["./darknet",
             "detect",
             "obj.data",
             "yolov3-tiny-prn-obj.cfg",
             "backup/yolov3-tiny-prn-obj_final.weights",
             "-thresh", "0.1"
             ]
yolo = YOLOProcess(cmdline_args=yolo_args)

# detection_successful = yolo.detect("frame.jpg\n")
# print("Haha")
# if detection_successful:
#     yolo.showPredictions()
