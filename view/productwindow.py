from PyQt5.Qt import Qt, QSize, QDate
from PyQt5.QtWidgets import QWidget, QLabel, QFrame, QLineEdit, QSpinBox, QDoubleSpinBox, QHBoxLayout, QVBoxLayout, QPushButton, QComboBox, QDateEdit, QMessageBox
from .widgets.dialog import Dialog
import requests
import loader

class ProductWindow(Dialog):
	def __init__(self, parent, *args):
		super(ProductWindow, self).__init__(parent, *args)
		self.setFixedSize(400, 600)
		self._initUI()

	def _initUI(self):
		self._name = QLineEdit()
		self._name.setFixedHeight(30)
		self._name.setPlaceholderText("Pirulito Pop")		
		
		self._stock = QSpinBox()
		self._stock.setMaximum(100000)
		self._stock.setFixedHeight(30)
		self._stock.setValue(10)
		
		self._price = QDoubleSpinBox()
		self._price.setDecimals(2)
		self._price.setMaximum(99999.99)
		self._price.setFixedHeight(30)
		self._price.setValue(10)

		self.inputCategory = QComboBox()
		self.inputCategory.setFixedHeight(30)
		
		self._date = QDateEdit()
		self._date.setDate(QDate.currentDate())

		self.addField("Nome do Produto", self._name)
		self.addField("Preço(R$)", self._price)
		self.addField("Estoque(Unidade)", self._stock)
		self.addField("Categoria", self.inputCategory)
		self.addField("Validade", self._date)
		super(ProductWindow, self)._initUI()

	def name(self):
		return self._name.text()

	def price(self):
		return self._price.value()

	def stock(self):
		return self._stock.value()

	def clear(self):
		self._name.clear()
		self._price.setValue(0)
		self._stock.setValue(0)
		self.inputCategory.setCurrentIndex(0)
		self._date.setDate(QDate.currentDate())
		self._name.parent().setProperty("hint", False)
		self.inputCategory.parent().setProperty("hint", False)
		self.update()

	def category(self):
		return self.inputCategory.currentIndex()

	def date(self):
		return self._date.date().toString("dd/MM/yyyy")

	def setData(self, data):
		self._name.setText(data.name)
		self._price.setValue(data.price)
		self._stock.setValue(data.stock)
		

	def show(self):
		super(ProductWindow, self).show()

	def checkSuccess(self):
		if len(self._name.text()) == 0:
			self._name.parent().setProperty("hint", True)
			return False
			
		if self.inputCategory.count() == 0:
			self.inputCategory.parent().setProperty("hint", True)
			QMessageBox.warning(self, "Falta campo", "Adicione um categoria antes", QMessageBox.Ok)
			return False
		return True