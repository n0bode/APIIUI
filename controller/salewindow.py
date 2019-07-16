from view.salewindow import SaleWindow
from view.selectproductwindow import SelectProductWindow
from .restthread import RestThread
from model.product import Product
from model.customer import Customer
from model.saleitem import SaleItem
from PyQt5.QtWidgets import QMessageBox
import requests

class SaleWindowController:
	def __init__(self, parent):
		self.view = SaleWindow(parent.view)
		self.view.products.onDeleteItem.connect(self.remCart)
		self.window = SelectProductWindow(self.view)
		self.window.setTitle("Adicionando ao carrinho")
		self.parent = parent
		self._cart = []
		self._customers = []
		self.saleID = 0
		self.createHeaderProducts()
		self.createHeaderCart()

		self.view.checkSuccess = self.checkSuccess
		self.view.buttonAddProduct.clicked.connect(self.showAddProductWindow)
		self.window.products.onFilter = self.filterItems
		

	def filterItems(self, data, pattern):
		return data.name.lower().startswith(pattern.lower())

	def getCart(self):
		return list(map(lambda p: SaleItem(0, 0, p.id, 1).__dict__, self._cart))

	def getCustomer(self):
		self.view.customers.setEnabled(False)
		self.view.customers.clear()
		try:
			r = requests.get("http://localhost:8080/api/v1/customers")
			if r.status_code == 200:
				self._customers = [Customer(**data) for data in r.json()]
				self.view.customers.addItems([customer.name for customer in self._customers])
		except Exception as e:
			print(e)
		self.view.customers.setEnabled(True)

	def getProduct(self):
		self.window.products.setEnabled(False)
		self.window.products.clear()
		r = requests.get("http://localhost:8080/api/v1/products/inStock")
		if r.status_code == 200:
			for data in r.json():
				self.addProduct(Product(**data))
		self.window.products.setEnabled(True)

	def getProductById(self, id):
		r = requests.get("http://localhost:8080/api/v1/products/{}".format(id))
		if r.status_code == 200:
			item = Product(**r.json())
			return item
		return None

	def getItemsCart(self):
		self.view.products.setEnabled(False)
		self.view.products.clear()
		r = requests.get("http://localhost:8080/api/v1/sales/items/{}".format(self.saleID))
		if r.status_code == 200:
			for data in r.json():
				item = SaleItem(**data)
				pro = self.getProductById(item.productId)
				self.addCart(pro)
		self.view.products.setEnabled(True)
		self.view.show()

		for i in range(len(self._customers)):
			if self._customers[i].id == self.sale.customerId:
				self.view.customers.setCurrentIndex(i)

	def getItems(self, id):
		self.saleID = id
		self.view.buttonAddProduct.setHidden(True)
		self.view.products.canDelete = False
		thread = RestThread(self.view)
		thread.update.connect(self.getItemsCart)
		thread.start()

	def addProduct(self, product):
		model = self.createModelProduct(product.id, product.name, product.price, product.stock)
		self.window.products.createItem(product, model)

	def updateGross(self):
		self.view.grossText.setText("Valor Total: {:.2f} R$".format(self.getGross()))

	def addCart(self, product):
		model = self.createModelCart(product.id, product.name, product.price)
		self.view.products.createItem(product, model)
		self._cart.append(product)
		self.updateGross()

	def remCart(self, item):
		product = self.view.products.itemWidget(item).data
		self.view.products.deleteItem(item)
		self.updateGross()

	def createHeaderCart(self):
		header = self.createModelCart("ID", "Nome", "Preço (R$)")
		self.view.products.createHeader(header)

	def createModelCart(self, id, name, price):
		return [
			{"text":id, "width":50},
			{"text":name},
			{"text":price, "width":100},
		]

	def createHeaderProducts(self):
		header = self.createModelProduct("ID", "Nome", "Preço (R$)", "Estoque")
		self.window.products.createHeader(header)

	def createModelProduct(self, id, name, price, stock):
		return [
			{"text":id, "width":50},
			{"text":name},
			{"text":price, "width":100},
			{"text":stock, "width":100},
		]

	def updateCustomer(self):
		thread = RestThread(self.view)
		thread.update.connect(self.getCustomer)
		thread.start()

	def updateProduct(self):
		thread = RestThread(self.view)
		thread.update.connect(self.getProduct)
		thread.start()

	def addSale(self, widget):
		print(widget)
	
	def getGross(self):
		return sum([c.price for c in self._cart])

	def showAddProductWindow(self):
		self.window.clear()
		self.window.show()
		self.window.onSuccess = self.addCart
		self.updateProduct()

	def customerId(self):
		return self._customers[self.view.customers.currentIndex()].id

	def listProducts(self):
		return self._cart

	def setData(self, sale):
		self.sale = sale
		self.updateGross()
		#self.view.customers.addItem(s)

	def checkSuccess(self):
		if len(self._cart) == 0:
			QMessageBox.about(self.view, "Adicionar Produto", "Precisa adicionar um produto")
			return False
		return True
