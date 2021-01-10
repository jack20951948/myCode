# coding:utf-8

import wx
import os
import time
import sys
import Model
from subprocess import Popen, PIPE
from Round import RoundPanel
from ListItem import *
from GifPanel import *
from sound import *
from Request import RequestTool
from wx.lib.pubsub import pub
from JsonParsing import *
import datetime
from JsonParsing import *
from GetData import *
import json
from SynListener import SynListener

WIDTH = 1080
HEIGHT = 1920

faceName = 'Alte DIN 1451 Mittelschrift'
abs_path = os.path.abspath(os.path.dirname(__file__)) + os.path.sep


# 主屏幕
class MainPanel(wx.Panel):
    def __init__(self, parent, pos, size):
        wx.Panel.__init__(self, parent, id=wx.NewId(), size=size)

        # 背景颜色
        self.SetBackgroundColour('Black')

        # 获取 图片文件夹地址
        files = Model.GetImageFileAddress()

        self.GIFName = None
        # e = wx.FontEnumerator()
        # e.EnumerateFacenames()
        # fontList= e.GetFacenames()
        # print fontList

        # 获取IP地址的注释掉
        # ipAdd = Model.GetLocalIPAddress()

        # 获取射出机 数据
        # self.client = ClientLinkThread()
        self.client = GetData()

        #         print self.client

        self.client.start()
        self.oldNumber = 0
        self.tolNum = 0

        self.url = None
        self.listOneData = None
        self.listOneId = None
        self.listTime = None

        logoPath = files + 'ENGEL_LOGO.png'
        logo = wx.StaticBitmap(self, wx.ID_ANY, pos=(228, 147), size=(624, 195))
        logoImage = wx.Image(logoPath).Scale(624, 195).ConvertToBitmap()
        logo.SetBitmap(logoImage)

        # logo下已经没有文字了
        self.textpanel = TextPanel(self, wx.ID_ANY, pos=(150, 357), size=(771, 45))

        self.totalMainpanel = TotalMianPanel(self, wx.ID_ANY, pos=(0, 376), size=(1080, 490))

        # self.ronpanel = RoundPanel(self, wx.ID_ANY, number=0, total=0)
        # self.ronpanel.SetPosition((930, 827))
        # self.ronpanel.SetSize((62, 62))

        self.timePanel = TimePanel(self, wx.ID_ANY)

        self.listPanel = ListPanel(self, wx.ID_ANY, pos=(66, 1046), size=(980, 200))
        self.imagePanel = ImagePanel(self, wx.ID_ANY)
        self.imagePanel.SetSize((1080, 170))
        self.imagePanel.SetPosition((31, 1268))

        self.loadGif = False

        # self.requestIndexURL(ipAdd)
        self.requestSuccess()
        self.soundMe = sound()
        self.gifPanel = GifPanel(self, wx.ID_ANY)
        self.gifPanel.SetPosition((0, HEIGHT - 420))
        self.gifPanel.SetSize((WIDTH, 420))

        # sec = (30 * 60 * 1000) / 2, 暂时不更新订单信息。
        # sec = 60 * 1000
        # wx.FutureCall(sec, self.intervalRequet)

        pub.subscribe(self.PlaySound, 'PlaySoundMethod')
        pub.subscribe(self.requestSuccess, 'ReturnData')
        pub.subscribe(self.MachineLoad, 'Machine')
        pub.subscribe(self.ListData, 'ListData')
        pub.subscribe(self.ClientMinimal, 'GetData')
        pub.subscribe(self.GifPlayer, 'GIFPlayerMethod')
        pub.subscribe(self.refreshData, 'refreshData')
        pub.subscribe(self.ElapsedTime, 'ElapsedTime')
        pub.subscribe(self.RequestError, 'RequestError')

    def ElapsedTime(self, time):
        self.listTime = time
        pass

    def LoadGIf(self):
        if self.loadGif == False:
            self.loadGif = True
            self.gifPanel.LoadGifView(self.GIFName)

    # if self.client.isOpen == False:
    # 	self.client.isOpen = True
    # 	self.client.threadOpen()

    def MachineLoad(self, result):

        machine = MachineAnlays(result)

        # logo下已经没有文字了
        # self.textpanel.LoadModel(machine.model)
        self.GIFName = machine.model

        wx.FutureCall(1000, self.LoadGIf)
        pass

    def ListData(self, result):

        self.listPanel.LoadModel(result)
        pass

    def ClientMinimal(self, number, totaltime, rate_str, remainTime, currentTime):

        if self.oldNumber == number:
            if self.listTime == None:
                time = '00:00:00'
            else:
                time = self.listTime

            dict = {'time': time, 'number': str(number)}
            Model.TotalWriteFile(self.listOneId, str(dict))

        else:
            # try:

            if self.listTime == None:
                time = '00:00:00'
            else:
                time = self.listTime
                pass

            self.oldNumber = number
            if Model.FileExists(self.listOneId) == False:
                num = number
            else:
                dictString = Model.ReadFile(self.listOneId)
                dict = eval(dictString)
                localNumber = dict['number']
                num = int(localNumber)

                if num < number:
                    num = (number - num) + num
                elif num > number:
                    num = number + num
                else:
                    num = number

            numString = format(num, ',')
            wx.FutureCall(1180, pub.sendMessage, 'PlaySoundMethod', state=True)
            self.totalMainpanel.LoadModel(numString)
            self.timePanel.LoadModel(totaltime, rate_str, remainTime, currentTime)

            # wx.FutureCall(1180, pub.sendMessage,'PlaySoundMethod',state = True)
            # os.system("aplay ding2.wav")
            # aaa = subprocess.check_call("aplay ding2.wav",shell=True)

            dict = {'time': time, 'number': str(number)}
            Model.TotalWriteFile(self.listOneId, str(dict))

            if self.listOneData != None:
                obj = DataAnlays(self.listOneData)
                self.tolNum = obj.qty
            else:
                self.tolNum = 0

            # wx.CallAfter(pub.sendMessage,'PlaySoundMethod',state = True)
            wx.CallAfter(pub.sendMessage, 'GIFPlayerMethod', state=True)

        # 球已经被隐藏了
        # self.refreshRound(number, self.tolNum)
        # os.popen("python sound.py")

        pass

    def GifPlayer(self, state):
        self.gifPanel.StarGif()
        pass

    def PlaySound(self, state):
        self.soundMe.StartSound()
        pass

    def requestIndexURL(self, ip):

        request = RequestTool()
        request.addPost(key='ip', value=ip)
        request.request(userKey='getURL', url=None, name='IOTmanage', method='get_url')

        pass

    def requestIndexData(self, url):
        self.url = url
        request = RequestTool()
        request.request(userKey='Data', url=url, name=None, method=None)
        pass

    # 模拟订单信息时的方法
    def requestSuccess(self):
        f = open(abs_path + 'order.config')
        r = json.load(f)
        anlyays_json = JSONAnlays(r)
        try:
            self.listOneData = anlyays_json.data[0]
            self.listOneId = self.listOneData['Id']
        except Exception as e:
            print
            '%s' % e
        else:
            self.listOneData = {'Id': ''}
            self.listOneId = ''

        wx.CallAfter(pub.sendMessage, 'Machine', result=anlyays_json.machine)
        wx.CallAfter(pub.sendMessage, 'ListData', result=anlyays_json.data)

    # 有订单信息时的方法
    # def requestSuccess(self, result, userKey):
    #
    #     r = requests.get(result['url'])
    #     anlyays_json = JSONAnlays(r.json())
    #     try:
    #         self.listOneData = anlyays_json.data[0]
    #         self.listOneId = self.listOneData['Id']
    #     except Exception as e:
    #         print
    #         '%s' % e
    #     else:
    #         self.listOneData = {'Id': ''}
    #         self.listOneId = ''
    #
    #     wx.CallAfter(pub.sendMessage, 'Machine', result=anlyays_json.machine)
    #     wx.CallAfter(pub.sendMessage, 'ListData', result=anlyays_json.data)


    def refreshData(self, state):
        wx.CallAfter(pub.sendMessage, 'ClearOldDalta', state=True)
        request = RequestTool()
        request.request(userKey='Data', url=self.url, name=None, method=None)

    def intervalRequet(self):
        request = RequestTool()
        request.request(userKey='Data', url=self.url, name=None, method=None)
        # sec = 60 * 1000
        # wx.FutureCall(sec,self.intervalRequet)
        pass

    def refreshRound(self, number, total):

        if self.ronpanel != None:
            self.ronpanel.Destroy()
            self.ronpanel = None
        else:
            pass
        self.ronpanel = RoundPanel(self, wx.ID_ANY, number=number, total=total)
        self.ronpanel.SetPosition((900, 827))
        self.ronpanel.SetSize((62, 62))

    def RequestError(self, userKey):
        if str(userKey) == 'getURL':
            self.requestIndexData(self.url)
        else:
            ipAdd = Model.GetLocalIPAddress()
            self.requestIndexURL(ipAdd)


