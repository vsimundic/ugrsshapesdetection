from .mainwindow import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from .tablemodel import TableModel
import ugrsshapesdetection.definitions as definitions
import pandas as pd
import os


def createEmptyTableView(tableview):
    tableModel = TableModel()
    tableview.setModel(tableModel)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setFixedSize(1030, 550)

        self.parent = parent
        self.last_table = 0

        self.ui.btn_Reset.clicked.connect(self.clickedReset)
        self.ui.btn_Save.clicked.connect(self.clickedSave)
        self.ui.btn_Load.clicked.connect(self.clickedLoad)

        self.ui.tabWidget_Boxes.setCurrentIndex(0)

        self.setDefaultTables()
        self.initializeFramesPixmap()
        self.updateImFrames()

        # self.ui.tableView_BoxesAll.model().rowsAboutToBeInserted(self.beforeInsert)
        # self.ui.tableView_Box1.setAutoScroll(True)
        # self.ui.tableView_Box2.setAutoScroll(True)
        # self.ui.tableView_Box3.setAutoScroll(True)
        # self.ui.tableView_Other.setAutoScroll(True)

    # def beforeInsert(self):
    #     idx = self.ui.tabWidget_Boxes.currentIndex()
    #     tableview = self.ui.tabWidget_Boxes.childAt(idx)
    #
    #     pass

    # def afterInsert(self):
    #     pass

    def insertRowinTables(self, row_in):
        row_w_id = row_in.copy()
        row_w_id.insert(0, self.ui.tableView_BoxesAll.model().rowCount())

        self.ui.tableView_BoxesAll.model().insertRow_(row_w_id)
        self.ui.tableView_BoxesAll.model().layoutChanged.emit()

        box_num = row_w_id[-1]
        if box_num == 1:
            self.ui.tableView_Box1.model().insertRow_(row_w_id)
            self.ui.tableView_Box1.model().layoutChanged.emit()
            self.last_table = 1

        elif box_num == 2:
            self.ui.tableView_Box2.model().insertRow_(row_w_id)
            self.ui.tableView_Box2.model().layoutChanged.emit()
            self.last_table = 2

        elif box_num == 3:
            self.ui.tableView_Box3.model().insertRow_(row_w_id)
            self.ui.tableView_Box3.model().layoutChanged.emit()
            self.last_table = 3

        elif box_num == 4:
            self.ui.tableView_Other.model().insertRow_(row_w_id)
            self.ui.tableView_Other.model().layoutChanged.emit()
            self.last_table = 4

        self.updateBoxNumberLabels()
        self.updateLasPredictedLabels()

    def clickedReset(self):
        for i in range(self.ui.tabWidget_Boxes.count()):
            tableviews = self.ui.tabWidget_Boxes.widget(i).findChildren(QtWidgets.QTableView)
            for j in range(len(tableviews)):
                tableview = tableviews[j]
                tablemodel = tableview.model()
                tablemodel.cleanModel()
                tablemodel.layoutChanged.emit()

        self.updateBoxNumberLabels()
        self.updateLasPredictedLabels()

    def clickedSave(self):

        df = self.ui.tableView_BoxesAll.model().getData()

        if not df.empty:
            df.to_csv(os.path.join(definitions.ROOT_DIR, 'data', 'tables', 'objects.csv'), index=False)

    def clickedLoad(self):
        path_to_table = os.path.join(definitions.ROOT_DIR, 'data', 'tables', 'objects.csv')

        if os.path.exists(path_to_table):
            model = self.ui.tableView_BoxesAll.model()
            df = pd.read_csv(path_to_table)
            model.insertData(df)
            model.layoutChanged.emit()

            for index, row in df.iterrows():
                row_in = []
                for header in definitions.TABLE_HEADER:
                    row_in.append(row[header])

                if row['Kutija'] == 1:
                    self.ui.tableView_Box1.model().insertRow_(row_in)
                    self.ui.tableView_Box1.model().layoutChanged.emit()
                elif row['Kutija'] == 2:
                    self.ui.tableView_Box2.model().insertRow_(row_in)
                    self.ui.tableView_Box2.model().layoutChanged.emit()
                elif row['Kutija'] == 3:
                    self.ui.tableView_Box3.model().insertRow_(row_in)
                    self.ui.tableView_Box3.model().layoutChanged.emit()
                else:
                    self.ui.tableView_Other.model().insertRow_(row_in)
                    self.ui.tableView_Other.model().layoutChanged.emit()

        self.updateBoxNumberLabels()
        self.updateLasPredictedLabels()

    def setDefaultTables(self):
        for i in range(self.ui.tabWidget_Boxes.count()):
            tableviews = self.ui.tabWidget_Boxes.widget(i).findChildren(QtWidgets.QTableView)
            for j in range(len(tableviews)):
                tableview = tableviews[j]
                createEmptyTableView(tableview)
                tableview.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

    def updateBoxNumberLabels(self):
        self.ui.lb_All_num.setText(str(self.ui.tableView_BoxesAll.model().rowCount()))
        self.ui.lb_Box1_num.setText(str(self.ui.tableView_Box1.model().rowCount()))
        self.ui.lb_Box2_num.setText(str(self.ui.tableView_Box2.model().rowCount()))
        self.ui.lb_Box3_num.setText(str(self.ui.tableView_Box3.model().rowCount()))
        self.ui.lb_BoxOther_num.setText(str(self.ui.tableView_Other.model().rowCount()))

    def updateLasPredictedLabels(self):
        if not self.ui.tableView_BoxesAll.model().isEmpty():
            last_object, index = self.ui.tableView_BoxesAll.model().getLast()
            self.ui.lb_class_name.setText(last_object.Klasa[index])
            self.ui.lb_color_name.setText(last_object.Boja[index])
        else:
            self.ui.lb_class_name.setText('#')
            self.ui.lb_color_name.setText('#')

    def updateFrames(self):
        try:
            self.ui.img_frame0.setPixmap(
                QtGui.QPixmap(os.path.join(definitions.ROOT_DIR, 'data', 'yolo_config_files', 'frames', 'frame0.jpg')))
            self.ui.stackedWidget_frames.setCurrentIndex(0)
            print("Done did frame 0")

            if definitions.CAM_NUMBER == 2:
                self.ui.img_frame1.setPixmap(QtGui.QPixmap(
                    os.path.join(definitions.ROOT_DIR, 'data', 'yolo_config_files', 'frames', 'frame1.jpg')))
                self.ui.stackedWidget_frames.setCurrentIndex(1)
                print("Done did frame 1")
            elif definitions.CAM_NUMBER == 3:
                self.ui.img_frame2.setPixmap(QtGui.QPixmap(
                    os.path.join(definitions.ROOT_DIR, 'data', 'yolo_config_files', 'frames', 'frame2.jpg')))
                self.ui.stackedWidget_frames.setCurrentIndex(2)
                print("Done did frame 2")
        except Exception as e:
            print("That's all when it comes to frames.")

    def updateDetectionFrame(self):
        path = os.path.join(definitions.ROOT_DIR, "data", "yolo_config_files", "frames", "colored_area.jpg")
        try:
            if definitions.CAM_NUMBER == 1:
                print("SET DETECTION IMAGE AA")
                self.ui.img_frame1.setPixmap(QtGui.QPixmap(path))
                self.ui.stackedWidget_frames.setCurrentIndex(1)
            elif definitions.CAM_NUMBER == 2:
                self.ui.img_frame2.setPixmap(QtGui.QPixmap(path))
                self.ui.stackedWidget_frames.setCurrentIndex(2)
            elif definitions.CAM_NUMBER == 3:
                self.ui.img_frame3.setPixmap(QtGui.QPixmap(path))
                self.ui.stackedWidget_frames.setCurrentIndex(3)
        except Exception as e:
            print("Couldn't get detection frame.")

    def initializeFramesPixmap(self):

        if definitions.CAM_NUMBER == 1:
            # self.ui.img_frame1.deleteLater()
            # self.ui.img_frame1 = None
            # self.ui.page_frame1.deleteLater()
            # self.ui.page_frame1 = None
            self.ui.img_frame2.deleteLater()
            self.ui.img_frame2 = None
            self.ui.page_frame2.deleteLater()
            self.ui.page_frame2 = None
            self.ui.img_frame3.deleteLater()
            self.ui.img_frame3 = None
            self.ui.page_frame3.deleteLater()
            self.ui.page_frame3 = None
        elif definitions.CAM_NUMBER == 2:
            # self.ui.img_frame2.deleteLater()
            # self.ui.img_frame2 = None
            # self.ui.page_frame2.deleteLater()
            # self.ui.page_frame2 = None
            self.ui.img_frame3.deleteLater()
            self.ui.img_frame3 = None
            self.ui.page_frame3.deleteLater()
            self.ui.page_frame3 = None

        for i in range(self.ui.stackedWidget_frames.count()):
            imageframes = self.ui.stackedWidget_frames.widget(i).findChildren(QtWidgets.QLabel)
            for j in range(len(imageframes)):
                imframe = imageframes[j]
                imframe.mouseReleaseEvent = self.clickedImFrame

                imframe.setHidden(True)

    def clickedImFrame(self, event):
        index = self.ui.stackedWidget_frames.currentIndex()
        index = index + 1 if index < definitions.CAM_NUMBER else 0

        self.ui.stackedWidget_frames.setCurrentIndex(index)

    def updateImFrames(self):
        if self.ui.img_frame0.isHidden():
            self.ui.img_frame0.setHidden(False)
            self.ui.img_frame1.setHidden(False)
            if definitions.CAM_NUMBER == 2:
                self.ui.img_frame1.setHidden(False)
                self.ui.img_frame2.setHidden(False)
            elif definitions.CAM_NUMBER == 3:
                self.ui.img_frame1.setHidden(False)
                self.ui.img_frame2.setHidden(False)
                self.ui.img_frame3.setHidden(False)

        self.ui.img_frame0.repaint()
        # self.ui.img_frame1.repaint() if definitions.CAM_NUMBER == 2 else False
        # self.ui.img_frame2.repaint() if definitions.CAM_NUMBER == 3 else False
        # self.ui.img_frame3.repaint() if definitions.CAM_NUMBER == 3 else False
        self.ui.img_frame1.repaint()
        self.ui.img_frame2.repaint() if definitions.CAM_NUMBER == 2 else False
        self.ui.img_frame3.repaint() if definitions.CAM_NUMBER == 3 else False

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        definitions.kill_thread()
