#coding:utf-8


import wx
from timeLabel import *
from JsonParsing import *


class PresentPanel(wx.Panel):
	def __init__(self,parent,id,pos,size):
		wx.Panel.__init__(self,parent,id=id,pos=pos,size=size)
		


		self.SetBackgroundColour('Black')

		width = self.GetSize().width
		height = self.GetSize().height


		font = wx.Font(29,wx.SWISS,wx.NORMAL,wx.NORMAL)

		self.title = wx.TextCtrl(self,wx.ID_ANY,pos=(0,0),size=(660,40),style = wx.TE_LEFT|wx.TE_READONLY|wx.BORDER_NONE|wx.ST_ELLIPSIZE_END)
		self.title.SetBackgroundColour('Black')
		self.title.SetFont(font)
		self.title.SetForegroundColour('#347766')



		self.totalPanel = TotalPanel(self,wx.ID_ANY,pos=(760,0),size=(320,height),color='#347766')
		# self.totalPanel.SetPosition((760,0))
		# self.totalPanel.SetSize((320,height))


		#self.timePanel = TimePanel(self,wx.ID_ANY,pos=(600,0))
		#self.timePanel.SetSize((150,40))


		linePanel = wx.Panel(self,wx.ID_ANY,pos=(0,height - 10),size=(width,1))
		linePanel.SetBackgroundColour('#4a4a4a')

	def PersentLoadModel(self,object):


		print "object =============="
		print object
		print 'object =============='

		data = DataAnlays(object)
		self.title.SetValue(data.name)
		self.totalPanel.totalLoadModel(data.qty)
		#if data.current == '1':
		#	self.timePanel.TimeLoadModel(data.start_time,data.Id)
		#else:
		#	self.timePanel.TimeLoadModel(None,data.Id)
		pass

	def PersentClearData(self):

		self.title.SetValue('')
		self.totalPanel.totalLoadModel('')
		#self.timePanel.TimeLoadModel(None,data.Id)



class OtherPanel(wx.Panel):
	def __init__(self,parent,id,pos,size):
		wx.Panel.__init__(self,parent,id=id,pos=pos,size=size)


		self.SetBackgroundColour('Black')


		width = self.GetSize().width
		height = self.GetSize().height



		self.title = wx.TextCtrl(self,wx.ID_ANY,pos=(0,0),size=(660,40),style =wx.TE_LEFT|wx.TE_READONLY|wx.BORDER_NONE|wx.wx.ST_ELLIPSIZE_END)
		self.title.SetForegroundColour('#4a4a4a')
		self.title.SetBackgroundColour('Black')
		font = wx.Font(29,wx.SWISS,wx.NORMAL,wx.NORMAL)
		self.title.SetFont(font)



		self.totalpanel = TotalPanel(self,wx.ID_ANY,pos=(760,0),size=(420,40),color='#4a4a4a')
		# self.totalpanel.SetPosition((760,0))
		# self.totalpanel.SetSize((420,40))



		linePanel = wx.Panel(self,wx.ID_ANY,pos=(0,height - 10),size=(width,1))
		linePanel.SetBackgroundColour('#4a4a4a')

		pass


	def OtherLoadModel(self,object):
		data = DataAnlays(object)

		self.title.SetValue(data.name)

		self.totalpanel.totalLoadModel(data.qty)

		pass

	def OtherClearData(self):
		self.title.SetValue('')
		self.totalpanel.totalLoadModel('')

class TotalPanel(wx.Panel):
	def __init__(self,parent,id,pos,size,color):
		wx.Panel.__init__(self,parent,id=id,pos = pos ,size= size)

		self.color = color

		self.SetBackgroundColour('Black')


		font = wx.Font(29,wx.DEFAULT,wx.NORMAL,wx.NORMAL,faceName='PingFangSC')

		width = self.GetSize().width
		height = self.GetSize().height


		self.total = wx.TextCtrl(self,wx.ID_ANY,pos=(0,0),size=(180,40),style = wx.TE_RIGHT|wx.TE_READONLY|wx.BORDER_NONE)
		self.total.SetFont(font)
		self.total.SetBackgroundColour('Black')
		self.total.SetForegroundColour(self.color)


	def totalLoadModel(self,object):

		self.total.SetValue(object)





