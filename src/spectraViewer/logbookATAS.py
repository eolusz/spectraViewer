# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'logbookATAS.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_LogBookDialog(QtWidgets.QDialog):
    def setupUi(self, LogBookDialog):
        LogBookDialog.setObjectName("LogBookDialog")
        LogBookDialog.resize(636, 718)
        self.verticalLayout = QtWidgets.QVBoxLayout(LogBookDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(LogBookDialog)
        self.label.setMinimumSize(QtCore.QSize(52, 0))
        self.label.setMaximumSize(QtCore.QSize(300, 16777215))
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.typeEdit = QtWidgets.QLineEdit(LogBookDialog)
        self.typeEdit.setMaximumSize(QtCore.QSize(500, 16777215))
        self.typeEdit.setObjectName("typeEdit")
        self.horizontalLayout.addWidget(self.typeEdit)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_3 = QtWidgets.QLabel(LogBookDialog)
        self.label_3.setMinimumSize(QtCore.QSize(52, 0))
        self.label_3.setMaximumSize(QtCore.QSize(52, 16777215))
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.subjectEdit = QtWidgets.QLineEdit(LogBookDialog)
        self.subjectEdit.setMaximumSize(QtCore.QSize(500, 16777215))
        self.subjectEdit.setObjectName("subjectEdit")
        self.horizontalLayout_2.addWidget(self.subjectEdit)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.label_2 = QtWidgets.QLabel(LogBookDialog)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.messageEdit = QtWidgets.QPlainTextEdit(LogBookDialog)
        self.messageEdit.setObjectName("messageEdit")
        self.verticalLayout.addWidget(self.messageEdit)
        self.attachmentBox = QtWidgets.QGroupBox(LogBookDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.attachmentBox.sizePolicy().hasHeightForWidth())
        self.attachmentBox.setSizePolicy(sizePolicy)
        self.attachmentBox.setMinimumSize(QtCore.QSize(0, 80))
        self.attachmentBox.setFlat(False)
        self.attachmentBox.setCheckable(True)
        self.attachmentBox.setObjectName("attachmentBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.attachmentBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout.addWidget(self.attachmentBox)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.addButton = QtWidgets.QPushButton(LogBookDialog)
        self.addButton.setObjectName("addButton")
        self.horizontalLayout_5.addWidget(self.addButton)
        self.buttonBox = QtWidgets.QDialogButtonBox(LogBookDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout_5.addWidget(self.buttonBox)
        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.retranslateUi(LogBookDialog)
        self.buttonBox.accepted.connect(LogBookDialog.accept)
        self.buttonBox.rejected.connect(LogBookDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(LogBookDialog)

    def retranslateUi(self, LogBookDialog):
        _translate = QtCore.QCoreApplication.translate
        LogBookDialog.setWindowTitle(_translate("LogBookDialog", "ATAS Logbook"))
        self.label.setText(_translate("LogBookDialog", "Type:"))
        self.label_3.setText(_translate("LogBookDialog", "Subject:"))
        self.label_2.setText(_translate("LogBookDialog", "Message:"))
        self.attachmentBox.setTitle(_translate("LogBookDialog", "Attachments:"))
        self.addButton.setText(_translate("LogBookDialog", "&Add"))

