from PyQt5.QtWidgets import QWidget, QGridLayout
from view.titlebar import Titlebar

class Screen(QWidget):
	def __init__(self, *args):
		super(Screen, self).__init__(*args)
		self._initUI()

	def _initUI(self):
		self.setLayout(QGridLayout())
		self.layout().setContentsMargins(0, 0, 0, 0)
		self.layout().addWidget(Titlebar("hello world"))

	def setCentralWidget(self):
		self.layout().addWidget(self, 0, 1)