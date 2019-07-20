from view.mainwindow import MainWindow
from controller.productsscreen import ProductsScreenController
from controller.salescreen import SaleScreenController
from controller.customersscreen import CustomersScreenController
from controller.categoriesscreen import CategoriesScreenController
import translator

class MainWindowController(object):
	def __init__(self):
		self.view = MainWindow()
		self.createScreens()

	def createScreens(self):
		self.productController = ProductsScreenController()
		self.salesController = SaleScreenController()
		self.clientsController = CustomersScreenController()
		self.categoriesController = CategoriesScreenController()

		self.view.sellsBtn.clicked.connect(lambda: self.switchScreen(0))
		self.view.productBtn.clicked.connect(lambda: self.switchScreen(1))
		self.view.clientBtn.clicked.connect(lambda: self.switchScreen(2))
		self.view.tagBtn.clicked.connect(lambda: self.switchScreen(3))

		self.view.stack.addWidget(self.salesController.view)
		self.view.stack.addWidget(self.productController.view)
		self.view.stack.addWidget(self.clientsController.view)
		self.view.stack.addWidget(self.categoriesController.view)
		
	def switchScreen(self, index):
		if self.view.stack.currentIndex() == index:
			return	
		if index == 0:
			self.view.titleText.setText("Vendas")
		elif index == 1:
			self.view.titleText.setText("Produtos")
			self.productController.updateProduct()
		elif index == 2:
			self.view.titleText.setText("Clientes")
		else:
			self.view.titleText.setText("Categorias")
		self.view.stack.setCurrentIndex(index)

	def run(self):
		self.view.show()