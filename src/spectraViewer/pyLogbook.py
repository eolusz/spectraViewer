from PyQt5 import QtCore, QtGui, QtWidgets
from .logbookATAS import Ui_LogBookDialog
from .attachement import QAttachment
from .make_entry import logbook_entryLinux as logbook_entry

class LaserLogBook(Ui_LogBookDialog):
	def __init__(self, parent=None, Type="Measurement", Subject=None, attachments="None"):
		QtWidgets.QDialog.__init__(self,parent)
		self.setupUi(self)
		self.typeEdit.setText(Type)
		self.lbEntry=logbook_entry("192.168.88.248", 8080, "ATAS", "robot", "robot")
	
		if Subject is not None:
			self.subjectEdit.setText(Subject)

		self.attachmentsList=[]
		self.addButton.clicked.connect(self.getNewAttachment)

	def addAttachment(self, file_path=None):
		if file_path is None:
			return
		self.attachmentsList.append([QtWidgets.QWidget(self.attachmentBox), QAttachment()])
		self.verticalLayout_2.addWidget(self.attachmentsList[-1][0])
		self.attachmentsList[-1][-1].setupUi(self.attachmentsList[-1][0])
		self.attachmentsList[-1][-1].label.setText(file_path)
		self.attachmentsList[-1][-1].checkBox.setChecked(True)
		self.attachmentsList[-1][0].show()
		

	def getNewAttachment(self):
		fileDial=QtWidgets.QFileDialog()
		files=fileDial.getOpenFileNames(filter="*.pdf *.png *.jpg *.jpeg *.gif *.avi")
		for i in files[0]:
			self.addAttachment(i)
		


	def accept(self):
		self.lbEntry.add_field("Type", self.typeEdit.text())
		self.lbEntry.add_field("Subject", self.subjectEdit.text())
		for i in self.attachmentsList:
			self.lbEntry.add_attachment(i[1].label.text())
		self.lbEntry.add_to_comment(self.messageEdit.document().toPlainText())
		self.lbEntry.send_entry()		
		self.done(1)

	def reject(self):
		self.done(0)

		
