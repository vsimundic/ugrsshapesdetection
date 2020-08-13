from .main_window_controller import MainWindow
from .settingswindow import Ui_SettingsWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from pathlib import Path
import ugrsshapesdetection.definitions as definitions
from .worker import Worker


class SettingsWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.parent = parent
        self.ui = Ui_SettingsWindow()
        self.ui.setupUi(self)
        self.setFixedSize(760, 320)
        self.ui.btn_Confirm.clicked.connect(self.confirmAndShowMain)

        self.main_window = None

        self.threadpool = QtCore.QThreadPool()
        # self.ui.btn_Confirm.clicked.connect(self.startRunThread())

    def startRunThread(self):
        pass

    def checkConditions(self):
        flag_confirm = True

        # create path from text edit
        darknet_path = Path(self.ui.textEdit_darknet_path.toPlainText())

        # check if the path exists and if it's not empty
        if darknet_path.exists() and str(darknet_path) != "." and str(darknet_path) != "":
            self.ui.lb_enterdarknetpath.setStyleSheet("QLabel {color:black}")
        else:
            flag_confirm = False
            self.ui.lb_enterdarknetpath.setStyleSheet("QLabel {color:red}")

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
        return flag_confirm, darknet_path

    def confirmAndShowMain(self):
        flag_confirm, darknet_path = self.checkConditions()

        # if all three conditions above are met
        if flag_confirm:
            definitions.DARKNET_PATH = str(darknet_path)

            definitions.EMBEDDED_CAM = self.ui.radioButton_embcam_yes.isChecked()

            if self.ui.rB_no1.isChecked():
                definitions.CAM_NUMBER = 1
            elif self.ui.rB_no2.isChecked():
                definitions.CAM_NUMBER = 2
            else:
                definitions.CAM_NUMBER = 3

            # destroy current window
            self.ui.centralwidget.hide()

            self.main_window = MainWindow(QtWidgets.QMainWindow())
            # open the main window
            self.main_window.show()
            worker = Worker()
            self.threadpool.start(worker)
            definitions.FLAG_RUN_ = True



if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    settings_window = SettingsWindow(QtWidgets.QMainWindow())
    settings_window.show()

    sys.exit(app.exec_())
