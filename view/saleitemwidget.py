from PyQt5.QtWidgets import QLineEdit, QSpinBox, QHBoxLayout, QLabel, QWidget, QPushButton, QListWidgetItem
from PyQt5.Qt import Qt, pyqtSignal
import loader

class SaleItemWidget (QWidget):
	valueChanged = pyqtSignal(QListWidgetItem, float)

	def __init__(self, listview, item, data, model, isHeader=False, canEdit=True, canDelete=True, *args):
		super(SaleItemWidget, self).__init__(*args)
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
			for elem in arr[:len(arr)-1]:
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
			self.inputQtds = QSpinBox()
			self.inputQtds.setMinimum(1)
			self.inputQtds.setFixedWidth(arr[-1]["width"])
			self.inputQtds.valueChanged.connect(self.onChangeValue)
			self.inputQtds.setEnabled(self.canEdit)
			layout.addWidget(self.inputQtds)

			if self.canDelete:
				self.btnDel = loader.buttonIcon("cancel.png", 15, 15)
				self.btnDel.setFixedSize(20, 20)
				self.btnDel.setFlat(True)
				self.btnDel.clicked.connect(self._onDelete)
				box.layout().addWidget(self.btnDel)
		layout.addWidget(box)
		self.setLayout(layout)

	def disable(self):
		self.setFlags(self.flags() & ~Qt.ItemIsEnabled)

	def onChangeValue(self, value):
		if self.item != None:
			self.valueChanged.emit(self.item, value)

	def enable(self):
		self.setFlags(self.flags() | Qt.ItemIsEnabled)

	def _onDelete(self):
		self.listview.onPressDelete(self.item)

	def __lt__(self, other):
		if self.isHeader:
			return True
		return self.widgets[0].text() > other.widgets[0].text()