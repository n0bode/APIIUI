from PyQt5.Qt import Qt, QSize, QDate
from PyQt5.QtWidgets import QWidget, QLabel, QFrame, QLineEdit, QSpinBox, QDoubleSpinBox, QHBoxLayout, QListView, QVBoxLayout, QPushButton, QComboBox, QDateEdit
from .widgets.dialog import Dialog
from .widgets.listview import ListView
import loader

class SaleWindow(Dialog):
	def __init__(self, parent, *args):
		super(SaleWindow, self).__init__(parent, *args)
		self.setFixedSize(600, 600)
		self._initUI()
		self._listProducts = []
		
	def _initUI(self):
		self.customers = QComboBox()
		self.customers.setFixedHeight(30)		
		self.customers.addItems(["asd", "sad"])
		self.products = ListView()
		self.products.setFixedHeight(300)

		self.label = QLabel("Valor total: 0 R$")
		self.buttonAddProduct = QPushButton("Adicionar um Produto")
		self.buttonAddProduct.setFixedHeight(30)

		self.addField("Nome do Cliente", self.customers)
		self.addField("Produtos", self.products)
		self.products.parent().layout().addWidget(self.label)
		self.products.parent().layout().addWidget(self.buttonAddProduct)
		super(SaleWindow, self)._initUI()

	def customerId(self):
		return self.customers.currentIndex()

	def listProducts(self):
		return self._listProducts

	def clear(self):
		self._listProducts = []

	def date(self):
		return self._date.date().toString("dd/MM/yyyy")

	def setData(self, data):
		self._name.setText(data.name)