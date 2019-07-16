from PyQt5.Qt import Qt, QSize, QDate, QSizePolicy
from PyQt5.QtWidgets import QWidget, QLabel, QFrame, QLineEdit, QSpinBox, QDoubleSpinBox, QHBoxLayout, QVBoxLayout, QPushButton, QComboBox, QDateEdit
from .widgets.dialog import Dialog
from .widgets.listview import ListView
from .widgets.searchbar import SearchBar
import loader

class SelectProductWindow(Dialog):
	def __init__(self, parent, *args):
		super(SelectProductWindow, self).__init__(parent, *args)
		self.setFixedSize(500, 700)
		self.setWindowTitle("Selecione um produto")
		self._initUI()

	def _initUI(self):
		self.products = ListView(canEdit=False, canDelete=False)	
		self.products.setFixedHeight(450)
		
		self.searchBar = SearchBar()
		self.searchBar.setPlaceHolder("Nome")
		self.searchBar.submitted.connect(self.products.filter)

		self.addWidget(self.searchBar)
		self.addField("Produtos", self.products)
		super(SelectProductWindow, self)._initUI()
		
	def getProduct(self):
		item = self.products.item(self.products.currentRow())
		widget = self.products.itemWidget(item)
		return widget.data

	def clear(self):
		self.products.clear()
		self.update()

	def setData(self, data):
		pass

	def checkSuccess(self):
		self.setCurrentItem(self.getProduct())
		return True