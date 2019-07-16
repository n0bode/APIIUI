from view.categoriesscreen import CategoriesScreen
from view.categorywindow import CategoryWindow
from model.category import Category
from PyQt5.QtWidgets import QMessageBox
from .restthread import RestThread
import json
import requests

class CategoriesScreenController(object):
	def __init__(self):
		self.view = CategoriesScreen(self)
		self.thread = RestThread(self.view)
		self.thread.update.connect(self.getCategory)
		self.thread.start()

		#Set Callback
		self.view.listview.onDeleteItem.connect(self.showDeleteAlert)
		self.view.listview.onEditItem.connect(self.showEditItem)
		self.view.listview.onFilter = self.filterItems

		self.window = CategoryWindow(self.view)
		self.createHeader()

	def addCategory(self, category):
		model = self.createModelItem(category.id, category.name)
		self.view.listview.createItem(category, model)

	def createHeader(self):
		header = self.createModelItem("ID", "Nome")
		self.view.listview.createHeader(header)

	def filterItems(self, data, pattern):
		return data.name.lower().startswith(pattern.lower())

	def getCategory(self):
		self.view.listview.setEnabled(False)
		self.view.listview.clear()
		try:
			r = requests.get("http://localhost:8080/api/v1/categories")
			if r.status_code == 200:
				for data in r.json():
					self.addCategory(Category(**data))
		except:
			pass
		self.view.listview.setEnabled(True)

	def postCategory(self, item):
		data = Category(0, self.window.inputName.text())
		headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
		r = requests.post("http://localhost:8080/api/v1/categories", data=data.toJson(), headers=headers)
		print(r.status_code)
		if r.status_code == 200:
			#self.addCategory(Category(**r.json()))
			self.getCategory()

	def deleteCategory(self, item):
		category = self.view.listview.itemWidget(item).data
		r = requests.delete("http://localhost:8080/api/v1/categories/{}".format(category.id))
		if r.status_code == 204:
			self.getCategory()

	def putCategory(self, item):
		data = Category(self.view.listview.itemWidget(item).data.id, self.window.inputName.text())
		headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
		r = requests.put("http://localhost:8080/api/v1/categories", data=data.toJson(), headers=headers)
		print(r.text)
		if r.status_code == 204:
			self.getCategory()

	def showAddItem(self):
		self.window.onSuccess = self.onAddNewItem
		self.window.clear()		
		self.window.setTitle("Adicionando Categoria")
		self.window.show()

	def showEditItem(self, item):
		category = self.view.listview.itemWidget(item).data
		self.window.clear()	
		self.window.setData(category)
		self.window.setTitle("Editando Categoria")
		self.window.onSuccess = self.onEditItem
		self.window.setCurrentItem(item)
		self.window.show()

	def onAddNewItem(self, item):
		postThread = RestThread(self.view, data=item)
		postThread.update.connect(self.postCategory)
		postThread.start()

	def onEditItem(self, item):
		putThread = RestThread(self.view, item)
		putThread.update.connect(self.putCategory)
		putThread.start()

	def showDeleteAlert(self, item):
		result = QMessageBox.warning(self.view, "Apagar Categoria", "Deseja apagar esse Categoria?", QMessageBox.Ok | QMessageBox.Cancel)
		if result == QMessageBox.Ok:
			deleteThread = RestThread(self.view, item)
			deleteThread.update.connect(self.deleteCategory)
			deleteThread.start()

	def load(self):
		pass
		
	def createModelItem(self, id, name):
		return [
			{"text":id, "width":50},
			{"text":name},
		]