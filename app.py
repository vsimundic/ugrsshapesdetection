import sys
from ugrsshapesdetection.qtapp import setupWindows


def run():
    # show windows
    app_windows, settings_window = setupWindows.initializeWindows()
    settings_window.show()
    sys.exit(app_windows.exec_())
