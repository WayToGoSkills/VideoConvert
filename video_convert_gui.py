# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'video_convert_gui.ui'
#
# Created: Thu Mar 17 20:11:10 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(575, 326)
        MainWindow.setMinimumSize(QtCore.QSize(575, 294))
        self.centralWidget = QtGui.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.verticalLayoutWidget = QtGui.QWidget(self.centralWidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 0, 551, 281))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(5, 10, 5, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lineEdit_FolderPath = QtGui.QLineEdit(self.verticalLayoutWidget)
        self.lineEdit_FolderPath.setText("")
        self.lineEdit_FolderPath.setReadOnly(True)
        self.lineEdit_FolderPath.setObjectName("lineEdit_FolderPath")
        self.horizontalLayout.addWidget(self.lineEdit_FolderPath)
        self.pushButton_Browse = QtGui.QPushButton(self.verticalLayoutWidget)
        self.pushButton_Browse.setObjectName("pushButton_Browse")
        self.horizontalLayout.addWidget(self.pushButton_Browse)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.groupBox = QtGui.QGroupBox(self.verticalLayoutWidget)
        self.groupBox.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBox.setFlat(False)
        self.groupBox.setCheckable(False)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayoutWidget_2 = QtGui.QWidget(self.groupBox)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(10, 20, 535, 31))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(20, -1, -1, -1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.checkBox_Recursive = QtGui.QCheckBox(self.horizontalLayoutWidget_2)
        self.checkBox_Recursive.setChecked(True)
        self.checkBox_Recursive.setObjectName("checkBox_Recursive")
        self.horizontalLayout_2.addWidget(self.checkBox_Recursive)
        self.checkBox_Stabilize = QtGui.QCheckBox(self.horizontalLayoutWidget_2)
        self.checkBox_Stabilize.setChecked(True)
        self.checkBox_Stabilize.setObjectName("checkBox_Stabilize")
        self.horizontalLayout_2.addWidget(self.checkBox_Stabilize)
        self.checkBox_Reconvert = QtGui.QCheckBox(self.horizontalLayoutWidget_2)
        self.checkBox_Reconvert.setObjectName("checkBox_Reconvert")
        self.horizontalLayout_2.addWidget(self.checkBox_Reconvert)
        self.checkBox_Thumbnails = QtGui.QCheckBox(self.horizontalLayoutWidget_2)
        self.checkBox_Thumbnails.setObjectName("checkBox_Thumbnails")
        self.horizontalLayout_2.addWidget(self.checkBox_Thumbnails)
        self.verticalLayout.addWidget(self.groupBox)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setContentsMargins(5, -1, 5, -1)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtGui.QLabel(self.verticalLayoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.progressBar_Current = QtGui.QProgressBar(self.verticalLayoutWidget)
        self.progressBar_Current.setProperty("value", 0)
        self.progressBar_Current.setTextVisible(False)
        self.progressBar_Current.setObjectName("progressBar_Current")
        self.gridLayout.addWidget(self.progressBar_Current, 0, 1, 1, 1)
        self.label_CurrentPercent = QtGui.QLabel(self.verticalLayoutWidget)
        self.label_CurrentPercent.setAlignment(QtCore.Qt.AlignCenter)
        self.label_CurrentPercent.setObjectName("label_CurrentPercent")
        self.gridLayout.addWidget(self.label_CurrentPercent, 0, 2, 1, 1)
        self.label_3 = QtGui.QLabel(self.verticalLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.progressBar_All = QtGui.QProgressBar(self.verticalLayoutWidget)
        self.progressBar_All.setProperty("value", 0)
        self.progressBar_All.setTextVisible(False)
        self.progressBar_All.setObjectName("progressBar_All")
        self.gridLayout.addWidget(self.progressBar_All, 1, 1, 1, 1)
        self.label_AllFraction = QtGui.QLabel(self.verticalLayoutWidget)
        self.label_AllFraction.setAlignment(QtCore.Qt.AlignCenter)
        self.label_AllFraction.setObjectName("label_AllFraction")
        self.gridLayout.addWidget(self.label_AllFraction, 1, 2, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setContentsMargins(5, -1, 5, -1)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.lineEdit_Status = QtGui.QLineEdit(self.verticalLayoutWidget)
        self.lineEdit_Status.setReadOnly(True)
        self.lineEdit_Status.setObjectName("lineEdit_Status")
        self.gridLayout_2.addWidget(self.lineEdit_Status, 0, 1, 1, 1)
        self.label_5 = QtGui.QLabel(self.verticalLayoutWidget)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 0, 0, 1, 1)
        self.label_6 = QtGui.QLabel(self.verticalLayoutWidget)
        self.label_6.setObjectName("label_6")
        self.gridLayout_2.addWidget(self.label_6, 1, 0, 1, 1)
        self.lineEdit_Folder = QtGui.QLineEdit(self.verticalLayoutWidget)
        self.lineEdit_Folder.setReadOnly(True)
        self.lineEdit_Folder.setObjectName("lineEdit_Folder")
        self.gridLayout_2.addWidget(self.lineEdit_Folder, 1, 1, 1, 1)
        self.label_7 = QtGui.QLabel(self.verticalLayoutWidget)
        self.label_7.setObjectName("label_7")
        self.gridLayout_2.addWidget(self.label_7, 2, 0, 1, 1)
        self.lineEdit_File = QtGui.QLineEdit(self.verticalLayoutWidget)
        self.lineEdit_File.setReadOnly(True)
        self.lineEdit_File.setObjectName("lineEdit_File")
        self.gridLayout_2.addWidget(self.lineEdit_File, 2, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_2)
        self.buttonBox = QtGui.QDialogButtonBox(self.verticalLayoutWidget)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtGui.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 575, 22))
        self.menuBar.setObjectName("menuBar")
        MainWindow.setMenuBar(self.menuBar)
        self.statusBar = QtGui.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Test Window", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEdit_FolderPath.setPlaceholderText(QtGui.QApplication.translate("MainWindow", "Choose Folder to Convert...", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_Browse.setText(QtGui.QApplication.translate("MainWindow", "Browse...", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("MainWindow", "Options", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox_Recursive.setText(QtGui.QApplication.translate("MainWindow", "Recursive?", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox_Stabilize.setText(QtGui.QApplication.translate("MainWindow", "Stabilize?", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox_Reconvert.setText(QtGui.QApplication.translate("MainWindow", "Reconvert Videos?", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox_Thumbnails.setText(QtGui.QApplication.translate("MainWindow", "Recreate Thumbnails?", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Current File:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_CurrentPercent.setText(QtGui.QApplication.translate("MainWindow", "0%", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("MainWindow", "All Files:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_AllFraction.setText(QtGui.QApplication.translate("MainWindow", "0 / 0", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("MainWindow", "Status:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("MainWindow", "Folder:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("MainWindow", "File:", None, QtGui.QApplication.UnicodeUTF8))
