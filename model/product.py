import json

class Product:
	def __init__(self, id, name, categoryId, price, stock):
		self.id = id
		self.name = name
		self.categoryId = categoryId
		self.price = price
		self.stock = stock
		
	def toJson(self):
		return json.dumps(self.__dict__)