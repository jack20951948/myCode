#coding:utf-8


class JSONAnlays(object):
	def __init__(self,object):
		self.machine = object['machine']
		self.data = object['data']


class MachineAnlays(object):
	def __init__(self,object):
		self.model = object['model']
		self.ip = object['ip']
		self.port = object['port']



class DataAnlays(object):
	def __init__(self,object):
		self.Id = object['Id']
		if 'name' in object.keys():
			self.name=object['name']
		else:
			self.name = ''
		if 'qty' in object.keys():
			self.qty = object['qty']
		else:
			self.qty = ''
		if 'current' in object.keys():
			self.current = object['current']
		else:
			self.current = '0'
		if 'start_time' in object.keys():
			self.start_time = object['start_time']
		else:
			self.start_time = None

