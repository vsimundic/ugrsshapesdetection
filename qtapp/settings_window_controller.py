from .main_window_controller import MainWindow
from .settingswindow import Ui_SettingsWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from pathlib import Path
import ugrsshapesdetection.definitions as definitions
from .worker import Worker
import time

class SettingsWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.parent = parent
        self.ui = Ui_SettingsWindow()

        self.ui.setupUi(self)

        self.setFixedSize(self.size().width(), self.size().height())

        self.ui.btn_Confirm.setStyleSheet("background-color: #20639B")
        self.ui.btn_Confirm.clicked.connect(self.confirmAndShowMain)
        self.ui.textEdit_darknet_path.setText(definitions.DARKNET_PATH)
        self.ui.textEdit_serial_port.setText(definitions.SERIAL_PORT)

        self.main_window = None
        self.worker = None
        self.threadpool = QtCore.QThreadPool()


    def checkConditions(self):
        flag_confirm = True

        # create path from text edit
        darknet_path = Path(self.ui.textEdit_darknet_path.toPlainText())
        serial_port = Path(self.ui.textEdit_serial_port.toPlainText())

        # check if the path for darknet exists and if it's not empty
        if darknet_path.exists() and str(darknet_path) != "." and str(darknet_path) != "":
            self.ui.lb_enterdarknetpath.setStyleSheet("QLabel {color:black}")
        else:
            flag_confirm = False
            self.ui.lb_enterdarknetpath.setStyleSheet("QLabel {color:red}")

        # check if the path for serial port exists and if it's not empty
        if serial_port.exists() and str(serial_port) != "." and str(serial_port) != "":
            self.ui.lb_enterserialport.setStyleSheet("QLabel {color:black}")
        else:
            flag_confirm = False
            self.ui.lb_enterserialport.setStyleSheet("QLabel {color:red}")

        # check if embedded cam radio buttons are checked
        if self.ui.radioButton_embcam_yes.isChecked() or self.ui.radioButton_embcam_no.isChecked():
            self.ui.lb_embeddedcam.setStyleSheet("QLabel {color:black}")
        else:
            flag_confirm = False
            self.ui.lb_embeddedcam.setStyleSheet("QLabel {color:red}")

        # check number of cameras if checked
        if self.ui.rB_no1.isChecked() or self.ui.rB_no2.isChecked() or self.ui.rB_no3.isChecked():
            self.ui.lb_how_many_cams.setStyleSheet("QLabel {color:black}")
        else:
            flag_confirm = False
            self.ui.lb_how_many_cams.setStyleSheet("QLabel {color:red}")
        return flag_confirm, darknet_path, serial_port

    def confirmAndShowMain(self):

        flag_confirm, darknet_path, serial_port = self.checkConditions()

        # if all three conditions above are met
        if flag_confirm:
            definitions.set_darknet_path(str(darknet_path))
            definitions.set_serial_port(str(serial_port))
            definitions.set_embedded_cam(self.ui.radioButton_embcam_yes.isChecked())

            cam_num = 0
            if self.ui.rB_no1.isChecked():
                cam_num = 1
            elif self.ui.rB_no2.isChecked():
                cam_num = 2
            else:
                cam_num = 3

            definitions.set_cam_number(cam_num)

            # destroy current window
            self.ui.centralwidget.hide()

            self.main_window = MainWindow(QtWidgets.QMainWindow())
            # open the main window
            self.main_window.show()

            self.worker = Worker()
            self.worker.signals.object_.connect(self.processSignalFromWorker)
            self.worker.signals.update_frame_.connect(self.processUpdateFrameSignal)
            self.worker.signals.update_detection_frame_.connect(self.processUpdateDetectionFrameSignal)
            self.threadpool.start(self.worker)

            definitions.set_flag_run(True)

    def processSignalFromWorker(self, object_):
        self.main_window.insertRowinTables(object_)

    def processUpdateFrameSignal(self):
        self.main_window.updateFrames()

    def processUpdateDetectionFrameSignal(self):
        self.main_window.updateDetectionFrame()


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    settings_window = SettingsWindow(QtWidgets.QMainWindow())
    settings_window.show()

    sys.exit(app.exec_())
