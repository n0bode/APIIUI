import json
class Category(object):
	def __init__(self, id, name):
		self.id = id
		self.name = name

	def toJson(self):
		return json.dumps(self.__dict__)