# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SpectraViewGUI.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setMinimumSize(QtCore.QSize(25, 0))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.tab)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.toolBar1 = QtWidgets.QWidget(self.tab)
        self.toolBar1.setMinimumSize(QtCore.QSize(25, 0))
        self.toolBar1.setMaximumSize(QtCore.QSize(16777215, 30))
        self.toolBar1.setObjectName("toolBar1")
        self.horizontalLayout_2.addWidget(self.toolBar1)
        self.label_2 = QtWidgets.QLabel(self.tab)
        self.label_2.setMaximumSize(QtCore.QSize(30, 16777215))
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.ImagMin = QtWidgets.QLineEdit(self.tab)
        self.ImagMin.setMaximumSize(QtCore.QSize(50, 16777215))
        self.ImagMin.setObjectName("ImagMin")
        self.horizontalLayout_2.addWidget(self.ImagMin)
        self.label_4 = QtWidgets.QLabel(self.tab)
        self.label_4.setMaximumSize(QtCore.QSize(30, 16777215))
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_2.addWidget(self.label_4)
        self.ImagMax = QtWidgets.QLineEdit(self.tab)
        self.ImagMax.setMaximumSize(QtCore.QSize(50, 16777215))
        self.ImagMax.setObjectName("ImagMax")
        self.horizontalLayout_2.addWidget(self.ImagMax)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.mpl1 =  MatplotlibWidget(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mpl1.sizePolicy().hasHeightForWidth())
        self.mpl1.setSizePolicy(sizePolicy)
        self.mpl1.setObjectName("mpl1")
        self.verticalLayout.addWidget(self.mpl1)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tab_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.toolBar2 = QtWidgets.QWidget(self.tab_2)
        self.toolBar2.setMaximumSize(QtCore.QSize(16777215, 30))
        self.toolBar2.setObjectName("toolBar2")
        self.horizontalLayout_5.addWidget(self.toolBar2)
        self.label_14 = QtWidgets.QLabel(self.tab_2)
        self.label_14.setMaximumSize(QtCore.QSize(30, 16777215))
        self.label_14.setObjectName("label_14")
        self.horizontalLayout_5.addWidget(self.label_14)
        self.ProyMin = QtWidgets.QLineEdit(self.tab_2)
        self.ProyMin.setMaximumSize(QtCore.QSize(50, 16777215))
        self.ProyMin.setObjectName("ProyMin")
        self.horizontalLayout_5.addWidget(self.ProyMin)
        self.label_16 = QtWidgets.QLabel(self.tab_2)
        self.label_16.setMaximumSize(QtCore.QSize(30, 16777215))
        self.label_16.setObjectName("label_16")
        self.horizontalLayout_5.addWidget(self.label_16)
        self.ProyMax = QtWidgets.QLineEdit(self.tab_2)
        self.ProyMax.setMaximumSize(QtCore.QSize(50, 16777215))
        self.ProyMax.setObjectName("ProyMax")
        self.horizontalLayout_5.addWidget(self.ProyMax)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
        self.mpl2 =  MatplotlibWidget(self.tab_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mpl2.sizePolicy().hasHeightForWidth())
        self.mpl2.setSizePolicy(sizePolicy)
        self.mpl2.setObjectName("mpl2")
        self.verticalLayout_2.addWidget(self.mpl2)
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_6 = QtWidgets.QWidget()
        self.tab_6.setObjectName("tab_6")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.tab_6)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.toolBar1_2 = QtWidgets.QWidget(self.tab_6)
        self.toolBar1_2.setMinimumSize(QtCore.QSize(25, 0))
        self.toolBar1_2.setMaximumSize(QtCore.QSize(16777215, 30))
        self.toolBar1_2.setObjectName("toolBar1_2")
        self.horizontalLayout_6.addWidget(self.toolBar1_2)
        self.label_9 = QtWidgets.QLabel(self.tab_6)
        self.label_9.setMaximumSize(QtCore.QSize(30, 16777215))
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_6.addWidget(self.label_9)
        self.ImagMin_2 = QtWidgets.QLineEdit(self.tab_6)
        self.ImagMin_2.setMaximumSize(QtCore.QSize(50, 16777215))
        self.ImagMin_2.setObjectName("ImagMin_2")
        self.horizontalLayout_6.addWidget(self.ImagMin_2)
        self.label_10 = QtWidgets.QLabel(self.tab_6)
        self.label_10.setMaximumSize(QtCore.QSize(30, 16777215))
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_6.addWidget(self.label_10)
        self.ImagMax_2 = QtWidgets.QLineEdit(self.tab_6)
        self.ImagMax_2.setMaximumSize(QtCore.QSize(50, 16777215))
        self.ImagMax_2.setObjectName("ImagMax_2")
        self.horizontalLayout_6.addWidget(self.ImagMax_2)
        self.verticalLayout_4.addLayout(self.horizontalLayout_6)
        self.mpl3 =  MatplotlibWidget(self.tab_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mpl3.sizePolicy().hasHeightForWidth())
        self.mpl3.setSizePolicy(sizePolicy)
        self.mpl3.setObjectName("mpl3")
        self.verticalLayout_4.addWidget(self.mpl3)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.accuFreeze = QtWidgets.QPushButton(self.tab_6)
        self.accuFreeze.setObjectName("accuFreeze")
        self.horizontalLayout_7.addWidget(self.accuFreeze)
        self.accuRestart = QtWidgets.QPushButton(self.tab_6)
        self.accuRestart.setObjectName("accuRestart")
        self.horizontalLayout_7.addWidget(self.accuRestart)
        self.verticalLayout_4.addLayout(self.horizontalLayout_7)
        self.tabWidget.addTab(self.tab_6, "")
        self.horizontalLayout.addWidget(self.tabWidget)
        self.tabWidget_2 = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget_2.setMaximumSize(QtCore.QSize(250, 16777215))
        self.tabWidget_2.setObjectName("tabWidget_2")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.tab_3)
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label = QtWidgets.QLabel(self.tab_3)
        self.label.setMinimumSize(QtCore.QSize(0, 18))
        self.label.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label.setObjectName("label")
        self.verticalLayout_3.addWidget(self.label)
        self.ExposureEdit = QtWidgets.QDoubleSpinBox(self.tab_3)
        self.ExposureEdit.setDecimals(3)
        self.ExposureEdit.setMinimum(0.001)
        self.ExposureEdit.setMaximum(9999.99)
        self.ExposureEdit.setObjectName("ExposureEdit")
        self.verticalLayout_3.addWidget(self.ExposureEdit)
        self.label_17 = QtWidgets.QLabel(self.tab_3)
        self.label_17.setObjectName("label_17")
        self.verticalLayout_3.addWidget(self.label_17)
        self.comboBox = QtWidgets.QComboBox(self.tab_3)
        self.comboBox.setObjectName("comboBox")
        self.verticalLayout_3.addWidget(self.comboBox)
        self.label_3 = QtWidgets.QLabel(self.tab_3)
        self.label_3.setMinimumSize(QtCore.QSize(0, 18))
        self.label_3.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_3.setObjectName("label_3")
        self.verticalLayout_3.addWidget(self.label_3)
        self.AcuEdit = QtWidgets.QSpinBox(self.tab_3)
        self.AcuEdit.setMinimumSize(QtCore.QSize(0, 20))
        self.AcuEdit.setMaximumSize(QtCore.QSize(100, 25))
        self.AcuEdit.setMinimum(0)
        self.AcuEdit.setObjectName("AcuEdit")
        self.verticalLayout_3.addWidget(self.AcuEdit)
        self.verticalLayout_7.addLayout(self.verticalLayout_3)
        self.StartButton = QtWidgets.QPushButton(self.tab_3)
        self.StartButton.setMaximumSize(QtCore.QSize(600, 16777215))
        self.StartButton.setObjectName("StartButton")
        self.verticalLayout_7.addWidget(self.StartButton)
        spacerItem = QtWidgets.QSpacerItem(20, 30, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_7.addItem(spacerItem)
        self.LockBox = QtWidgets.QCheckBox(self.tab_3)
        self.LockBox.setObjectName("LockBox")
        self.verticalLayout_7.addWidget(self.LockBox)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_12 = QtWidgets.QLabel(self.tab_3)
        self.label_12.setObjectName("label_12")
        self.horizontalLayout_4.addWidget(self.label_12)
        self.NumImgEdit = QtWidgets.QSpinBox(self.tab_3)
        self.NumImgEdit.setMaximumSize(QtCore.QSize(50, 16777215))
        self.NumImgEdit.setMinimum(1)
        self.NumImgEdit.setMaximum(200)
        self.NumImgEdit.setObjectName("NumImgEdit")
        self.horizontalLayout_4.addWidget(self.NumImgEdit)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.verticalLayout_7.addLayout(self.horizontalLayout_4)
        self.label_13 = QtWidgets.QLabel(self.tab_3)
        self.label_13.setObjectName("label_13")
        self.verticalLayout_7.addWidget(self.label_13)
        self.NameEdit = QtWidgets.QLineEdit(self.tab_3)
        self.NameEdit.setObjectName("NameEdit")
        self.verticalLayout_7.addWidget(self.NameEdit)
        self.SaveButton = QtWidgets.QPushButton(self.tab_3)
        self.SaveButton.setMaximumSize(QtCore.QSize(600, 16777215))
        self.SaveButton.setObjectName("SaveButton")
        self.verticalLayout_7.addWidget(self.SaveButton)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_7.addItem(spacerItem2)
        self.BgButton = QtWidgets.QPushButton(self.tab_3)
        self.BgButton.setObjectName("BgButton")
        self.verticalLayout_7.addWidget(self.BgButton)
        self.EntryButton = QtWidgets.QPushButton(self.tab_3)
        self.EntryButton.setObjectName("EntryButton")
        self.verticalLayout_7.addWidget(self.EntryButton)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_7.addItem(spacerItem3)
        self.tabWidget_2.addTab(self.tab_3, "")
        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setObjectName("tab_5")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.tab_5)
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.label_15 = QtWidgets.QLabel(self.tab_5)
        self.label_15.setObjectName("label_15")
        self.verticalLayout_8.addWidget(self.label_15)
        self.MemorzView = QtWidgets.QListView(self.tab_5)
        self.MemorzView.setObjectName("MemorzView")
        self.verticalLayout_8.addWidget(self.MemorzView)
        self.AddButton = QtWidgets.QPushButton(self.tab_5)
        self.AddButton.setObjectName("AddButton")
        self.verticalLayout_8.addWidget(self.AddButton)
        self.LoadButton = QtWidgets.QPushButton(self.tab_5)
        self.LoadButton.setObjectName("LoadButton")
        self.verticalLayout_8.addWidget(self.LoadButton)
        self.RemoveButton = QtWidgets.QPushButton(self.tab_5)
        self.RemoveButton.setObjectName("RemoveButton")
        self.verticalLayout_8.addWidget(self.RemoveButton)
        self.tabWidget_2.addTab(self.tab_5, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.tab_4)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.groupBox = QtWidgets.QGroupBox(self.tab_4)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_6.setSpacing(3)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setMaximumSize(QtCore.QSize(16777215, 25))
        self.label_5.setObjectName("label_5")
        self.verticalLayout_6.addWidget(self.label_5)
        self.X0Edit = QtWidgets.QLineEdit(self.groupBox)
        self.X0Edit.setMaximumSize(QtCore.QSize(16777215, 25))
        self.X0Edit.setObjectName("X0Edit")
        self.verticalLayout_6.addWidget(self.X0Edit)
        self.label_6 = QtWidgets.QLabel(self.groupBox)
        self.label_6.setMaximumSize(QtCore.QSize(16777215, 25))
        self.label_6.setObjectName("label_6")
        self.verticalLayout_6.addWidget(self.label_6)
        self.X1Edit = QtWidgets.QLineEdit(self.groupBox)
        self.X1Edit.setMaximumSize(QtCore.QSize(16777215, 25))
        self.X1Edit.setObjectName("X1Edit")
        self.verticalLayout_6.addWidget(self.X1Edit)
        self.label_7 = QtWidgets.QLabel(self.groupBox)
        self.label_7.setMaximumSize(QtCore.QSize(16777215, 25))
        self.label_7.setObjectName("label_7")
        self.verticalLayout_6.addWidget(self.label_7)
        self.Y0Edit = QtWidgets.QLineEdit(self.groupBox)
        self.Y0Edit.setMaximumSize(QtCore.QSize(16777215, 25))
        self.Y0Edit.setObjectName("Y0Edit")
        self.verticalLayout_6.addWidget(self.Y0Edit)
        self.label_8 = QtWidgets.QLabel(self.groupBox)
        self.label_8.setMaximumSize(QtCore.QSize(16777215, 25))
        self.label_8.setObjectName("label_8")
        self.verticalLayout_6.addWidget(self.label_8)
        self.Y1Edit = QtWidgets.QLineEdit(self.groupBox)
        self.Y1Edit.setObjectName("Y1Edit")
        self.verticalLayout_6.addWidget(self.Y1Edit)
        spacerItem4 = QtWidgets.QSpacerItem(20, 50, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_6.addItem(spacerItem4)
        self.SetROIButton = QtWidgets.QPushButton(self.groupBox)
        self.SetROIButton.setMaximumSize(QtCore.QSize(16777215, 25))
        self.SetROIButton.setObjectName("SetROIButton")
        self.verticalLayout_6.addWidget(self.SetROIButton)
        self.verticalLayout_5.addWidget(self.groupBox)
        self.label_11 = QtWidgets.QLabel(self.tab_4)
        self.label_11.setObjectName("label_11")
        self.verticalLayout_5.addWidget(self.label_11)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.PathEdit = QtWidgets.QLineEdit(self.tab_4)
        self.PathEdit.setObjectName("PathEdit")
        self.horizontalLayout_3.addWidget(self.PathEdit)
        self.PathButton = QtWidgets.QPushButton(self.tab_4)
        self.PathButton.setMaximumSize(QtCore.QSize(20, 16777215))
        self.PathButton.setObjectName("PathButton")
        self.horizontalLayout_3.addWidget(self.PathButton)
        self.verticalLayout_5.addLayout(self.horizontalLayout_3)
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem5)
        self.tabWidget_2.addTab(self.tab_4, "")
        self.horizontalLayout.addWidget(self.tabWidget_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 25))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget_2.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_2.setText(_translate("MainWindow", "Min:"))
        self.label_4.setText(_translate("MainWindow", "Max:"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Image"))
        self.label_14.setText(_translate("MainWindow", "Min:"))
        self.label_16.setText(_translate("MainWindow", "Max:"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Proyection"))
        self.label_9.setText(_translate("MainWindow", "Min:"))
        self.label_10.setText(_translate("MainWindow", "Max:"))
        self.accuFreeze.setText(_translate("MainWindow", "Freeze"))
        self.accuRestart.setText(_translate("MainWindow", "Restart"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_6), _translate("MainWindow", "Acum mode"))
        self.label.setText(_translate("MainWindow", "Exposure"))
        self.label_17.setText(_translate("MainWindow", "AcqMode"))
        self.label_3.setText(_translate("MainWindow", "Acumulations"))
        self.StartButton.setText(_translate("MainWindow", "StartAcq"))
        self.LockBox.setText(_translate("MainWindow", "Lockin Mode"))
        self.label_12.setText(_translate("MainWindow", "Save Images:"))
        self.label_13.setText(_translate("MainWindow", "Saving name:"))
        self.SaveButton.setText(_translate("MainWindow", "Save"))
        self.BgButton.setText(_translate("MainWindow", "Take Bg"))
        self.EntryButton.setText(_translate("MainWindow", "&Make entry"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_3), _translate("MainWindow", "Acq. Conf."))
        self.label_15.setText(_translate("MainWindow", "Saved images:"))
        self.AddButton.setText(_translate("MainWindow", "Add"))
        self.LoadButton.setText(_translate("MainWindow", "Load"))
        self.RemoveButton.setText(_translate("MainWindow", "Remove"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_5), _translate("MainWindow", "Memory"))
        self.groupBox.setTitle(_translate("MainWindow", "ROI"))
        self.label_5.setText(_translate("MainWindow", "X0:"))
        self.label_6.setText(_translate("MainWindow", "Size X:"))
        self.label_7.setText(_translate("MainWindow", "Y0:"))
        self.label_8.setText(_translate("MainWindow", "Size Y:"))
        self.SetROIButton.setText(_translate("MainWindow", "Set"))
        self.label_11.setText(_translate("MainWindow", "Saving path:"))
        self.PathButton.setText(_translate("MainWindow", "..."))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_4), _translate("MainWindow", "Others"))

from mplwidget import  MatplotlibWidget