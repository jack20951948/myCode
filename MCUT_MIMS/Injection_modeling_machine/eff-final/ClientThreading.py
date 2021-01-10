#coding:utf-8

import wx
import threading
from wx.lib.pubsub import pub
import client_minimal2


class ClientNumer(threading.Thread):

	def __init__(self):
		threading.Thread.__init__(self)
		self.isStart = False


	def open(self):
		self.isStart = True
		self.start()

	def run(self):
		client_minimal2.ClientLink()



		
