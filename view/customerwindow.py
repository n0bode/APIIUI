from PyQt5.Qt import Qt, QSize, QDate, QRegularExpression, QRegularExpressionValidator
from PyQt5.QtWidgets import QWidget, QLabel, QFrame, QLineEdit, QSpinBox, QDoubleSpinBox, QHBoxLayout, QVBoxLayout, QPushButton, QComboBox, QDateEdit
from .widgets.dialog import Dialog
import loader

class CustomerWindow(Dialog):
	def __init__(self, parent, *args):
		super(CustomerWindow, self).__init__(parent, *args)
		self.setFixedSize(400, 600)
		self._initUI()
		self.checkSuccess = self.checkSuccess

	def _initUI(self):
		self._name = QLineEdit()
		self._name.setFixedHeight(30)	
		self._name.setPlaceholderText("Nome")

		self._email = QLineEdit()
		self._email.setFixedHeight(30)
		self._email.setPlaceholderText("example@email.com")
		rg = QRegularExpression("\\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\\.[A-Z]{2,4}\\b", QRegularExpression.CaseInsensitiveOption)
		self._email.setValidator(QRegularExpressionValidator(rg, self))

		self._phone = QLineEdit()
		self._phone.setFixedHeight(30)
		self._phone.setPlaceholderText("(55) 9999-9999")
		rg = QRegularExpression("^((\\+?(\\d{2}))\\s?)?((\\d{2})|(\\((\\d{2})\\))\\s?)?(\\d{3,15})(\\-(\\d{3,15}))?$", QRegularExpression.CaseInsensitiveOption)
		self._phone.setValidator(QRegularExpressionValidator(rg, self))

		self.addField("Nome do Cliente", self._name)
		self.addField("Email", self._email)
		self.addField("Telefone", self._phone)
		super(CustomerWindow, self)._initUI()

	def name(self):
		return self._name.text()

	def email(self):
		return self._email.text()

	def phone(self):
		return self._phone.text()

	def clear(self):
		self._name.clear()
		self._email.clear()
		self._phone.clear()
		self._email.parent().setProperty("hint", False)
		self._phone.parent().setProperty("hint", False)
		self._name.parent().setProperty("hint", False)
		self.update()

	def setData(self, data):
		self._name.setText(data.name)
		self._email.setText(data.email)
		self._phone.setText(str(data.phone))

	def checkSuccess(self):
		success = True
		if self._email.hasAcceptableInput():
			self._email.parent().setProperty("hint", False)
		else:
			self._email.parent().setProperty("hint", True)
			success = False

		if len(self._name.text()) > 0:
			self._name.parent().setProperty("hint", False)
		else:
			self._name.parent().setProperty("hint", True)
			success = False

		if len(self._phone.text()) > 0:
			self._phone.parent().setProperty("hint", False)
		else:
			self._phone.parent().setProperty("hint", True)
			success = False
		return success