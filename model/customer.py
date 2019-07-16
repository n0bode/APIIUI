import json

class Customer(object):
	def __init__(self, id, name, email, phone):
		self.id = id
		self.name = name
		self.email = email
		self.phone = phone

	def toJson(self):
		return json.dumps(self.__dict__)