import json
class Category(object):
	def __init__(self, id, name):
		self.id = id
		self.name = name

	def toJson(self):
		arr = json.dumps(self.__dict__)
		print(arr)
		return arr