from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLineEdit, QFrame, QMessageBox
from PyQt5.Qt import QSizePolicy
from .widgets.listview import ListView
from .widgets.searchbar import SearchBar
from .widgets.stack import Stack
import loader

class CustomersScreen(QFrame):
	def __init__(self, controller, *args):
		super(CustomersScreen, self).__init__(*args)
		self.controller = controller
		self._initUI()
		
	def _initUI(self):
		self.listview = ListView()
		toolbar = self._createToolBarProduct()
		layout = QVBoxLayout()
		layout.addWidget(toolbar)
		layout.addWidget(self.listview)
		self.setLayout(layout)

	def _createToolBarProduct(self):
		bar = Stack()
		layout = QHBoxLayout()
		layout.setContentsMargins(5, 5, 5, 5)

		self.buttonAdd = loader.buttonIcon("addClient.png", 20, 20)
		self.buttonAdd.setFixedHeight(30)
		self.buttonAdd.setFixedWidth(200)

		self.buttonAdd.setObjectName("buttonAdd")
		self.buttonAdd.setText("Adicionar um Cliente")
		self.buttonAdd.setToolTip("Adicionar um novo Cliente")
		self.buttonAdd.clicked.connect(self.controller.showAddItem)
			
		self.searchBar = SearchBar(placeholder="buscar")
		self.searchBar.submitted.connect(self.listview.filter)

		layout.addWidget(self.buttonAdd)
		layout.addStretch()
		layout.addWidget(self.searchBar)
		bar.setLayout(layout)
		return bar