# LOGO 下面的文字
class TextPanel(wx.Panel):

    def __init__(self, parent, id, pos, size):
        wx.Panel.__init__(self, parent, id=id, pos=pos, size=size)

        self.SetBackgroundColour('Black')

        font = wx.Font(1, wx.DEFAULT, wx.NORMAL, wx.NORMAL, faceName=faceName)

        wid = self.GetSize().width
        hei = self.GetSize().height

        self.logoSubText = wx.TextCtrl(self, wx.ID_ANY, pos=(0, 0), size=(wid, hei),
                                       style=wx.TE_RIGHT | wx.BORDER_NONE | wx.TE_READONLY)
        self.logoSubText.SetBackgroundColour('Black')
        self.logoSubText.SetForegroundColour('#9b9b9b')
        self.logoSubText.SetFont(font)

    def LoadModel(self, object):
        # string = 'ALLROUNDER %s' % object
        title = ''
        self.logoSubText.SetValue(title)
        pass


class TotalMianPanel(wx.Panel):
    def __init__(self, parent, id, pos, size):
        wx.Panel.__init__(self, parent, id=id, pos=pos, size=size)

        self.SetBackgroundColour('Black')

        wid = self.GetSize().width
        hei = self.GetSize().height

        box = wx.BoxSizer(wx.HORIZONTAL)

        font = wx.Font(200, wx.DEFAULT, wx.NORMAL, wx.NORMAL, faceName=faceName)

        self.totalText = wx.TextCtrl(self, wx.ID_ANY, pos=(0, 0), size=(wid, hei),
                                     style=wx.TE_CENTER | wx.TE_READONLY | wx.BORDER_NONE)
        self.totalText.SetFont(font)
        self.totalText.SetForegroundColour('White')
        self.totalText.SetBackgroundColour('Black')
        box.Add(self.totalText, 1, wx.EXPAND)

        self.SetSizer(box)

        pass

    def LoadModel(self, object):
        # self.totalText.SetLabel(object)
        self.totalText.SetValue(object)
        # os.popen2("python sound.py")
        pass


