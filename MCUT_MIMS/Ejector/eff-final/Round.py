#coding:utf-8

import wx
import math
from wx.lib.pubsub import pub
import requests
from numpy import size
from wx.lib.analogclock import styles


class RoundPanel(wx.Panel):
	def __init__(self,parent,id,number,total):
		wx.Panel.__init__(self,parent,id = id)

		self.SetBackgroundColour('Black')

		self.number = number
		self.total = total


		showPanel = DrawShowPanel(self,wx.ID_ANY,number = self.number,total = self.total)
		showPanel.SetPosition((0,0))
		showPanel.SetSize((62,62))







# 最外层的圆
class DrawShowPanel(wx.Panel):
	def __init__(self,parent,id,number,total):
		wx.Panel.__init__(self,parent,id=id)

		self.number = number
		self.totalNumber = total

		self.SetBackgroundColour('Black')
		self.Bind(wx.EVT_PAINT,self.DrawPaint)


		# gs = wx.GridSizer(1,1,0,0)
		hbox = wx.BoxSizer(wx.HORIZONTAL)
		vbox = wx.BoxSizer(wx.VERTICAL)


		try:
			num = (float(self.number) / float(self.totalNumber)) * 100
		except Exception as e:
			num = 0.0
		
		if num > 0.0:
			numString = str(int(num)) + '%'
		else:
			numString = '0%'

		

		self.total = wx.StaticText(self,wx.ID_ANY,style=wx.ALIGN_CENTER)
		self.total.SetForegroundColour('#ffffff')
		font = wx.Font(22.5,wx.DEFAULT,wx.NORMAL,wx.NORMAL,faceName='Alte DIN 1451 Mittelschrift')
		self.total.SetFont(font)
		self.total.SetLabel(numString)

		vbox.Add(self.total,1,wx.CENTER)
		hbox.Add(vbox,1,wx.CENTER)

		self.SetSizer(hbox)


	def DrawPaint(self,ecect):
		dc = wx.PaintDC(self)

		# 半径
		R = 62.0/2.0
		R2 = 62.0/2.0 - 5.0

		# 圆心
		cY = 62.0/2.0
		cX = 62.0/2.0

		try:
			num = (float(self.number)/float(self.totalNumber)) * 360.0
		except Exception as e:
			num = 0.0


		sinNum = math.sin(num*(math.pi / 180.0))
		cosNum = math.cos(num*(math.pi / 180.0))

		x2 = cX + R2 * sinNum
		y2 = cY + R2 * cosNum

		dc.SetPen(wx.Pen('Black',1,wx.TRANSPARENT))
		dc.SetBrush(wx.Brush('#4a4a4a'))
		dc.DrawArc(R,0,R,0,cX,cY)

		if num > 0:
			dc.SetPen(wx.Pen('#4a4a4a',1,wx.TRANSPARENT))
			dc.SetBrush(wx.Brush('#2f7c69'))
			dc.DrawArc(x2,((R * 2) - y2),R,0.0,cX,cY)
		else:
			pass






