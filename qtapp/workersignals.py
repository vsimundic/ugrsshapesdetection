from PyQt5 import QtCore
import traceback, sys

class WorkerSignals(QtCore.QObject):
    object_ = QtCore.pyqtSignal(object)
    update_frame_ = QtCore.pyqtSignal()
    update_detection_frame_ = QtCore.pyqtSignal()
