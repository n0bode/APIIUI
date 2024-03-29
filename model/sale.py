import json

class Sale(object):
	def __init__(self, id, customerId, grossAmount=0, netAmount=0, amountPaid=0, discount=0, cart = []):
		self.id = id
		self.customerId = customerId
		self.grossAmount = grossAmount
		self.netAmount = netAmount
		self.amountPaid = amountPaid
		self.discount = discount
		self.cart = cart

	def toJson(self):
		return json.dumps(self.__dict__)