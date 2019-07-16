from view.mainwindow import MainWindow
from controller.productsscreen import ProductsScreenController
from controller.salescreen import SaleScreenController
from controller.customersscreen import CustomersScreenController
from controller.categoriesscreen import CategoriesScreenController
import translator

class MainWindowController(object):
	def __init__(self):
		self.view = MainWindow(self)
		self.createScreens()

	def createScreens(self):
		productController = ProductsScreenController()
		salesController = SaleScreenController()
		clientsController = CustomersScreenController()
		categoriesController = CategoriesScreenController()

		self.view.stack.addWidget(productController.view)
		self.view.stack.addWidget(salesController.view)
		self.view.stack.addWidget(clientsController.view)
		self.view.stack.addWidget(categoriesController.view)
		
	def switchScreen(self, index):
		if self.view.stack.currentIndex() == index:
			return	
		if index == 0:
			self.view.titleText.setText("Produtos")
		elif index == 1:
			self.view.titleText.setText("Vendas")
		elif index == 2:
			self.view.titleText.setText("Clientes")
		else:
			self.view.titleText.setText("Categorias")
		self.view.stack.setCurrentIndex(index)

	def run(self):
		self.view.show()