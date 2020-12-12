#coding:utf-8

import wx
import wx.animate
from wx.animate import GIFAnimationCtrl
import Model

class GifPanel(wx.Panel):
	def __init__(self,parent,id):
		wx.Panel.__init__(self,parent,id=id)

		self.SetBackgroundColour('Black')

		self.ag = None
		pass

	def LoadGifView(self,name):
		gifName = Model.GetImageFileAddress() + name+ '.gif'
		self.ag = wx.animate.GIFAnimationCtrl(self,wx.ID_ANY,gifName)

		if str(name) == '370E':
			point_y = -245
		elif str(name) == '420C':
			point_y = -180
		else:
			point_y = -360

		self.ag.SetPosition((0,point_y))
		self.ag.GetPlayer().UseBackgroundColour(True)


	def StarGif(self):
		self.ag.Play()
		pass


	def StopGif(self):
		self.ag.Stop()
		pass




