from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel

class Titlebar(QWidget):
	def __init__(self, title, mode=0, *args):
		super(Titlebar, self).__init__(*args)
		self.setAutoFillBackground(True)
		self._initUI()
		self.setTitle(title)

	def _initUI(self):
		self._label = QLabel("")
		closeBtn = QPushButton()
		closeBtn.setObjectName("closebutton")

		minimizeBtn = QPushButton()
		minimizeBtn.setObjectName("minimizebutton")

		maximizeBtn = QPushButton()
		maximizeBtn.setObjectName("maximebutton")

		self.setLayout(QHBoxLayout())
		self.layout().setContentsMargins(0, 0, 0, 0)
		self.layout().addStretch()
		self.layout().addWidget(self._label)
		self.layout().addStretch()
		self.layout().addWidget(minimizeBtn)
		self.layout().addWidget(maximizeBtn)
		self.layout().addWidget(closeBtn)

	def setTitle(self, text):
		self._label.setText(text)

	def title(self):
		return self._label.text()
