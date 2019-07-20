from view.salewindow import SaleWindow
from view.selectproductwindow import SelectProductWindow
from .restthread import RestThread
from model.product import Product
from model.customer import Customer
from model.saleitem import SaleItem
from PyQt5.QtWidgets import QMessageBox
from view.saleitemwidget import SaleItemWidget
import requests

class SaleWindowController:
	def __init__(self, parent):
		self.view = SaleWindow(parent.view)
		self.view.products.onDeleteItem.connect(self.remCart)
		self.window = SelectProductWindow(self.view)
		self.window.setTitle("Adicionando ao carrinho")
		self.parent = parent
		self._products = []
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
		arr = []
		for i in range(1, self.view.products.count()):
			saleItem = self.view.products.itemWidget(self.view.products.item(i)).data
			if saleItem.quantity > 0:
				arr.append(saleItem.__dict__)
		return arr

	def getCustomer(self):
		self.view.customers.setEnabled(False)
		self.view.customers.clear()
		try:
			r = requests.get("http://localhost:8080/api/v1/customers")
			if r.status_code == 200:
				self._customers = [Customer(**data) for data in r.json()]
				self.view.customers.addItems([customer.name for customer in self._customers])
		except Exception as e:
			print("Error to get customers in Sale Window", e)
		self.view.customers.setEnabled(True)

	def getProduct(self):
		self.window.products.setEnabled(False)
		self.window.products.clear()
		try:
			r = requests.get("http://localhost:8080/api/v1/products/inStock")
			if r.status_code == 200:
				for data in r.json():
					product = Product(**data)
					self.addProduct(product)
					self._products.append(product)
			self.window.products.setEnabled(True)
		except Exception as e:
			print("Error to get products in Sale Window", e)

	def getProductById(self, id):
		for product in self._products:
			if product.id == id:
				return product
		return None

	def getItemsCart(self):
		self.getProduct()
		self.view.products.setEnabled(False)
		self.view.products.clear()
		r = requests.get("http://localhost:8080/api/v1/sales/items/{}".format(self.saleID))
		if r.status_code == 200:
			for data in r.json():
				item = SaleItem(**data)
				pro = self.getProductById(item.productId)
				self.addCart(pro, item.quantity, False, False)
		self.view.products.setEnabled(True)
		self.view.show()
		self.updateGross()

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

	def onAddToCart(self, product):
		self.addCart(product, 1)
		self.hideProductList(product.id, True)

	def addCart(self, product, quantity, canEdit=True, canDelete=True): 
		model = self.createModelCart(product.id, product.name, product.price, "")
		widget = SaleItemWidget(self.view.products, None, SaleItem(0, 0, product.id, quantity), model, canEdit=canEdit, canDelete=canDelete)
		widget.inputQtds.setValue(quantity)
		widget.valueChanged.connect(self.onValueChangedItemCart)
		
		self.view.products.addWidget(widget)
		self.updateGross()

	def remCart(self, item):
		saleItem = self.view.products.itemWidget(item).data
		self.view.products.deleteItem(item)
		self.hideProductList(saleItem.productId, False)
		self.updateGross()

	def onValueChangedItemCart(self, item, value):
		widget = self.view.products.itemWidget(item)
		saleItem = widget.data
		product = self.getProductById(saleItem.productId)
		if product.stock < value:
			widget.inputQtds.setValue(product.stock)
			saleItem.quantity = product.stock
		else:
			saleItem.quantity = value
		self.updateGross()
		

	def hideProductList(self, id, hidden):
		for i in range(1, self.window.products.count()):
			item = self.window.products.item(i)
			widget = self.window.products.itemWidget(item)
			if widget.data.id == id:
				item.setHidden(hidden)


	def existInCart(self, product):
		for i in range(1, self.view.products.count()):
			saleItem = self.view.products.itemWidget(self.view.products.item(i)).data
			if saleItem.productId == product.id:
				return True
		return False

	def createHeaderCart(self):
		header = self.createModelCart("ID", "Nome", "Preço (R$)", "Quantidade")
		self.view.products.createHeader(header)

	def createModelCart(self, id, name, price, qts):
		return [
			{"text":id, "width":50},
			{"text":name},
			{"text":price, "width":100},
			{"text":qts, "width":150},
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

	def updateGross(self):
		self.view.grossText.setText("Valor Total: {:.2f} R$".format(self.getGross()))

	def addSale(self, widget):
		pass
	
	def getGross(self):
		gross = 0
		for i in range(1, self.view.products.count()):
			sale = self.view.products.itemWidget(self.view.products.item(i)).data
			for product in self._products:
				if sale.productId == product.id:
					gross += product.price * sale.quantity
		return gross

	def showAddProductWindow(self):
		self.window.show()
		self.window.products.setCurrentRow(0)
		self.window.searchBar.clear()
		self.window.onSuccess = self.onAddToCart
		#self.updateProduct()

	def customerId(self):
		return self._customers[self.view.customers.currentIndex()].id

	def listProducts(self):
		return self._cart

	def setData(self, sale):
		self.sale = sale
		#self.view.customers.addItem(s)

	def checkSuccess(self):
		if self.view.products.count() < 1:
			QMessageBox.about(self.view, "Adicionar Produto", "Precisa adicionar um produto")
			return False
		return True
