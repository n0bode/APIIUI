import json

class Product:
	def __init__(self, id, name, categoryID, price, stock):
		self.id = id
		self.name = name
		self.categoryID = categoryID
		self.price = price
		self.stock = stock
		
	def toJson(self):
		arr = json.dumps(self.__dict__)
		print(arr)
		return arr