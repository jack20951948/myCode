#coding:utf-8


import os
import sys
import socket
import fcntl
import struct



AshCloud62Font = 'AshCloud62'


# 获取项目地址
def GetProjectAddress():
	asbPATH = os.path.abspath(sys.argv[0])
	asbPATH = os.path.dirname(asbPATH)
	return asbPATH



# 获取图片地址
def GetImageFileAddress():
	absPATH = os.path.abspath(sys.argv[0])
	absPATH = os.path.dirname(absPATH) + '/images/'
	return absPATH


# 获取 本机IP地址
def GetLocalIPAddress():
	ifname = 'wlan0'
	s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	return socket.inet_ntoa(fcntl.ioctl(s.fileno(),0x8915,struct.pack('256s',ifname[:15]))[20:24])

def FileExists(fileName):
	path = GetProjectAddress()+'/totals/'+str(fileName)+'.text'
	if os.path.exists(path):
		return True
	else:
		return False

def TotalWriteFile(fileName,text):
	try:
		path = GetProjectAddress()+ '/totals/' + str(fileName) +'.text'
		with open(path,'w+') as file:
			file.write(str(text))
	except Exception as e:
		pass

def ReadFile(fileName):
	try:
		absPATH = GetProjectAddress() + '/totals/'
		file = open(absPATH+str(fileName)+'.text','r')
		text = file.read()
		file.close()
		return text
	except Exception as e:
		return ''