from PyQt5.QtWidgets import QFrame
from PyQt5.Qt import pyqtProperty

class Stack (QFrame):
	def __init__(self, *args):
		super(Stack, self).__init__(*args)
		self.setProperty("hint", False)