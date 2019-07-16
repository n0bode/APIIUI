from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLineEdit, QFrame, QMessageBox
from .widgets.listview import ListView
from .widgets.searchbar import SearchBar 
from .widgets.stack import Stack
import loader

class SaleScreen(QFrame):
	def __init__(self, controller, *args):
		super(SaleScreen, self).__init__(*args)
		self.controller = controller
		self._initUI()

	def _initUI(self):
		self.listview = ListView(canDelete=False)
		toolbar = self._createToolBarProduct()
		layout = QVBoxLayout()
		layout.addWidget(toolbar)
		layout.addWidget(self.listview)
		self.setLayout(layout)

	def _createToolBarProduct(self):
		bar = Stack()
		layout = QHBoxLayout()
		layout.setContentsMargins(5, 5, 5, 5)

		self.buttonAdd = loader.buttonIcon("addSales.png", 25, 25)
		self.buttonAdd.setFixedHeight(30)
		self.buttonAdd.setFixedWidth(200)
		
		self.buttonAdd.setObjectName("buttonAdd")
		self.buttonAdd.setText("Adicionar Venda")
		self.buttonAdd.setToolTip("Adicionar uma nova venda")
		
		self.searchBar = SearchBar(placeholder="buscar")
		self.searchBar.submitted.connect(self.listview.filter)

		layout.addWidget(self.buttonAdd)
		layout.addStretch()
		layout.addWidget(self.searchBar)
		bar.setLayout(layout)
		return bar