from PyQt5 import QtCore
# import ugrsshapesdetection.background_func as func
from ugrsshapesdetection.qtapp.background_func import run_detection

class Worker(QtCore.QRunnable):
    """
    Worker thread
    """

    @QtCore.pyqtSlot()
    def run(self) -> None:
        '''
        Runs outsider run
        :return: nothing
        '''

        run_detection()
