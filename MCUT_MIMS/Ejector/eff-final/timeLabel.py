#coding:utf-8



import wx
import Model
import datetime
import time
import pytz

from wx.lib.pubsub import pub



timeStyle = '%Y-%m-%d %H:%M:%S'
hmsStyle = '%H:%M:%S'


class TimePanel(wx.Panel):
	def __init__(self,parent,id,pos):
		wx.Panel.__init__(self,parent,id=id,pos=pos)
		
		self.SetBackgroundColour('Black')

		box = wx.BoxSizer(wx.HORIZONTAL)

		self.time = None
		self.IdString = None
		self.isRefsh = False
		self.oldDelta = None

		font = wx.Font(28,wx.SWISS,wx.NORMAL,wx.NORMAL)

		self.HLabel = timeLabel(self,wx.ID_ANY,pos=(0,0),size=(33,33))

		symbol1 = wx.StaticText(self,wx.ID_ANY,label=':')
		symbol1.SetForegroundColour('#1ba784')
		symbol1.SetFont(font)


		self.MLabel = timeLabel(self,wx.ID_ANY,pos=(0,0),size=(33,33))

		symbol2 = wx.StaticText(self,wx.ID_ANY,label=':')
		symbol2.SetForegroundColour('#1ba784')
		symbol2.SetFont(font)

		self.SLabel = timeLabel(self,wx.ID_ANY,pos=(0,0),size=(33,33))

		box.Add(self.HLabel,0,wx.EXPAND)
		box.Add(symbol1,0,wx.ALL)
		box.Add(self.MLabel,0,wx.EXPAND)
		box.Add(symbol2,0,wx.ALL)
		box.Add(self.SLabel,0,wx.EXPAND)


		self.SetSizer(box)

		pub.subscribe(self.ClearOldDalta,'ClearOldDalta')


	def TimeLoadModel(self,object,Id):
		self.time = object
		if object == None:
			self.HLabel.LoadMoel('00')
			self.MLabel.LoadMoel('00')
			self.SLabel.LoadMoel('00')
		else:
			self.IdString = Id
			if Model.FileExists(str(self.IdString)) == True:
				string = Model.ReadFile(str(self.IdString))
				dict = eval(string)
				delta = dict['time']
				self.oldDelta = delta

				time_local = time.localtime(delta)
				dt = time.strftime(hmsStyle,time_local)
				pass
			else:
				# 时间转化为时间戳
				# 取得任务时间的时间戳
				d1Array = time.strptime(object,timeStyle)
				d1mestamp = time.mktime(d1Array)

				# 取得当前时间的时间戳
				tz = pytz.timezone('Asia/Shanghai')
				now = datetime.datetime.now(tz)
				nowStr = str(now.strftime(timeStyle))
				nowArray = time.strptime(nowStr,timeStyle)
				nowmestamp = time.mktime(nowArray)

				# 两个时间戳相减
				delta = nowmestamp - d1mestamp

				# 将时间戳转成时间
				time_local = time.localtime(delta)
				dt = time.strftime(hmsStyle,time_local)

			wx.CallAfter(pub.sendMessage,'ElapsedTime',time = delta)

			delatArr = dt.split(':')
			self.HLabel.SetLabel(delatArr[0])
			self.MLabel.SetLabel(delatArr[1])
			self.SLabel.SetLabel(delatArr[2])

		if self.isRefsh == False:
			wx.FutureCall(1000,self.reloadTime)
			self.isRefsh = True
		pass


	def reloadTime(self):

		if Model.FileExists(str(self.IdString)) == True:
			self.oldDelta = float(self.oldDelta) + 1.0
			delta= self.oldDelta
			time_local = time.localtime(self.oldDelta)
			dt = time.strftime(hmsStyle,time_local)
		else:
			# 取得当前时间的时间戳
			tz = pytz.timezone('Asia/Shanghai')
			now = datetime.datetime.now(tz)
			nowStr = str(now.strftime(timeStyle))
			nowArray = time.strptime(nowStr,timeStyle)
			nowmestamp = time.mktime(nowArray)

			if self.time == None:
				self.time = nowStr
			else:
				pass

			# 时间转化为时间戳
			# 取得任务时间的时间戳
			d1Array = time.strptime(self.time,timeStyle)
			d1mestamp = time.mktime(d1Array)

			# 两个时间戳相减
			delta = nowmestamp - d1mestamp

			# 将时间戳转成时间
			time_local = time.localtime(delta)
			dt = time.strftime(hmsStyle,time_local)


		wx.CallAfter(pub.sendMessage,'ElapsedTime',time = delta)

		delatArr = dt.split(':')
		self.HLabel.LoadMoel(delatArr[0])
		self.MLabel.LoadMoel(delatArr[1])
		self.SLabel.LoadMoel(delatArr[2])
		
		wx.FutureCall(1000,self.reloadTime)

	def ClearOldDalta(self,state):
		self.oldDelta = None
		pass


class timeLabel(wx.Panel):

	def __init__(self,parent,id,pos,size):
		wx.Panel.__init__(self,parent,id=id,pos=pos,size=size)

		self.SetBackgroundColour('Black')
		
		imagePath = Model.GetImageFileAddress()
		imageName = imagePath + 'bg.png'


		width = self.GetSize().width
		height = self.GetSize().height

		backImageView = wx.StaticBitmap(self,wx.ID_ANY,pos=(0,8),size=(width,height))
		bacImage = wx.Image(imageName).Scale(width,height).ConvertToBitmap()
		backImageView.SetBitmap(bacImage)


		# box = wx.BoxSizer(wx.HORIZONTAL)
		hbox = wx.BoxSizer(wx.HORIZONTAL)
		vbox = wx.BoxSizer(wx.VERTICAL)


		font = wx.Font(25,wx.DEFAULT,wx.NORMAL,wx.NORMAL,faceName=Model.AshCloud62Font)
		self.total = wx.StaticText(self,wx.ID_ANY,pos=((2.5,11)),size=((width,height)),style = wx.ALIGN_CENTER)
		self.total.SetFont(font)
		self.total.SetForegroundColour('#1ba784')
		self.total.SetLabel('00')


		self.SetSizer(hbox)
		

	def LoadMoel(self,object):
		self.total.SetLabel(object)




		

