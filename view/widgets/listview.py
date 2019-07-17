from PyQt5.QtWidgets import QListWidget, QLabel, QListWidgetItem, QWidget, QHBoxLayout, QPushButton
from PyQt5.Qt import QSize, Qt, pyqtSignal
from .listviewitem import ListViewItem
from model.product import Product

class ListView(QListWidget):
	onEditItem = pyqtSignal(QListWidgetItem)
	onDeleteItem = pyqtSignal(QListWidgetItem)

	def __init__(self, header=None, canEdit=True, canDelete=True, *args):
		super(ListView, self).__init__(*args)
		self.setAlternatingRowColors(True)
		self.header = header
		self.onFilter = None
		self._lastPattern = ""
		self.canEdit = canEdit
		self.canDelete = canDelete
		if header is not None:
			self.createHeader()

	def createItem(self, data, model):
		item = QListWidgetItem()
		item.setSizeHint(QSize(0, 35))
		widget = self.createWidget(item, data, model)
		self.addItem(item)
		self.setItemWidget(item, widget)
		return item

	def addWidget(self, widget):
		item = QListWidgetItem()
		item.setSizeHint(QSize(0, 35))
		widget.item = item
		widget.canEdit = self.canEdit
		widget.canDelete = self.canDelete
		self.addItem(item)
		self.setItemWidget(item, widget)
		return item

	def onPressEdit(self, item):
		self.onEditItem.emit(item)

	def onPressDelete(self, item):
		self.onDeleteItem.emit(item)

	def deleteItem(self, item):
		row = self.row(item)
		#Testa pra ver se não é o header
		if row == 0:
			return
		self.takeItem(row)

	def editItem(self, id):
		pass

	def clear(self):
		super(ListView, self).clear()
		self.createHeader(self.header)

	def filter(self, pattern):
		if self._lastPattern != pattern:
			self._lastPattern = pattern
			for i in range(1, self.count()):
				item = self.item(i)
				widget = self.itemWidget(item)
				if self.onFilter != None and widget.data != None and self.onFilter(widget.data, pattern):
					item.setHidden(False)
				else:
					item.setHidden(True)

	def createWidget(self, item, data, model):
		return ListViewItem(self, item, data, model, canEdit=self.canEdit, canDelete=self.canDelete)

	def createHeader(self, header):
		self.header = header
		item = QListWidgetItem()
		item.setFlags(Qt.NoItemFlags)
		item.setSizeHint(QSize(0, 25))

		widget = ListViewItem(self, item, None, self.header, True)
		self.addItem(item)
		self.setItemWidget(item, widget)