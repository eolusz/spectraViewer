# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class QAttachment(object):
    def setupUi(self, Widget):
        Widget.setObjectName("Widgetn")
        Widget.resize(476, 275)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Widget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(Widget)
        self.label.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.checkBox = QtWidgets.QCheckBox(Widget)
        self.checkBox.setMaximumSize(QtCore.QSize(80, 16777215))
        self.checkBox.setObjectName("checkBox")
        self.horizontalLayout.addWidget(self.checkBox)
        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.retranslateUi(Widget)
        QtCore.QMetaObject.connectSlotsByName(Widget)

    def retranslateUi(self, Widget):
        _translate = QtCore.QCoreApplication.translate
        self.label.setText(_translate("Widget", "/media/atto/asadsd/asdas"))
        self.checkBox.setText(_translate("Widget", "Attach"))

