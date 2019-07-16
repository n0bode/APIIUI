from PyQt5.Qt import Qt, QSize, QDate
from PyQt5.QtWidgets import QWidget, QLabel, QFrame, QLineEdit, QSpinBox, QDoubleSpinBox, QHBoxLayout, QVBoxLayout, QPushButton, QComboBox, QDateEdit
from .widgets.dialog import Dialog
import loader

class CategoryWindow(Dialog):
	def __init__(self, parent, *args):
		super(CategoryWindow, self).__init__(parent, *args)
		self.setFixedSize(400, 600)
		self._initUI()

	def _initUI(self):
		self.inputName = QLineEdit()
		self.inputName.setFixedHeight(30)		
	
		self.addField("Nome da Categoria", self.inputName)
		super(CategoryWindow, self)._initUI()

	def name(self):
		return self.inputName.text()

	def clear(self):
		self.inputName.clear()
		self.inputName.parent().setProperty("hint", False)
		self.update()

	def setData(self, data):
		self.inputName.setText(data.name)

	def checkSuccess(self):
		if len(self.inputName.text()) > 0:
			return True
		self.inputName.parent().setProperty("hint", True)
		print(self.inputName.parent().property("hint"))
		self.update()
		return False