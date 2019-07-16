from PyQt5.QtWidgets import QLineEdit, QSpinBox, QHBoxLayout, QLabel, QWidget, QPushButton
from PyQt5.Qt import Qt, pyqtSignal
import loader

class ListViewItem (QWidget):
	def __init__(self, listview, item, data, model, isHeader=False, canEdit=True, canDelete=True, *args):
		super(ListViewItem, self).__init__(*args)
		self.item = item
		self.listview = listview
		self.isHeader = isHeader
		self.data = data
		self.canEdit = canEdit
		self.canDelete = canDelete
		self._initUI(model)

	def _initUI(self, arr):
		layout = QHBoxLayout()
		layout.setContentsMargins(5, 0, 0, 5)
		self.widgets = []

		if not self.isHeader:
			for elem in arr:
				label = QLabel(str(elem["text"]))
				if "width" in elem:
					label.setFixedWidth(elem["width"])
				layout.addWidget(label)
				self.widgets.append(label)
		else:
			for elem in arr:
				label = QPushButton(str(elem["text"]))
				label.setFlat(True)
				if "width" in elem:
					label.setFixedWidth(elem["width"])
				layout.addWidget(label)
				self.widgets.append(label)

		box = QWidget()
		box.setFixedWidth(60)
		box.setLayout(QHBoxLayout())
		box.layout().setContentsMargins(0, 0, 0, 0)
		box.layout().setAlignment(Qt.AlignLeft)

		if not self.isHeader:
			if self.canEdit:
				btnEdit = loader.buttonIcon("edit.png", 15, 15)
				btnEdit.setFixedSize(20, 20)
				btnEdit.setFlat(True)
				btnEdit.clicked.connect(self._onEdit)
				box.layout().addWidget(btnEdit)
			if self.canDelete:
				btnDel = loader.buttonIcon("cancel.png", 15, 15)
				btnDel.setFixedSize(20, 20)
				btnDel.setFlat(True)
				btnDel.clicked.connect(self._onDelete)
				box.layout().addWidget(btnDel)
		layout.addWidget(box)
		self.setLayout(layout)

	def _onEdit(self):
		self.listview.onPressEdit(self.item)

	def _onDelete(self):
		self.listview.onPressDelete(self.item)

	def disable(self):
		self.setFlags(self.flags() & ~Qt.ItemIsEnabled)

	def enable(self):
		self.setFlags(self.flags() | Qt.ItemIsEnabled)

	def __lt__(self, other):
		if self.isHeader:
			return True
		return self.widgets[0].text() > other.widgets[0].text()