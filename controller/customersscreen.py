from view.customersscreen import CustomersScreen
from view.customerwindow import CustomerWindow
from model.customer import Customer
from PyQt5.QtWidgets import QMessageBox
from .restthread import RestThread
import requests

class CustomersScreenController(object):
	def __init__(self):
		self.view = CustomersScreen(self)
		self.thread = RestThread(self.view)
		self.thread.update.connect(self.getCustomer)
		self.thread.start()

		#Set Callback
		self.view.listview.onDeleteItem.connect(self.showDeleteAlert)
		self.view.listview.onEditItem.connect(self.showEditItem)
		self.view.listview.onFilter = self.filterItems

		self.window = CustomerWindow(self.view)
		self.createHeader()

	def addCustomer(self, customer):
		model = self.createModelItem(customer.id, 
			customer.name, 
			customer.email, 
			customer.phone
		)
		self.view.listview.createItem(customer, model)

	def getCustomer(self):
		self.view.listview.setEnabled(False)
		self.view.listview.clear()
		try:
			r = requests.get("http://localhost:8080/api/v1/customers")
			if r.status_code == 200:
				for data in r.json():
					self.addCustomer(Customer(**data))
		except:
			pass
		self.view.listview.setEnabled(True)

	def postCustomer(self, item):
		data = Customer(
			0,
			self.window.name(),
			self.window.email(),
			self.window.phone(),
		)
		r = requests.post("http://localhost:8080/api/v1/customers", data=data.toJson())
		if r.status_code == 200:
			self.getCustomer()
			#self.addCustomer(Customer(**r.json()))

	def deleteCustomer(self, item):
		data = self.view.listview.itemWidget(item).data
		r = requests.delete("http://localhost:8080/api/v1/customers/{}".format(data.id))
		if r.status_code == 200:
			self.getCustomer()

	def putCustomer(self, item):
		data = Customer(
			self.view.listview.itemWidget(item).data.id,
			self.window.name(),
			self.window.email(),
			self.window.phone(),
		)
		r = requests.put("http://localhost:8080/api/v1/customers/{}".format(data.id), data=data.toJson())
		if r.status_code == 200:
			self.getCustomer()

	def createHeader(self):
		header = self.createModelItem("ID", "Nome", "Email", "Telefone")
		self.view.listview.createHeader(header)

	def filterItems(self, data, pattern):
		return data.name.lower().startswith(pattern.lower())

	def showAddItem(self):
		self.window.onSuccess = self.onAddNewItem
		self.window.clear()		
		self.window.setTitle("Adicionando Cliente")
		self.window.show()

	def showEditItem(self, item):
		product = self.view.listview.itemWidget(item).data
		self.window.clear()	
		self.window.setData(product)
		self.window.setTitle("Editando um Cliente")
		self.window.onSuccess = self.onEditItem
		self.window.setCurrentItem(item)		
		self.window.show()

	def onAddNewItem(self, item):
		postThread = RestThread(self.view, data=item)
		postThread.update.connect(self.postCustomer)
		postThread.start()

	def onEditItem(self, item):
		putThread = RestThread(self.view, item)
		putThread.update.connect(self.putCustomer)
		putThread.start()

	def showDeleteAlert(self, item):
		result = QMessageBox.warning(self.view, "Apagar Cliente", "Deseja apagar esse Cliente?", QMessageBox.Ok | QMessageBox.Cancel)
		if result == QMessageBox.Ok:
			deleteThread = RestThread(self.view, item)
			deleteThread.update.connect(self.deleteCustomer)
			deleteThread.start()

	def createModelItem(self, id, name, email, phone):
		return [
			{"text":id, "width":50},
			{"text":name},
			{"text":email},
			{"text":phone, "width":115},
		]