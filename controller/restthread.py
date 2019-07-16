from PyQt5.Qt import QThread, pyqtSignal

class RestThread (QThread):
	update = pyqtSignal(object)
	def __init__(self, parent, data=None, *args):
		super(RestThread, self).__init__(parent, *args)
		self.data = data 

	def run(self):
		try:
			self.update.emit(self.data)
		except:
			pass