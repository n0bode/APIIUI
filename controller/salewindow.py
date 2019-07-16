from view.salewindow import SaleWindow
from view.selectproductwindow import SelectProductWindow
from .restthread import RestThread
import requests

class SaleWindowController:
	def __init__(self, parent):
		self.view = SaleWindow(parent.view)
		self.window = SelectProductWindow(self.view)
		self.parent = parent
		self.createHeaderProducts()
		self.view.buttonAddProduct.clicked.connect(self.showAddProductWindow)

	def getCustomer(self):
		self.view.customers.setEnabled(False)
		self.view.customers.clear()
		try:
			r = requests.get("http://localhost:8080/customer")
			if r.status_code == 200:
				for data in r.json():
					print(data["name"])
					self.view.customers.addItem(data["name"])
		except Exception as e:
			print(e)
			pass
		self.view.customers.setEnabled(True)

	def getProduct(self):
		self.window.products.setEnabled(False)
		self.window.products.clear()
		try:
			r = requests.get("http://localhost:8080/product")
			if r.status_code == 200:
				for data in r.json():
					self.window.products.addItem(data["name"])
		except Exception as e:
			print(e)
			pass
		self.window.products.setEnabled(True)

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
		pass
		
	def showAddProductWindow(self):
		self.window.clear()
		self.window.show()
		self.window.onSuccess = self.addSale
		self.updateProduct()
