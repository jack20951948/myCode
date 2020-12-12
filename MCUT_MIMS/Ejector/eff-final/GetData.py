# coding:utf-8
import wx
import threading
from wx.lib.pubsub import pub
from opcua import Client
import time
import logging
import traceback
# logging.basicConfig(filename='opcua.log', format='%(asctime)s - %(name)s-%(filename)s[line:%(lineno)d] - %(levelname)s - %(message)s')
def numToStr(object):
    num1 = round(object, 2)
    # print(num1)
    int1 = int(num1)

    strInt1 = str(int1)
    intStr = strInt1.zfill(2)

    formatStr = format(num1, "00.2f")

    strNum = str(formatStr)

    str1 = formatStr + "“"
    return str1


def toTime(numSec):
    intSec = int(numSec)
    intMin1 = intSec / 60
    intSec1 = intSec % 60
    strSec = str(intSec1)
    strFormatSec = strSec.zfill(2)

    intMin = int(intMin1)

    if intMin < 60:
        strMin1 = str(intMin)
        strMin = strMin1.zfill(2)
        strTime = "00:" + strMin + "'" + strFormatSec + "“"
    else:
        intHour1 = intMin / 60
        intHour = int(intHour1)
        strHour1 = str(intHour)
        strHour = strHour1.zfill(2)
        intMin2 = intMin % 60
        strMin2 = str(intMin2)
        strMin = strMin2.zfill(2)
        strTime = strHour + ":" + strMin + "'" + strFormatSec + "“"

    return strTime


def toRemainStr(numTime):
    intHour = int(numTime)
    strHour1 = str(intHour)
    strHour = strHour1.zfill(2)

    numTime1 = format(numTime, "00.4f")
    strTime1 = str(numTime1)
    strMin1 = strTime1[-4:-2]
    strSec1 = strTime1[-2:]

    strMin = strMin1.zfill(2)
    strSec = strSec1.zfill(2)

    strTime = strHour + ":" + strMin + "'" + strSec + "“"

    return strTime

def getData():
    client = Client("opc.tcp://localuser1568169531271:airfactory1@192.168.102.1:4840") #connect using a user
    client.connect()
    while True:
        try:
            varArburgLoop = client.get_node("ns=1;i=24")
            LoopNumber = varArburgLoop.get_value()

            varArburgRemain = client.get_node("ns=1;i=39")
            timeRemain = varArburgRemain.get_value()
            timeRemainStr = toRemainStr(timeRemain)


            varTimeRound = client.get_node("ns=1;i=29")
            timeRound = varTimeRound.get_value()
            timeRoundStr = numToStr(timeRound)

            # varTimeRoundAvg = client.get_node("ns=2;i=416422")
            # timeRoundAvg = varTimeRoundAvg.get_value()
            # timeRoundAvgStr = numToStr(timeRoundAvg)
            
            totalSec = LoopNumber * timeRound
            totaltimeStr = toTime(totalSec)

            job_good_counter = client.get_node('ns=1;i=25')
            good_value = job_good_counter.get_value()
            if LoopNumber == 0:
                rate_str = '100%'
            else:
                rate = good_value / LoopNumber
                if rate == 0:
                    rate_str = '100%'
                else:
                    rate_str = '{}%'.format(rate)

            wx.CallAfter(pub.sendMessage, 'GetData', number=LoopNumber, totaltime=totaltimeStr, rate_str=rate_str, remainTime=timeRemainStr, currentTime=timeRoundStr)
            time.sleep(1)
        except:
            logging.error(traceback.format_exc())



class GetData(threading.Thread):

    def  __init__(self):
        threading.Thread.__init__(self)
        self.isOpen = False


    def run(self):
       getData()



    def threadOpen(self):
        self.isOpen = True
        self.start()








