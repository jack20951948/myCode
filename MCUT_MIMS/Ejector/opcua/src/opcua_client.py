# coding:utf-8
from opcua import Client
import time
from sdk import client
import traceback
import os
from apscheduler.schedulers.background import BackgroundScheduler
import Queue
import sys
import threading
import datetime
import sqlite3
import paho.mqtt.client as mqtt
mqtt_client = client.MqttClient()
abs_path = os.path.abspath(os.path.dirname(__file__))
message_queue = Queue.Queue()
last_status = None
conn = sqlite3.connect('opcua.db', isolation_level=None)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS OPCUA(oid INTEGER PRIMARY KEY, checktime TEXT, total INTEGER,status INTEGER)''')
cursor.close()
conn.close()
upload_success = False
def upload():
    global last_status
    global upload_success
    data = {}
    data['checktime'] = time.strftime('%Y-%m-%d %H:%M:%S')
    last_status = opcua_client.get_status()
    data['status'] = last_status
    data['total'] = opcua_client.current_sum
    # with open(abs_path + '/data.txt', 'a') as f:
    #     data['avg_time'] = int(opcua_client.avg_time)
    #     f.write(str(data) + '\n')
    for i in range(12):
        mqtt_client.send_data(data, action='save', ack=1)
        save_database(data)
        time.sleep(5)
        if upload_success:
            upload_success = False
            break



# 保存本地数据库
def save_database(data):
    conn = sqlite3.connect('opcua.db', isolation_level=None)
    cursor = conn.cursor()
    # 判断数据是否超过10万条，超过删除前1万条
    cursor.execute('select count(*) from OPCUA')
    number = int(cursor.fetchone()[0])
    if number >= 100000:
        cursor.execute('delete from OPCUA order by `aid` limit 10000')
    cursor.execute('insert into OPCUA(`checktime`, `total`, `status`) values(?,?,?)',
                       (data['checktime'], data['total'], data['status']))
    cursor.close()
    conn.close()


def get_today_data():
    conn = sqlite3.connect('opcua.db', isolation_level=None)
    today = datetime.datetime.now().replace(minute=0,second=0, microsecond=0) - datetime.timedelta(hours=22)
    cursor = conn.cursor()
    cursor.execute("select `oid`, `checktime`, `total`, `status` from OPCUA where `checktime` >= ? order by `oid`", (str(today),))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    sub_data = []
    for item in rows:
        sub_data.append({'checktime':item[1], 'total':item[2], 'status':item[3]})
    return sub_data


class OpcuaClient:
    def __init__(self):
        self.client = Client('opc.tcp://localuser1568169531271:airfactory1@192.168.102.1:4840')
        self.FREE = 1
        self.RUN = 2
        self.ALARM = 4
        self.STOP = 8
        try:
            self.client.connect()
        except:
            pass
        # 最后一次异常发生的时间
        self.last_alarm_time = None
        # 上一次生产的时间
        self.last_product_time = None
        # 平均时间节点
        # self.avg_time_node = self.client.get_node('ns=2;i=140842')
        self.avg_time_node = self.client.get_node('ns=1;i=29')
        # # 正品数节点
        # self.qualified_node = self.client.get_node('ns=2;i=239002')
        # 开合模次数节点
        self.qualified_node = self.client.get_node('ns=1;i=24')
        # 次品数节点
        # self.defective_goods_node = self.client.get_node('ns=2;i=239022')
        # 获取最后一次警报节点
        self.last_alarm_node = self.client.get_node('ns=0;i=17280')
        alarm_counter = self.last_alarm_node.get_value()
        # 订单总数
        # self.item_count_node = self.client.get_node('ns=2;i=238992')
        # 平均时间
        self.avg_time = self.avg_time_node.get_value()
        self.last_avg_time = self.avg_time_node.get_value()
        self.last_sum = self.qualified_node.get_value()
        self.current_sum = self.qualified_node.get_value()
        self.last_puls_sum = self.last_sum
        self.scheduler = BackgroundScheduler()
        self.scheduler.add_job(upload, 'cron', hour='*')
        self.scheduler.start()

    def get_status(self):
       for i in range(10):
            try:
                # 当前产品总数
                self.current_sum = self.qualified_node.get_value()
                current_time = int(time.time())
                # 判断是否有警报发生
                s = str(self.last_alarm_node.get_data_value())
                if self.last_alarm_time:
                    if self.last_alarm_time != s[s.find('SourceTimestamp'):s.rfind(')')]:
                        self.last_alarm_time = s[s.find('SourceTimestamp'):s.rfind(')')]
                        # with open(abs_path + '/alarm.txt', 'a') as f:
                        #     f.write(s + '\n')
                        return self.ALARM
                else:
                    # 记录最后一次异常的时间
                    self.last_alarm_time = s[s.find('SourceTimestamp'):s.rfind(')')]
                    self.LAST_STATUS = 2
                    self.last_product_time = current_time
                    return self.RUN
                self.avg_time = self.avg_time_node.get_value()
                #有可能获取到平均时间为0，如果都为0，默认为60
                if int(self.avg_time) == 0 and self.last_avg_time:
                    self.avg_time = self.last_avg_time
                else:
                    self.avg_time = 60
                self.last_avg_time = self.avg_time
                if self.last_sum != self.current_sum:
                    self.last_puls_sum = self.last_sum
                    self.last_sum = self.current_sum
                    self.last_product_time = current_time
                    self.LAST_STATUS = self.RUN
                    return self.RUN
                if (current_time - self.last_product_time) > 2 * self.avg_time:
                    self.LAST_STATUS = self.FREE
                    return self.FREE
                # 上述状态都不满足时则认为是轮询时间小于单个产品的平均时间，返回上一次的状态
                return self.LAST_STATUS
            except:
                # 连续5秒内都抛出抛出异常则认为是停机状态
                exc_type, exc_value, exc_tb = sys.exc_info()
                traceback.print_exception(exc_type, exc_value, exc_tb)
                time.sleep(0.5)
                if i == 9:
                    self.LAST_STATUS = self.STOP
                    return self.STOP

    def connect(self):
        try:
            self.client.connect()
        except:
            exc_type, exc_value, exc_tb = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_tb)


opcua_client = OpcuaClient()



def task():
    global last_status
    # 用来判断是否要上传数据的标识
    last_status = opcua_client.get_status()
    # 如果第一次就是停机状态，则上传数据
    if last_status == opcua_client.STOP:
        data = {}
        data['checktime'] = time.strftime('%Y-%m-%d %H:%M:%S')
        data['status'] = opcua_client.STOP
        mqtt_client.send_data(data, action='save')
    replace = True
    while True:
        current_status = opcua_client.get_status()
        # 换单情况上传一次数据
        if (opcua_client.current_sum == 1 or opcua_client.current_sum == 0) and replace:
            data = {}
            last_status = current_status
            data['last_total'] = opcua_client.last_puls_sum
            data['checktime'] = time.strftime('%Y-%m-%d %H:%M:%S')
            data['status'] = current_status
            data['total'] = opcua_client.last_puls_sum
            mqtt_client.send_data(data, action='save')
            save_database(data)
            replace = False
        # 状态变化上传数据
        if last_status != current_status:
            data = {}
            last_status = current_status
            data['last_total'] = opcua_client.last_puls_sum
            data['checktime'] = time.strftime('%Y-%m-%d %H:%M:%S')
            data['status'] = current_status
            data['total'] = opcua_client.current_sum
            while True:
                try:
                    # with open(abs_path + '/data.txt', 'a') as f:
                    #     data['avg_time'] = int(opcua_client.avg_time)
                    #     f.write(str(data) + '\n')
                    mqtt_client.send_data(data, action='save')
                    save_database(data)
                    break
                except:
                    exc_type, exc_value, exc_tb = sys.exc_info()
                    traceback.print_exception(exc_type, exc_value, exc_tb)
                    time.sleep(1)
        if opcua_client.current_sum == 2:
            replace = True
        if current_status == opcua_client.STOP:
            try:
                opcua_client.connect()
            except:
                pass
        time.sleep(2)



def on_message(payload):
    message_queue.put(payload)



def manage_mesaage():
    while True:
        try:
            payload = message_queue.get()
            keys = payload.keys()
            if 'action' in keys:
                data = {}
                if 'read' == payload['action']:
                    data['status'] = opcua_client.get_status()
                    data['total'] = opcua_client.current_sum
                    data['checktime'] = time.strftime('%Y-%m-%d %H:%M:%S')
                    mqtt_client.send_data(data, payload)
                if 'get_today' == payload['action']:
                    data['sub_data'] = get_today_data()
                    mqtt_client.send_data(data, payload,action='get_today')
                if 'ack' == payload['action'] and client.get_device_id() == payload['device_id']:
                    if int(payload['data']['status']) > 0:
                        global upload_success
                        upload_success = True
        except:
            exc_type, exc_value, exc_tb = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_tb)


def init_mqtt_client():
    mqtt_client.on_message = on_message
    mqtt_client.connect()
    task = threading.Thread(target=manage_mesaage)
    task.start()


def start():
    t = threading.Thread(target=task)
    t.start()
    init_mqtt_client()


if __name__ == '__main__':
    start()