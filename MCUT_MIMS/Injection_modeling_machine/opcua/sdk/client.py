# -*- coding: UTF-8 –*-
import json
import requests
import paho.mqtt.client as mqtt
import os
import traceback
import time
from apscheduler.schedulers.background import BackgroundScheduler

class MqttClient(object):
    def __init__(self):
        self._token = None
        self._topic = None
        self.client = None
        self.on_message = None
        self.on_connect = None
        self.on_publish = None
        self.connect_data = get_connect_data(get_device_id(), get_secret_key())
        # 启动定时刷新token任务
        self._scheduler = BackgroundScheduler()
        self._scheduler.add_job(self.refresh_token, 'interval', hours=10)
        self._scheduler.start()

    def connect(self,blocking=False):
        # 获取结果中需要的参数
        user = self.connect_data['data']['user']
        pwd = self.connect_data['data']['pwd']
        self._token = self.connect_data['data']['token']
        self._topic = self.connect_data['data']['topic']
        endpoint = self.connect_data['data']['endpoint']
        port = int(self.connect_data['data']['port'])
        device_id = self.connect_data['data']['device_id']
        # mqtt连接
        self.client = mqtt.Client(
            client_id=device_id,
            clean_session=True,
            userdata=None,
            protocol=mqtt.MQTTv311,
            transport="websockets")
        self.client.username_pw_set(user, pwd)  # 设置用户名，密码
        self.client.on_connect = self.call_connect  # 连接后的操作
        self.client.on_publish = self.call_publish  # 发布信息成功后的回调函数
        self.client.on_message = self.call_message  # 接受消息的操作
        self.client.on_disconnect = self.on_disconnect
        self.client.connect(endpoint, port, 60)  # 连接服务 keepalive=60
        if blocking:
            self.client.loop_forever()
        else:
            self.client.loop_start()

    def on_disconnect(self,client, userdata,rc=0):
        is_connect = True
        while is_connect:
            try:
                client.reconnect()
                is_connect = False
            except:
                time.sleep(3)


    def call_publish(self, client, userdata, mid):
        self.on_publish(mid)

    # 发送消息
    def send_data(self, data, payload=None, topic=None, ack=0, **kw):
        # if client is None:
        #     raise Exception('请先连接再发布消息')
        # # 判断token是否为None
        # if token is None:
        #     raise Exception('请先获取连接数据')
        # 如果传了payload,将不在有这些默认值
        replay = {}
        if payload and 'client_id' in payload.keys():
            replay['client_id'] = payload['client_id']
        else:
            replay['token'] = self._token
            replay['ack'] = ack
        replay['device_id'] = get_device_id()
        if kw:
            for k, v in kw.items():
                replay[k] = v
        if data and type(data) is list:
            replay['data'] = {}
            replay['data']['sub_device'] = data
        elif data:
            replay['data'] = data
        if topic:
            self.client.publish(topic, payload=json.dumps(replay), qos=2)
        else:
            self.client.publish(self._topic, payload=json.dumps(replay), qos=2)  # qos

    # 从mqtt接收到的消息接收消息回调
    def call_message(self, client, userdata, msg):
        try:
            payload = msg.payload
            payload_json = json.loads(payload)
            # 校验是否是平台发送的信息，过滤掉自身发布消息后的回调信息
            if 'token' in payload_json.keys() and (payload_json['token'] == 'mqtt:service' or payload_json['token'] == 'mqtt:cloudserviceapp'):
                # 校验设备id
                if payload_json['device_id'] == get_device_id() or len(payload_json['device_id']) == 0:
                    self.on_message(payload_json)
        except:
            traceback.print_exc()

    # mqtt服务连接成功后的回调方法
    def call_connect(self, client, userdata, flags, rc):  # 连接后返回0为成功
        # 连接成功，订阅服务
        self.client.subscribe(self._topic, 2)
        self.on_connect()

    # 断开mqtt连接
    def disconnect(self):
        self.client.disconnect()

    def refresh_token(self):
        try:
            connect_data = get_connect_data(get_device_id(), get_secret_key())
            self._token = connect_data['data']['token']
        except Exception:
            count = 0
            while count < 5:
                try:
                    connect_data = get_connect_data(get_device_id(), get_secret_key())
                    self._token = connect_data['data']['token']
                    count = 5
                except Exception:
                    count += 1
                    time.sleep(60)




def get_connect_data(device_id, secret_key):
    with open(get_current_path() + 'connect.url','r') as f:
        CONNECT_DATA_URL = f.read()
    device_message = {'device_id': device_id, 'secret_key': secret_key}
    for i in range(100):
        try:
            r = requests.post(CONNECT_DATA_URL, data=device_message,timeout=5)
            print(r.text)
            break
        except:
            traceback.print_exc()
    return r.json()


 # 获得设备ID
def get_device_id():
    with open(get_current_path() + 'device.id', mode='r') as device:
        # 本地存在设备信息
        device_id = device.read()
        return device_id

# 获取secret_key
def get_secret_key():
    with open(get_current_path() + 'secret.key', 'r') as cert_file:
        return cert_file.read()

def save_device_id(device_id):
    with open(get_current_path() + 'device.id', 'w') as id_file:
        id_file.write(device_id)


def save_secret_key(self, key):
    with open(self.get_current_path() + 'secret.key', 'w') as cert_file:
        cert_file.write(key)


def get_current_path():
    return os.path.split(os.path.abspath(__file__))[0] + os.path.sep

def on_message(payload_json):
    print(payload_json)

