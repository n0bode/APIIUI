from PyQt5.QtWidgets import QWidget, QLineEdit, QHBoxLayout
from PyQt5.Qt import QSize, pyqtSignal
import loader

class SearchBar(QWidget):
	submitted = pyqtSignal(str)
	
	def __init__(self, placeholder="type", *args):
		super(SearchBar, self).__init__(*args)
		self._initUI()
		self.setPlaceHolder(placeholder)
		
	def setPlaceHolder(self, text):
		self._input.setPlaceholderText(text)

	def getPlaceHolder(self):
		return self._input.placeholderText()

	def _initUI(self):
		self._input = QLineEdit()
		self._input.setFixedHeight(25)
		self._input.returnPressed.connect(self._onSubmit)
		self._input.textChanged.connect(self._onType)

		self._btn = loader.buttonIcon("search.png", 15, 15)
		self._btn.setFixedSize(25, 25)
		self._btn.clicked.connect(self._onSubmit)

		self.setLayout(QHBoxLayout())
		self.layout().setSpacing(0)
		self.layout().addWidget(self._input)
		self.layout().addWidget(self._btn)

	def _onType(self, text):
		self.submitted.emit(text)

	def _onSubmit(self):
		self.submitted.emit(self._input.text())

	def clear(self):
		self._input.clear()