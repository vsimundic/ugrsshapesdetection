# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SettingsWindow.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_SettingsWindow(object):
    def setupUi(self, SettingsWindow):
        SettingsWindow.setObjectName("SettingsWindow")
        SettingsWindow.resize(760, 320)
        self.centralwidget = QtWidgets.QWidget(SettingsWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox_darknetpath = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_darknetpath.setGeometry(QtCore.QRect(40, 10, 680, 90))
        self.groupBox_darknetpath.setTitle("")
        self.groupBox_darknetpath.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox_darknetpath.setObjectName("groupBox_darknetpath")
        self.lb_enterdarknetpath = QtWidgets.QLabel(self.groupBox_darknetpath)
        self.lb_enterdarknetpath.setGeometry(QtCore.QRect(20, 0, 641, 51))
        self.lb_enterdarknetpath.setTextFormat(QtCore.Qt.RichText)
        self.lb_enterdarknetpath.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lb_enterdarknetpath.setObjectName("lb_enterdarknetpath")
        self.textEdit_darknet_path = QtWidgets.QTextEdit(self.groupBox_darknetpath)
        self.textEdit_darknet_path.setGeometry(QtCore.QRect(20, 50, 641, 31))
        self.textEdit_darknet_path.setObjectName("textEdit_darknet_path")
        self.groupBox_embeddedcam = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_embeddedcam.setGeometry(QtCore.QRect(40, 105, 680, 60))
        self.groupBox_embeddedcam.setTitle("")
        self.groupBox_embeddedcam.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox_embeddedcam.setObjectName("groupBox_embeddedcam")
        self.lb_embeddedcam = QtWidgets.QLabel(self.groupBox_embeddedcam)
        self.lb_embeddedcam.setGeometry(QtCore.QRect(20, 0, 291, 51))
        self.lb_embeddedcam.setTextFormat(QtCore.Qt.RichText)
        self.lb_embeddedcam.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lb_embeddedcam.setObjectName("lb_embeddedcam")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.groupBox_embeddedcam)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(320, 10, 341, 31))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.radioButton_embcam_yes = QtWidgets.QRadioButton(self.horizontalLayoutWidget)
        self.radioButton_embcam_yes.setObjectName("radioButton_embcam_yes")
        self.buttonGroup = QtWidgets.QButtonGroup(SettingsWindow)
        self.buttonGroup.setObjectName("buttonGroup")
        self.buttonGroup.addButton(self.radioButton_embcam_yes)
        self.horizontalLayout.addWidget(self.radioButton_embcam_yes)
        self.radioButton_embcam_no = QtWidgets.QRadioButton(self.horizontalLayoutWidget)
        self.radioButton_embcam_no.setObjectName("radioButton_embcam_no")
        self.buttonGroup.addButton(self.radioButton_embcam_no)
        self.horizontalLayout.addWidget(self.radioButton_embcam_no)
        self.groupBox_numcams = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_numcams.setGeometry(QtCore.QRect(40, 170, 680, 60))
        self.groupBox_numcams.setTitle("")
        self.groupBox_numcams.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox_numcams.setObjectName("groupBox_numcams")
        self.lb_how_many_cams = QtWidgets.QLabel(self.groupBox_numcams)
        self.lb_how_many_cams.setGeometry(QtCore.QRect(20, 0, 231, 51))
        self.lb_how_many_cams.setTextFormat(QtCore.Qt.RichText)
        self.lb_how_many_cams.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lb_how_many_cams.setObjectName("lb_how_many_cams")
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.groupBox_numcams)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(270, 10, 391, 31))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.rB_no1 = QtWidgets.QRadioButton(self.horizontalLayoutWidget_2)
        self.rB_no1.setObjectName("rB_no1")
        self.buttonGroup_2 = QtWidgets.QButtonGroup(SettingsWindow)
        self.buttonGroup_2.setObjectName("buttonGroup_2")
        self.buttonGroup_2.addButton(self.rB_no1)
        self.horizontalLayout_2.addWidget(self.rB_no1)
        self.rB_no2 = QtWidgets.QRadioButton(self.horizontalLayoutWidget_2)
        self.rB_no2.setObjectName("rB_no2")
        self.buttonGroup_2.addButton(self.rB_no2)
        self.horizontalLayout_2.addWidget(self.rB_no2)
        self.rB_no3 = QtWidgets.QRadioButton(self.horizontalLayoutWidget_2)
        self.rB_no3.setObjectName("rB_no3")
        self.buttonGroup_2.addButton(self.rB_no3)
        self.horizontalLayout_2.addWidget(self.rB_no3)
        self.btn_Confirm = QtWidgets.QPushButton(self.centralwidget)
        self.btn_Confirm.setGeometry(QtCore.QRect(290, 240, 151, 51))
        self.btn_Confirm.setObjectName("btn_Confirm")
        SettingsWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(SettingsWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 760, 25))
        self.menubar.setObjectName("menubar")
        SettingsWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(SettingsWindow)
        self.statusbar.setObjectName("statusbar")
        SettingsWindow.setStatusBar(self.statusbar)

        self.retranslateUi(SettingsWindow)
        QtCore.QMetaObject.connectSlotsByName(SettingsWindow)

    def retranslateUi(self, SettingsWindow):
        _translate = QtCore.QCoreApplication.translate
        SettingsWindow.setWindowTitle(_translate("SettingsWindow", "Postavke"))
        self.lb_enterdarknetpath.setText(_translate("SettingsWindow", "<html><head/><body><p><span style=\" font-size:14pt; font-weight:600;\">Unesi putanju darknet-a:</span></p></body></html>"))
        self.textEdit_darknet_path.setHtml(_translate("SettingsWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.lb_embeddedcam.setText(_translate("SettingsWindow", "<html><head/><body><p><span style=\" font-size:14pt; font-weight:600;\">Ima li uređaj ugrađenu kameru?</span></p></body></html>"))
        self.radioButton_embcam_yes.setText(_translate("SettingsWindow", "Da"))
        self.radioButton_embcam_no.setText(_translate("SettingsWindow", "Ne"))
        self.lb_how_many_cams.setText(_translate("SettingsWindow", "<html><head/><body><p><span style=\" font-size:14pt; font-weight:600;\">Koliko kamera se koristi?</span></p></body></html>"))
        self.rB_no1.setText(_translate("SettingsWindow", "1"))
        self.rB_no2.setText(_translate("SettingsWindow", "2"))
        self.rB_no3.setText(_translate("SettingsWindow", "3"))
        self.btn_Confirm.setText(_translate("SettingsWindow", "U redu"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    SettingsWindow = QtWidgets.QMainWindow()
    ui = Ui_SettingsWindow()
    ui.setupUi(SettingsWindow)
    SettingsWindow.show()
    sys.exit(app.exec_())

