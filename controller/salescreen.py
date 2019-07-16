from view.salesscreen import SaleScreen
from model.sale import Sale
from controller.salewindow import SaleWindowController
from .restthread import RestThread

class SaleScreenController(object):
	def __init__(self):
		self.view = SaleScreen(self)
		self.thread = RestThread(self.view)
		self.thread.update.connect(self.getSale)
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
			sale.grossAmount, 
		)
		self.view.listview.createItem(product, model)

	def createHeader(self):
		header = self.createModelItem("ID", "Cliente", "Preço (R$)")
		self.view.listview.createHeader(header)

	def filterItems(self, data, pattern):
		return data.name.lower().startswith(pattern.lower())

	def getSale(self):
		self.view.listview.setEnabled(False)
		self.view.listview.clear()
		try:
			r = requests.get("http://localhost:8080/api/v1/sales")
			if r.status_code == 200:
				for data in r.json():
					self.addSale(Sale(**data))
		except:
			pass
		self.view.listview.setEnabled(True)
		
		# TERMINAR ESSA PARTE QUANDO ACABAR O 

	def postSale(self, item):
		sale = Sale(
			0,
			self.window.customerId(),
			cart=self.window.listProduct()
		)
		headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
		r = requests.post("http://localhost:8080/api/v1/sales", data=sale.toJson(), headers=headers)
		print(r.status_code)
		if r.status_code == 200:
			self.getSale()

	def deleteProduct(self, item):
		self.view.listview.setEnabled(False)
		data = self.view.listview.itemWidget(item).data
		r = requests.delete("http://localhost:8080/api/v1/sales/{}".format(data.id))
		if r.status_code == 204:
			self.view.listview.deleteItem(item)
		self.view.listview.setEnabled(True)

	def putSale(self, item):
		self.view.listview.setEnabled(False)
		data = Product(
			self.view.listview.itemWidget(item).data.id,
			self.window.name(),
			self.window.category(),
			self.window.price(),
			self.window.stock(),
		)
		headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
		r = requests.put("http://localhost:8080/api/v1/sales/{}".format(data.id), data=data.toJson(), headers=headers)
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
		sale = self.view.listview.itemWidget(item).data
		self.window.view.clear()	
		self.window.view.setData(sale)
		self.window.view.setTitle("Editando um Produto")
		self.window.view.onSuccess = self.onEditItem
		self.window.view.setCurrentItem(item)	
		self.window.view.show()

	def onAddNewItem(self, item):
		postThread = RestThread(self.view, data=item)
		postThread.update.connect(self.postSale)
		postThread.start()

	def onEditItem(self, item):
		putThread = RestThread(self.view, item)
		putThread.update.connect(self.putSale)
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
