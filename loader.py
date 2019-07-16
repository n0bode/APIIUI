import os
from PyQt5.QtWidgets import QPushButton
from PyQt5.Qt import QIcon, QSize

_icons = {}

def curpath():
	return os.path.dirname(__file__)

def loadStyle(name):
	with open(os.path.join(curpath(), "assets", "styles", name), "r") as file:
		return file.read()

def iconPath(name):
	return os.path.join(curpath(), "assets", "icons", name)

def readTranslate(name):
	if not name.endswith(".json"):
		name = "{}.json".format(name)

	with open(os.path.join(curpath(), "assets", "translations", name), "r") as file:
		return file.read()

def loadIcon(name):
	if not name.endswith(".png"):
		name = "{}.png".format(name)

	if name in _icons:
		return _icons[name]

	icon = QIcon(iconPath(name))
	_icons.update({name:icon})
	return icon

def buttonIcon(name, width=30, height=30):
	btn = QPushButton()
	btn.setIcon(loadIcon(name))
	btn.setIconSize(QSize(width, height))
	return btn