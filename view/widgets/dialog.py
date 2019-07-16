from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QWidget, QFrame, QHBoxLayout, QVBoxLayout, QLabel
from view.widgets.stack import Stack
import loader

class Dialog(QWidget):
	def __init__(self, parent, *args):
		super(Dialog, self).__init__(parent=parent, *args)
		self.setWindowFlags(Qt.Dialog)
		self.onSuccess = None
		self.currentItem = None
		self.centralLayout = QVBoxLayout()
		self.centralLayout.setContentsMargins(5, 5, 5, 5)
		self.setStyleSheet(loader.loadStyle("dialog.style.css"))

	def _initUI(self):	
		topbar = self.createTopBar()
		#Botoes
		btnAdd = loader.buttonIcon("accept.png")
		btnAdd.setText("Aceitar")
		btnAdd.clicked.connect(self._onsuccess)
		
		btnRem = loader.buttonIcon("cancel.png")
		btnRem.setText("Discartar")
		btnRem.clicked.connect(self.close)

		boxBtn = QHBoxLayout()
		boxBtn.setAlignment(Qt.AlignRight)
		boxBtn.setContentsMargins(0, 0, 0, 0)
		boxBtn.addWidget(btnAdd)
		boxBtn.addWidget(btnRem)

		#Adicionando elementos a Layout Principal
		self.setLayout(QVBoxLayout())
		self.layout().setSpacing(10)
		self.layout().setContentsMargins(0, 0, 0, 0)

		self.centralLayout.addLayout(boxBtn)
		self.centralLayout.addStretch()

		self.layout().addWidget(topbar)
		self.layout().addLayout(self.centralLayout)

	def createTopBar(self):
		topbar = QFrame()
		topbar.setFixedHeight(50)
		topbar.setObjectName("topbar")
		topbar.setLayout(QHBoxLayout())
		topbar.layout().setAlignment(Qt.AlignLeft)

		buttonClose = loader.buttonIcon("close", 35, 35)
		buttonClose.setObjectName("buttonClose")
		buttonClose.setFixedSize(35, 35)
		buttonClose.setFlat(True)
		buttonClose.clicked.connect(self.close)		

		self._title = QLabel()
		topbar.layout().addWidget(self._title)
		topbar.layout().addStretch()
		topbar.layout().addWidget(buttonClose)
		return topbar

	def setCurrentItem(self, item):
		self.currentItem = item

	def update(self):
		self.setStyleSheet(self.styleSheet())

	def clear(self):
		pass
		
	def setTitle(self, title):
		self._title.setText(title)
		self.setWindowTitle(title)

	def setData(self, data):
		pass

	def addWidget(self, widget):
		frame = Stack()
		frame.setLayout(QVBoxLayout())
		frame.layout().setContentsMargins(5, 5, 5, 5)
		
		frame.layout().addWidget(widget)
		self.centralLayout.addWidget(frame)
		frame.setProperty("hint", False)

	def addField(self, text, widget):
		frame = Stack()
		frame.setLayout(QVBoxLayout())
		frame.layout().setContentsMargins(5, 5, 5, 5)

		frame.layout().addWidget(QLabel(text))
		frame.layout().addWidget(widget)
		self.centralLayout.addWidget(frame)
		frame.setProperty("hint", False)

	def _onsuccess(self):
		if self.checkSuccess():
			if self.onSuccess is not None:
				self.onSuccess(self.currentItem)
			self.close()
		self.update()

	def checkSuccess(self):
		return True