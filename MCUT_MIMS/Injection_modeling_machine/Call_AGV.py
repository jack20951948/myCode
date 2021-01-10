from opcua import Client
import paho.mqtt.client as mqtt
import time

# MQTT: For AGV
Broker_IP = "192.168.68.129" 
Broker_Port = 1883 #port
TopicName = "pgv01/target" #TOPIC name
# MQTT: For AGV

# Opcua: For Ejector
client = Client("opc.tcp://localuser1568169531271:airfactory1@192.168.102.1:4840") #connect using a user
'''
opc.tcp: opcua protocol
Ejector1 account: localuser1568169531271
Ejector1 password: airfactory1
Ejector static ip: 192.168.102.1:4840
'''
client.connect()
counter = client.get_node("ns=1;i=24") # number of open time
# Opcua: For Ejector

position = "35680"
counter_number = 0
product_batch = 20 # batch to call AGV

def call(TopName, Broker_IP, Broker_Port, position):
    mqttc = mqtt.Client(clean_session=True)
    mqttc.connect(Broker_IP, Broker_Port)
    mqttc.publish(TopName, position, qos=1)

while True:
    
    if counter_number != counter.get_value(): # avoid recall
        counter_number = counter.get_value()
        print(counter_number)
        
        if counter_number != 0 and counter_number % product_batch == 0 :
            call(TopicName, Broker_IP, Broker_Port, position)
            print("publish", position)

    time.sleep(3)
'''
call(TopicName, Broker_IP, Broker_Port, position)
'''