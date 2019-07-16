from controller.mainwindow import MainWindowController
import loader
import translator

if __name__ == "__main__":
	from PyQt5.QtWidgets import QApplication
	import sys
	translator.init("portugueses")
	app = QApplication(sys.argv)
	win = MainWindowController()
	win.view.setStyleSheet(loader.loadStyle("main.style.css"))
	win.run()
	sys.exit(app.exec_())