# coding:utf-8


import Model
import wx
import urllib
import urllib2
import os
import sys
import requests
import threading
import time
from wx.lib.pubsub import pub


class RequestTool(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

        self.url = 'http://192.168.20.1/appAPI/web.php/'
        self.parameter = {}
        self.userKey = None

    def addPost(self, value, key):
        try:
            self.parameter[key] = value
        except Exception as e:
            print
            '参数错误 ： %s' % e

    def request(self, userKey, url, name, method):
        self.userKey = userKey
        if url != None:
            self.url = url
        else:
            self.url = self.url + name + '/' + method
        print
        self.url
        self.start()

    def run(self):
        for i in range(100):
            try:
                r = requests.post(self.url, self.parameter, timeout=3)
            except:
                print '**********'
                time.sleep(2)
        result = r.json()
        wx.CallAfter(pub.sendMessage, 'ReturnData', result=result, userKey=self.userKey)



