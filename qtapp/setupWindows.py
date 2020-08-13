from .settings_window_controller import SettingsWindow
from PyQt5 import QtCore, QtGui, QtWidgets
import sys


def initializeWindows():
    app = QtWidgets.QApplication(sys.argv)
    settings_window = SettingsWindow(QtWidgets.QMainWindow())
    # settings_window.show()

    return app, settings_window
