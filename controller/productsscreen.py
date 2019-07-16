from view.productsscreen import ProductsScreen
from view.productwindow import ProductWindow
from model.product import Product
from PyQt5.QtWidgets import QMessageBox
from .restthread import RestThread
import requests

class ProductsScreenController(object):
	def __init__(self):
		self.view = ProductsScreen(self)
		self.thread = RestThread(self.view)
		self.thread.update.connect(self.getProduct)
		self.thread.start()

		#Set Callback
		self.view.listview.onDeleteItem.connect(self.showDeleteAlert)
		self.view.listview.onEditItem.connect(self.showEditItem)
		self.view.listview.onFilter = self.filterItems

		self.window = ProductWindow(self.view)
		self.createHeader()

	def addProduct(self, product):
		model = self.createModelItem(
			product.id, 
			product.name,
			product.categoryId, 
			product.price, 
			product.stock, 
		)
		self.view.listview.createItem(product, model)

	def createHeader(self):
		header = self.createModelItem("ID", "Nome", "Categoria", "Preço (R$)", "Estoque")
		self.view.listview.createHeader(header)

	def filterItems(self, data, pattern):
		return data.name.lower().startswith(pattern.lower())

	def getProduct(self):
		self.view.listview.setEnabled(False)
		self.view.listview.clear()
		try:
			r = requests.get("http://localhost:8080/api/v1/products")
			if r.status_code == 200:
				for data in r.json():
					print(data)
					self.addProduct(Product(**data))
		except:
			pass
		self.view.listview.setEnabled(True)

	def getCategory(self):
		self.window.inputCategory.setEnabled(False)
		self.window.inputCategory.clear()
		r = requests.get("http://localhost:8080/api/v1/categories")
		if r.status_code == 200:
			arr = [x["name"] for x in r.json()]
			self.window.inputCategory.addItems(arr)
			self.window.inputCategory.setEnabled(True)

	def postProduct(self, item):
		data = Product(
			0,
			self.window.name(),
			self.window.category(),
			self.window.price(),
			self.window.stock(),
		)
		r = requests.post("http://localhost:8080/api/v1/products", data=data.toJson())
		print(r.text)
		print(r.status_code)
		if r.status_code == 200:
			self.addProduct(Product(**r.json()))

	def deleteProduct(self, item):
		self.view.listview.setEnabled(False)
		data = self.view.listview.itemWidget(item).data
		r = requests.delete("http://localhost:8080/api/v1/products/{}".format(data.id))
		if r.status_code == 200:
			self.view.listview.deleteItem(item)
		self.view.listview.setEnabled(True)

	def putProduct(self, item):
		self.view.listview.setEnabled(False)
		data = Product(
			self.view.listview.itemWidget(item).data.id,
			self.window.name(),
			self.window.category(),
			self.window.price(),
			self.window.stock(),
		)

		r = requests.put("http://localhost:8080/api/v1/products/{}".format(data.id), data=data.toJson())
		print(r.text)
		if r.status_code == 200:
			data = Product(**r.json())
			model = self.createModelItem(
				data.id, 
				data.name, 
				self.window.inputCategory.currentText(), 
				data.price, 
				data.stock, 
			)
			widget = self.view.listview.createWidget(item, data, model)
			self.view.listview.setItemWidget(item, widget)
		self.view.listview.setEnabled(True)

	def showAddItem(self):
		self.window.onSuccess = self.onAddNewItem
		self.window.clear()		
		self.window.setTitle("Adicionando Produto")
		self.getCategory()
		self.window.show()

	def showEditItem(self, item):
		product = self.view.listview.itemWidget(item).data
		self.window.clear()	
		self.window.setData(product)
		self.window.setTitle("Editando um Produto")
		self.window.onSuccess = self.onEditItem
		self.window.setCurrentItem(item)		
		self.window.show()

	def onAddNewItem(self, item):
		postThread = RestThread(self.view, data=item)
		postThread.update.connect(self.postProduct)
		postThread.start()

	def onEditItem(self, item):
		putThread = RestThread(self.view, item)
		putThread.update.connect(self.putProduct)
		putThread.start()

	def showDeleteAlert(self, item):
		result = QMessageBox.warning(self.view, "Apagar Produto", "Deseja apagar esse Produto?", QMessageBox.Ok | QMessageBox.Cancel)
		if result == QMessageBox.Ok:
			deleteThread = RestThread(self.view, item)
			deleteThread.update.connect(self.deleteProduct)
			deleteThread.start()

	def createModelItem(self, id, name, category, price, stock):
		return [
			{"text":id, "width":50},
			{"text":name},
			{"text":category},
			{"text":price, "width":100},
			{"text":stock, "width":115},
		]