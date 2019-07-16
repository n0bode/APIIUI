from view.salesscreen import SaleScreen
from controller.salewindow import SaleWindowController
from .restthread import RestThread

class SaleScreenController(object):
	def __init__(self):
		self.view = SaleScreen(self)
		self.thread = RestThread(self.view)
		self.thread.update.connect(self.getProduct)
		self.thread.start()

		#Set Callback
		self.view.listview.onDeleteItem.connect(self.showDeleteAlert)
		self.view.listview.onEditItem.connect(self.showEditItem)
		self.view.listview.onFilter = self.filterItems
		self.view.buttonAdd.clicked.connect(self.showAddItem)

		self.window = SaleWindowController(self)
		self.createHeader()

	def addSale(self, sale):
		model = self.createModelItem(
			sale.id, 
			sale.customerId,
			sale.amountPaid, 
		)
		self.view.listview.createItem(product, model)

	def createHeader(self):
		header = self.createModelItem("ID", "Cliente", "Preço (R$)")
		self.view.listview.createHeader(header)

	def filterItems(self, data, pattern):
		return data.name.lower().startswith(pattern.lower())

	def getProduct(self):
		self.view.listview.setEnabled(False)
		self.view.listview.clear()
		try:
			r = requests.get("http://localhost:5050/product")
			if r.status_code == 200:
				for data in r.json():
					print(data)
					self.addProduct(Product(**data))
		except:
			pass
		self.view.listview.setEnabled(True)

	def postProduct(self, item):
		data = Sale(
			0,
			self.window.customerId(),
			cart=self.window.listProduct()
		)
		r = requests.post("http://localhost:5050/sale", data=data.toJson())
		print(r.status_code)
		if r.status_code == 200:
			self.addProduct(Product(**r.json()))

	def deleteProduct(self, item):
		self.view.listview.setEnabled(False)
		data = self.view.listview.itemWidget(item).data
		r = requests.delete("http://localhost:5050/product/{}".format(data.id))
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

		r = requests.put("http://localhost:5050/product/{}".format(data.id), data=data.toJson())
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
		self.window.view.onSuccess = self.onAddNewItem
		self.window.view.clear()		
		self.window.updateCustomer()
		self.window.view.setTitle("Adicionando Produto")
		self.window.view.show()

	def showEditItem(self, item):
		product = self.view.listview.itemWidget(item).data
		self.window.view.clear()	
		self.window.view.setData(product)
		self.window.view.setTitle("Editando um Produto")
		self.window.view.onSuccess = self.onEditItem
		self.window.view.setCurrentItem(item)	
		self.window.view.show()

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

	def createModelItem(self, id, customer, amountPaid):
		return [
			{"text":id, "width":50},
			{"text":customer},
			{"text":amountPaid},
		]