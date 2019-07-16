import json

class SaleItem(json.JSONEncoder):
	def __init__(self, id , saleId, productId, quantity=0):
		self.id = id
		self.saleId = saleId
		self.productId = productId
		self.quantity = quantity

	def default(self, o):
		return o.__dict__