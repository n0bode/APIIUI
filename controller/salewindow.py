from view.salewindow import SaleWindow
from view.selectproductwindow import SelectProductWindow
from .restthread import RestThread
import requests

class SaleWindowController:
	def __init__(self, parent):
		self.view = SaleWindow(parent.view)
		self.view.products.onDeleteItem.connect(self.remCart)
		self.window = SelectProductWindow(self.view)
		self.parent = parent
		self._gross = 0
		self._cart = []
		self.createHeaderProducts()
		self.view.buttonAddProduct.clicked.connect(self.showAddProductWindow)

	def getCustomer(self):
		self.view.customers.setEnabled(False)
		self.view.customers.clear()
		try:
			r = requests.get("http://localhost:8080/api/v1/customers")
			if r.status_code == 200:
				for data in r.json():
					print(data["name"])
					self.view.customers.addItem(data["name"])
		except Exception as e:
			print(e)
		self.view.customers.setEnabled(True)

	def getProduct(self):
		self.window.products.setEnabled(False)
		self.window.products.clear()
		try:
			r = requests.get("http://localhost:8080/api/v1/products")
			if r.status_code == 200:
				for data in r.json():
					self.addProduct(data)
		except Exception as e:
			print(e)
			pass
		self.window.products.setEnabled(True)

	def addProduct(self, data):
		model = self.createModelProduct(data["id"], data["name"], data["price"])
		self.window.products.createItem(data, model)

	def updateGross(self):
		self.view.label.setText("Valor Total: {} R$".format(self._gross))

	def addCart(self, data):
		model = self.createModelProduct(data["id"], data["name"], data["price"])
		self.view.products.createItem(data, model)
		self._cart.append(data)
		self._gross += float(data["price"])
		self.updateGross()

	def remCart(self, item):
		data = self.view.products.itemWidget(item).data
		self.view.products.deleteItem(item)
		self._gross -= float(data["price"])
		self.updateGross()

	def createHeaderProducts(self):
		header = self.createModelProduct("ID", "Nome", "Preço (R$)")
		self.view.products.createHeader(header)
		self.window.products.createHeader(header)

	def createModelProduct(self, id, name, price):
		return [
			{"text":id, "width":50},
			{"text":name},
			{"text":price},
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
	
	def showAddProductWindow(self):
		self.window.clear()
		self.window.show()
		self.window.onSuccess = self.addCart
		self.updateProduct()

	def customerId(self):
		return self.customers.currentIndex()

	def listProducts(self):
		return self._cart
