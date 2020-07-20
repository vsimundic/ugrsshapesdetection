from yolodetection.yoloprocess import YOLOProcess
yolo_args = ["/home/valentin/FAKS/UGRS_projekt/alexeyAB_darknet/darknet/darknet",
             "detector", "test",
             "/home/valentin/FAKS/UGRS_projekt/alexeyAB_darknet/darknet/cfg/coco.data",
             "/home/valentin/FAKS/UGRS_projekt/alexeyAB_darknet/darknet/cfg/yolov3-tiny-prn.cfg",
             "/home/valentin/FAKS/UGRS_projekt/alexeyAB_darknet/darknet/yolov3-tiny-prn.weights",
             "-thresh", "0.3"
             ]
yolo = YOLOProcess(yolo_args)

detection_successful = yolo.detect("dog.jpg\n")
print("Haha")
if detection_successful:
    yolo.showPredictions()
