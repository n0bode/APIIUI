from PyQt5.Qt import QAbstractListModel

class FilterModel(QAbstractListModel):
	def __init__(self, *args):
		super(FilterModel, self).__init__(*args)