class TimePanel(wx.Panel):
    def __init__(self, parent, id):
        wx.Panel.__init__(self, parent, id=id, pos=(66, 800), size=(940, 200))
        self.SetBackgroundColour('Black')

        box = wx.BoxSizer(wx.HORIZONTAL)
        font = wx.Font(30, wx.DEFAULT, wx.NORMAL, wx.NORMAL, faceName=faceName)
        font1 = wx.Font(30, wx.DEFAULT, wx.NORMAL, wx.NORMAL, faceName=faceName)

        # totalStaticText = wx.StaticText(self, wx.ID_ANY,pos=(0,0),label="------------------------",size=(940, 25))

        totalStaticText = wx.StaticText(self, wx.ID_ANY, pos=(0, 30), label="用時", size=(70, 40))
        totalStaticText.SetFont(font1)
        totalStaticText.SetForegroundColour('#347766')
        self.totalTimeText = wx.TextCtrl(self, wx.ID_ANY, pos=(80, 40), size=(200, 40),
                                         style=wx.TE_RIGHT | wx.TE_READONLY | wx.BORDER_NONE)
        self.totalTimeText.SetFont(font)
        self.totalTimeText.SetForegroundColour('White')
        self.totalTimeText.SetBackgroundColour('Black')
        # box.Add(self.totalTimeText,1,wx.EXPAND)

        avgStaticText = wx.StaticText(self, wx.ID_ANY, pos=(740, 30), label="良率", size=(70, 40))
        avgStaticText.SetFont(font1)
        avgStaticText.SetForegroundColour('#347766')
        self.timeRoundAvgText = wx.TextCtrl(self, wx.ID_ANY, pos=(820, 40), size=(120, 40),
                                            style=wx.TE_LEFT | wx.TE_READONLY | wx.BORDER_NONE)
        self.timeRoundAvgText.SetFont(font)
        self.timeRoundAvgText.SetForegroundColour('White')
        self.timeRoundAvgText.SetBackgroundColour('Black')
        # box.Add(self.timeRoundAvgText,1,wx.EXPAND)

        remainStaticText = wx.StaticText(self, wx.ID_ANY, pos=(0, 100), label="剩餘", size=(70, 40))
        remainStaticText.SetFont(font1)
        remainStaticText.SetForegroundColour('#347766')
        self.remainText = wx.TextCtrl(self, wx.ID_ANY, pos=(80, 110), size=(200, 40),
                                      style=wx.TE_RIGHT | wx.TE_READONLY | wx.BORDER_NONE)
        self.remainText.SetFont(font)
        self.remainText.SetForegroundColour('White')
        self.remainText.SetBackgroundColour('Black')
        # box.Add(self.remainText,1,wx.EXPAND)

        currentStaticText = wx.StaticText(self, wx.ID_ANY, pos=(740, 100), label="本次", size=(70, 40))
        currentStaticText.SetFont(font1)
        currentStaticText.SetForegroundColour('#347766')
        self.timeRoundText = wx.TextCtrl(self, wx.ID_ANY, pos=(820, 110), size=(120, 40),
                                         style=wx.TE_RIGHT | wx.TE_READONLY | wx.BORDER_NONE)
        self.timeRoundText.SetFont(font)
        self.timeRoundText.SetForegroundColour('White')
        self.timeRoundText.SetBackgroundColour('Black')
        # box.Add(self.timeRoundText,1,wx.EXPAND)

        self.SetSizer(box)

        pass

    # totaltime,avgTime,remainTime,currentTime
    def LoadModel(self, object1, object2, object3, object4):
        self.totalTimeText.SetValue(object1)
        self.timeRoundAvgText.SetValue(object2)
        self.remainText.SetValue(object3)
        self.timeRoundText.SetValue(object4)
        pass


