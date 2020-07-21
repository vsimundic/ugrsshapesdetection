import fcntl
import os.path, sys
from subprocess import Popen, PIPE, check_output
import select
import cv2


class YOLOProcess:
    def __init__(self, cmdline_args=None):
        if cmdline_args is None:
            cmdline_args = ["/home/valentin/FAKS/UGRS_projekt/alexeyAB_darknet/darknet/darknet",
                            "detect",
                            "/home/valentin/FAKS/UGRS_projekt/alexeyAB_darknet/darknet/cfg/coco.data",
                            "/home/valentin/FAKS/UGRS_projekt/alexeyAB_darknet/darknet/yolov3-tiny-prn-obj.cfg",
                            "/home/valentin/FAKS/UGRS_projekt/alexeyAB_darknet/darknet/yolov3-tiny-prn.weights",
                            "-thresh", "0.1"]

        self.process = Popen(cmdline_args, stdin=PIPE, stdout=PIPE)
        fcntl.fcntl(self.process.stdout.fileno(), fcntl.F_SETFL, os.O_NONBLOCK)  # setting non-blocking pipes

    def detect(self, image_path="data/dog.jpg"):
        # reading command line and waiting for YOLO to finish setup/detection
        stdout_buffer = ""
        while True:
            try:
                select.select([self.process.stdout], [], [])

                stdout = self.process.stdout.read()
                stdout_buffer += stdout

                if len(stdout.strip()) > 0:
                    print('get %s' % stdout)

                if 'Enter Image Path' in stdout_buffer:
                    break

                stdout_buffer = ""

            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print("Error location: ", exc_type, fname, exc_tb.tb_lineno)
                print("Error description: ", e)
                self.killprocess()
                return False

        # send image to YOLO detection
        try:
            print(image_path)
            self.process.stdin.write(image_path)
            # print("Ne dda")

            stdout_buffer = ""

            while True:
                select.select([self.process.stdout], [], [])

                stdout = self.process.stdout.read()
                print(stdout)
                stdout_buffer += stdout

                if len(stdout.strip()) > 0:
                    print('get %s' % stdout)

                if 'Enter Image Path' in stdout_buffer:
                    print("Enter image path yaaay")
                    if self.checkPredictionsExist():
                        return True

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("Error location: ", exc_type, fname, exc_tb.tb_lineno)
            print("Error description: ", e)
            return False

    def checkPredictionsExist(self):
        if os.path.exists("predictions.jpg"):
            return True
        return False

    def showPredictions(self):
        stdout = str(self.process.stdout.read())
        if stdout is not None:
            if "Enter Image Path" in self.process.stdout.read() and self.checkPredictionsExist():
                predictions_image = cv2.imread("predictions.jpg")
                cv2.imshow("predictions", predictions_image)
                cv2.waitKey(0)

    def killprocess(self):
        self.process.kill()
