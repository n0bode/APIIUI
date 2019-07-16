import loader 
import json

_data = {}

def init(language):
	text = loader.readTranslate(language)
	_data = json.loads(text)

def name(names):

	return _data[names]