# 信息列表
class ListPanel(wx.Panel):
    def __init__(self, parent, id, pos, size):
        wx.Panel.__init__(self, parent, id=id, pos=pos, size=size)

        self.SetBackgroundColour('Black')

        width = self.GetSize().width
        height = self.GetSize().height

        self.onePanel = PresentPanel(self, wx.ID_ANY, pos=(0, 0), size=(width, height / 3))
        self.twoPanel = OtherPanel(self, wx.ID_ANY, pos=(0, height / 3), size=(width, height / 3))
        self.three = OtherPanel(self, wx.ID_ANY, pos=(0, height / 3 * 2), size=(width, height / 3))

        pass

    def LoadModel(self, object):

        if len(object) > 2:
            self.onePanel.PersentLoadModel(object[0])
            self.twoPanel.OtherLoadModel(object[1])
            self.three.OtherLoadModel(object[2])
        elif len(object) == 2:
            self.onePanel.PersentLoadModel(object[0])
            self.twoPanel.OtherLoadModel(object[1])
            self.three.OtherClearData()
        elif len(object) < 2:
            if len(object) > 0:
                self.onePanel.PersentLoadModel(object[0])
                self.twoPanel.OtherClearData()
                self.three.OtherClearData()
            else:
                self.onePanel.PersentClearData()
                self.twoPanel.OtherClearData()
                self.three.OtherClearData()
                pass
        else:
            pass


# 图
class ImagePanel(wx.Panel):
    def __init__(self, parent, id):
        wx.Panel.__init__(self, parent, id=id)

        self.SetBackgroundColour('Black')

        okimg = Model.GetImageFileAddress() + 'OK.png'
        wdimg = Model.GetImageFileAddress() + 'temperature.png'

        imageView1 = wx.StaticBitmap(self, wx.ID_ANY, pos=(32, 0), size=(440, 170))
        okImage = wx.Image(okimg).Scale(440, 170).ConvertToBitmap()
        imageView1.SetBitmap(okImage)

        imageView2 = wx.StaticBitmap(self, wx.ID_ANY, pos=(533, 0), size=(440, 170))
        wdImage = wx.Image(wdimg).Scale(440, 170).ConvertToBitmap()
        imageView2.SetBitmap(wdImage)


class Window(wx.Frame):
    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, title='mian', size=(WIDTH, HEIGHT))

        # 全屏
        self.ShowFullScreen(True)

        # 设置隐藏鼠标
        cursor = wx.StockCursor(wx.CURSOR_BLANK)
        wx.SetCursor(cursor)

        # 背景颜色
        self.SetBackgroundColour('Black')

        minaPanel = MainPanel(self, -1, size=(WIDTH, HEIGHT))

    def setInit(self):
        pass


class Container(wx.App):
    def OnInit(self):
        frame = Window(None, -1)

        pub.subscribe(self.reloadTask, 'reload')

        self.listener = SynListener(30030)
        self.listener.start()

        frame.Show()
        return True

    def reloadTask(self, parameters):
        # wx.CallAfter(pub.sendMessage, 'refreshData', state=True)
        pass


if __name__ == '__main__':
    app = Container()
    app.MainLoop()

