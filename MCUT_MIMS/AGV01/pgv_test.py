#!/usr/bin/python3
# coding=utf-8
import time
import math

import threading #多线程
import paho.mqtt.client as mqtt #Mqtt

import serial
from bitstring import Bits
import subprocess as sp

import RPi.GPIO as GPIO
from adafruit_servokit import ServoKit

# from pygame import mixer
# mixer.init()

# tripData = [0=startTimeStamp, 1=Target, 2=finishFlag]
tripData = [time.time(), 0, False]

scanTimeStamp = time.time()
# pgvData = [0=which PGV camera,1=XP(shifted),2=YP,3=ANG,4=Error,5=Lost,6=Warn,7=scanTimeStamp, 8=pgv in curve]
pgvData = [1, 0, 0, 0, True, True, True, scanTimeStamp, False]

# Define the curve interval
curve_interval = [[142100, 140700], [139100, 137300], [135700, 134020], [45700, 44000], [51300, 49800], [54800, 52000], [92500, 90400], [98900, 97200]]

class mqtt_client_connection():
    def on_connect(client, userdata, flags, rc):
        print("Connected With Result Code "+rc)

    def on_message(client, userdata, message):
        global mqttTarget
        #print("Message Recieved: "+message.payload.decode())
        mqttTarget.append(int(message.payload.decode()))
        print("\nMQTT Recieved Position: %d" % mqttTarget[-1])
        print("Task List:", mqttTarget)
        #client.disconnect()

    def mqttLoop():
        global client
        while True:
            client.loop()
            #print(mqttTarget)
            
class mqtt_agv2_connection():
    def on_connect(client, userdata, flags, rc):
        print("Connected With Result Code "+rc)

    def on_message(client, userdata, message):
        global mqttFlag
        #print("Message Recieved: "+message.payload.decode())
        recievedCode = int(message.payload.decode())
        if recievedCode == 1:
            mqttFlag = True
        if recievedCode == 0:
            mqttFlag = False
        print("\nMQTT Recieved Flag: %5r" % mqttFlag)
        #client.disconnect()

    def mqttLoop():
        global mqttc
        while True:
            mqttc.loop()
            #print(mqttTarget)
    
class pgv_action():
    def checkSpeed(sp, limit): # 检查避免超出PWM产生器范围
        if limit > 100:
            limit = 100
        if sp >= limit:
            sp = limit
        if sp <= 0:
            sp = 0
        return sp

    def stop_agv(breaker=True):
        GPIO.output(stopPin, GPIO.HIGH)
        kit.servo[0].angle = 0
        kit.servo[1].angle = 0
        if breaker:
            GPIO.output(brakePin, GPIO.HIGH)
        else:
            GPIO.output(brakePin, GPIO.LOW)

    def move_n_step(direction=None, trip=3520, final_speed=10.0, acc=5.0, vel=0.0, time_step=0.01, turn_factor=1/65):
        GPIO.output(brakePin, GPIO.LOW)
        GPIO.output(stopPin, GPIO.LOW)

        if direction.lower() == 'forward':
            pgvData[0] = 0 #设置PGV00开始读取
            GPIO.output(rightDirPin, GPIO.LOW)
            GPIO.output(leftDirPin, GPIO.HIGH)
        elif direction.lower() == 'backward':
            pgvData[0] = 1 #设置PGV01开始读取
            GPIO.output(rightDirPin, GPIO.HIGH)
            GPIO.output(leftDirPin, GPIO.LOW)
        else:
            raise NameError('direction should be either "forward" or "fackward"')
    
        trip /= 35.2
        time_duration = (((acc*trip - (final_speed**2)) / (acc*final_speed)) + (2*final_speed/acc)) / time_step
        dec_time = (((acc*trip - (final_speed**2)) / (acc*final_speed)) + (final_speed/acc)) / time_step

        print('move!')
        for i in range(int(time_duration)):
            if i > dec_time:
                acc = -abs(acc)
            if (vel + acc*time_step) > final_speed: 
                vel = final_speed 
            else: 
                vel = vel + acc*time_step
            right_speed = pgv_action.checkSpeed(vel - turn_factor*final_speed*vel*pgvData[2], final_speed)
            left_speed = pgv_action.checkSpeed(vel + turn_factor*final_speed*vel*pgvData[2], final_speed)
            print("\rtime: %.3f / %.3f, right_vel: %.3f, left_vel: %.3f, y-bias:%.3f" %(time_step*i, time_duration*time_step, right_speed, left_speed, pgvData[2]), end="")
            kit.servo[0].angle = right_speed
            kit.servo[1].angle = left_speed
            time.sleep(time_step)
        print('\nfinish', direction)
        GPIO.output(brakePin, GPIO.HIGH)
        GPIO.output(stopPin, GPIO.HIGH)

    def move_to_position(target_position=0, final_speed=10.0, acc=5.0, vel=0.0, time_step=0.01, turn_factor=5/16):
        GPIO.output(brakePin, GPIO.LOW)
        GPIO.output(stopPin, GPIO.LOW)

        ori_acc = acc
        ori_fin_speed = final_speed
        ori_turn_factor = turn_factor

        while pgvData[1] == 0:
            pass

        if target_position - pgvData[1] > 0: # forward
            direction = "Forward"
            pgvData[0] = 0 #设置PGV00开始读取
            GPIO.output(rightDirPin, GPIO.LOW)
            GPIO.output(leftDirPin, GPIO.HIGH)

        elif target_position - pgvData[1] < 0: # backward
            direction = "Backward"
            pgvData[0] = 1 #设置PGV01开始读取
            GPIO.output(rightDirPin, GPIO.HIGH)
            GPIO.output(leftDirPin, GPIO.LOW)
        print(time.ctime(), ': Setting direction to "{}"...'.format(direction))

        trip = abs(target_position - pgvData[1])
        safe_distance = (0.5 * ((final_speed / acc)) * final_speed )

        print(time.ctime(), ': Begin to move...')
        while (((target_position - pgvData[1]) / 35.2) > 0 and direction == "Forward") or (((target_position - pgvData[1]) / 35.2) < 0 and direction == "Backward"):
            if pgvData[8]:
                acc = 8
                final_speed = 5
                turn_factor = 5/16
            elif (abs(target_position - pgvData[1]) / 35.2) < safe_distance:
                acc = -abs(acc)
                if vel <= 0 and (abs(target_position - pgvData[1]) / 35.2) > 0:
                    acc = 0
                    vel = 3
            else:
                acc = ori_acc
                final_speed = ori_fin_speed
                turn_factor = ori_turn_factor
            
            if (vel + acc*time_step) > final_speed: 
                vel = final_speed 
            else: 
                vel = vel + acc*time_step
            right_speed = pgv_action.checkSpeed(vel - turn_factor*(1/final_speed)*vel*pgvData[2], final_speed)
            left_speed = pgv_action.checkSpeed(vel + turn_factor*(1/final_speed)*vel*pgvData[2], final_speed)
            print("\r%s : trip: %8.2f / %8.2f, target: %6d, safe disdance: %6.2f, right_vel: %6.3f, left_vel: %6.3f, y-bias:%+6.2f, AGV in curve: %5r" %(time.ctime(), abs(target_position - pgvData[1]), trip, target_position, safe_distance*35.2, right_speed, left_speed, pgvData[2], pgvData[8]), end="")
            kit.servo[0].angle = right_speed
            kit.servo[1].angle = left_speed
            time.sleep(time_step)
        print()
        print(time.ctime(), ': Arrived position', target_position)
        GPIO.output(brakePin, GPIO.HIGH)
        GPIO.output(stopPin, GPIO.HIGH)

    def rollUntilGet():
        if GPIO.input(rollerSensorL) == 0 or GPIO.input(rollerSensorR) == 0:
            GPIO.output(rollerRun, GPIO.LOW)
            while GPIO.input(rollerSensorL) == 0 or GPIO.input(rollerSensorR) == 0:
                GPIO.output(rollerDir,GPIO.LOW)
                GPIO.output(rollerRun, GPIO.HIGH)
                time.sleep(0.01)
            tmpTime = time.time()
            while GPIO.input(rollerSensorL) == 1 and GPIO.input(rollerSensorR) == 1:
                pass
            tmpTime = time.time()-tmpTime
            GPIO.output(rollerRun, GPIO.LOW)
            GPIO.output(rollerDir,GPIO.HIGH)
            GPIO.output(rollerRun, GPIO.HIGH)
            time.sleep(tmpTime/2)
            GPIO.output(rollerRun, GPIO.LOW)

    
    def rollUntilRelease():
        GPIO.output(rollerRun, GPIO.LOW)
        while GPIO.input(rollerSensorL) == 1 or GPIO.input(rollerSensorR) == 1:
            GPIO.output(rollerDir,GPIO.HIGH)
            GPIO.output(rollerRun, GPIO.HIGH)
            time.sleep(0.01)
        GPIO.output(rollerRun, GPIO.LOW)
        
    def placeEmptyBox():
        global tripData
        pgv_action.move_to_position(target_position=37360, final_speed=20.0, acc=10.0, turn_factor=1/20)    
        pgv_action.rollUntilGet()
        time.sleep(1)
        pgv_action.move_to_position(target_position=35680, final_speed=20.0, acc=10.0, turn_factor=1/20)
        time.sleep(3)
        pgv_action.rollUntilRelease()
        time.sleep(1)
        pgv_action.move_to_position(target_position=42100, final_speed=20.0, acc=10.0, turn_factor=1/20)


    def pickUpItemToCheck(target=None):
        global tripData
        pgv_action.move_to_position(target_position=target, final_speed=20.0, acc=10.0, turn_factor=1/20)
        pgv_action.rollUntilGet()
        time.sleep(1)
        pgv_action.move_to_position(target_position=37640, final_speed=20.0, acc=10.0, turn_factor=1/20)
        time.sleep(1)
        pgv_action.rollUntilRelease()
        time.sleep(1)
        
    def pickUpItemToStore(target=None):
        global tripData, mqttFlag
        pgv_action.move_to_position(target_position=target, final_speed=20.0, acc=10.0, turn_factor=1/20)
        pgv_action.rollUntilGet()
        time.sleep(1)
        pgv_action.move_to_position(target_position=42100, final_speed=20.0, acc=10.0, turn_factor=1/20)
        time.sleep(1)
        while not(mqttFlag):
            pass
        pgv_action.rollUntilRelease()
        time.sleep(1)

    def goMotorsLoop():
        global tripData, mqttTarget
        
        tripData = [time.time(), mqttTarget.pop(0), False]
        pgv_action.move_to_position(target_position=tripData[1], final_speed=20.0, acc=10.0, turn_factor=1/20)
        tripData[2] = True
        pgv_action.placeEmptyBox()

        while True:
            if not(tripData[2]):
                if tripData[1] == 35680:
                    pgv_action.pickUpItemToCheck(target=tripData[1])
                    pgv_action.placeEmptyBox()
                else:
                    pgv_action.pickUpItemToStore(target=tripData[1])
                tripData[0] = time.time()
                tripData[2] = True
            elif len(mqttTarget) > 0:
                tripData = [time.time(), mqttTarget.pop(0), False]
                print()
            else:
                print("\r%s : Waiting for new tasks..." %(time.ctime()), end="")
        
    # --- move Motors end ---

class pgv_detection():  
    def readPGV(): 
        ser.open()
        # pgvData[0] = 0
        if pgvData[0] == 0:
            ser.write(b'\xc8\x37') #read head 0 # ser.write(b'\xc8\x37') for agv in plant
        else:
            ser.write(b'\xc9\x36') #read head 1 # ser.write(b'\xc9\x36') for agv in plant
        s=ser.read(21)

        ## clean screen
        #tmp=sp.call('clear',shell=True)

        # print(s)
        sHEX=s.hex()
        #print(sHEX)
        #print()
        #print('21bits from PGV head%s' % pgvData[0])
        ## GET PGV ERROR, LOST AND WARNING
        pgvError =  bin(int(sHEX[0:2], 16))[2:].zfill(8)[7:8] != '0'
        #print("PGV Error %r" % pgvError)
        pgvData[4]=pgvError
        pgvLost =  bin(int(sHEX[0:2], 16))[2:].zfill(8)[6:7] != '0'
        #print("PGV Lost: %r" % pgvLost)
        pgvData[5]=pgvLost
        pgvWarn =  bin(int(sHEX[0:2], 16))[2:].zfill(8)[5:6] != '0'
        #print("PGV Warning: %r" %pgvWarn)
        pgvData[6]=pgvWarn
        #print()

        ## GET XP
        ## extract X bytes and convert to binary numbers
        xBytes= bin(int(sHEX[4:12], 16))[2:].zfill(32)

        ## remove useless bit7 = 0 in every byte (0-5,8,16,24)
        ## and use Bits to convert minus (-) bit into int
        XP=Bits(bin=xBytes[5:8]+xBytes[9:16]+xBytes[17:24]+xBytes[25:32]).int

        if pgvData[0] == 0:
            pgvData[1]=XP + pgvHeadShift[0]
        else:
            pgvData[1]=XP + pgvHeadShift[1]
        # print("Position X: %d" % pgvData[1])

        ## GET YP
        ## extract Y bytes and convert to binary numbers
        yBytes=bin(int(sHEX[12:16], 16))[2:].zfill(16)

        ## remove useless bit7 = 0 in every byte (0,8)
        ## and use Bits to convert minus (-) bit into int
        YP=Bits(bin=yBytes[1:8]+yBytes[9:16]).int
        #print("Position Y: %d" % YP)
        pgvData[2]=YP
        ## GET ANG
        ## extract ANG bytes and convert to binary numbers
        angBytes = bin(int(sHEX[20:24], 16))[2:].zfill(16)
        #print(angBytes)
        ANG=int(angBytes[1:8]+angBytes[9:16], 2)
        #print("Position ANG: %d" % ANG)
        pgvData[3]=ANG
        ser.close()
        #print("Scan Speed:")
        #print(pgvData[7] - time.time())

        for curve in curve_interval:
            if curve[0] > pgvData[1] and pgvData[1] > curve[1]:
                pgvData[8] = True
                break
            else:
                pgvData[8] = False
                
        pgvData[7] = time.time()

    def readPGVloop():
        while True:
            pgv_detection.readPGV()

def subscribe_mqtt():
    global mqttTarget, client
    # --- subscribe mqtt begin ---
    #设置 MQTT broker 的 IP 位置（预设为本机树莓派IP位置，固定IP设置在 /etc/dhcpcd.conf
    #或外其他 broker 位置，遥控器也需要设置向同ip发送
    broker_url = "127.0.0.1"
    broker_port = 1883  #设置 MQTT broker 的 port
    mqttTopic = "pgv01/target"  #设置订阅的 topic
    mqttTargetInit = 42100  #设置mqttTarget 的初始值
    mqttTarget = [0,]
    mqttTarget[0] = mqttTargetInit  #定义mqttTarget

    client = mqtt.Client(clean_session=True)
    client.on_connect = mqtt_client_connection.on_connect
    client.on_message = mqtt_client_connection.on_message
    client.connect(broker_url, broker_port)

    client.subscribe(mqttTopic, qos=1)
    # --- subscribe mqtt end ---
    
def subscribe_mqtt_agv2():
    global mqttFlag, mqttc
    # --- subscribe mqtt begin ---
    #设置 MQTT broker 的 IP 位置（预设为本机树莓派IP位置，固定IP设置在 /etc/dhcpcd.conf
    #或外其他 broker 位置，遥控器也需要设置向同ip发送
    broker_url = "127.0.0.1"
    broker_port = 1883  #设置 MQTT broker 的 port
    mqttTopic = "pgv01/storeSignal"  #设置订阅的 topic
    mqttFlag = False

    mqttc = mqtt.Client(clean_session=True)
    mqttc.on_connect = mqtt_agv2_connection.on_connect
    mqttc.on_message = mqtt_agv2_connection.on_message
    mqttc.connect(broker_url, broker_port)

    mqttc.subscribe(mqttTopic, qos=1)
    # --- subscribe mqtt end ---

def motor_config():
    global pgvHeadShift, maxSpeed, minSpeed, safeDistance, correctAngleSpeed, correctYDistanceSpeed, softStartTimer, direction

    # --- motor config
    pgvHeadShift=[0, 0]
    maxSpeed = 15.0
    minSpeed = 3.0
    safeDistance = 300.0
    correctAngleSpeed = 0.001
    correctYDistanceSpeed = 0.08

    softStartTimer = 3
    direction = 1

class GPIO_setting():
    def __setup_motor_pins():
        global GPIO, stopPin, brakePin, rightDirPin, leftDirPin
        ## motor pins setting
        stopPin=17
        brakePin=27
        rightDirPin=22
        leftDirPin=5
        motorPins=[stopPin, brakePin, rightDirPin, leftDirPin]
        GPIO.setup(motorPins, GPIO.OUT)
        GPIO.output(stopPin, GPIO.HIGH)
        GPIO.output(brakePin, GPIO.HIGH)
        GPIO.output(rightDirPin, GPIO.HIGH)
        GPIO.output(leftDirPin, GPIO.LOW)

    def __setup_sensor_pins():
        global GPIO, lidaBackZ1, lidaBackZ3, lidaFrontZ1, lidaFrontZ3, rollerSensorL, rollerSensorR
        ## sensor pins setting
        lidaBackZ1=16
        lidaBackZ3=12
        lidaFrontZ1=20
        lidaFrontZ3=7
        rollerSensorL=8
        rollerSensorR=25
        sensorPins=[lidaBackZ1, lidaBackZ3, lidaFrontZ1, lidaFrontZ3, rollerSensorL, rollerSensorR]
        GPIO.setup(sensorPins, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def __setup_roller_pins():
        global GPIO, rollerRun, rollerDir
        ## roller pins setting
        rollerRun=24
        rollerDir=23
        rollerPins=[rollerRun, rollerDir]
        GPIO.setup(rollerPins, GPIO.OUT)

    def setup_gpio():
        global GPIO
        ## GPIO setting
        GPIO.setmode(GPIO.BCM)
        GPIO_setting.__setup_motor_pins()
        GPIO_setting.__setup_sensor_pins()
        GPIO_setting.__setup_roller_pins()

def setup_servoKit():
    global kit
    kit = ServoKit(channels=16)
    kit.servo[0].set_pulse_width_range(0,35500)
    kit.servo[1].set_pulse_width_range(0,35500)
    kit.servo[0].actuation_range = 100
    kit.servo[1].actuation_range = 100
    kit.servo[0].angle = 0
    kit.servo[1].angle = 0

def rs_485_setup():
    global ser
    # --- read 485 serial PGV begin ---

    # serial initial setting
    ser =serial.Serial()
    ser.baudrate=115200
    ser.port='/dev/ttyUSB0'
    ser.parity='E'
    ser.bytesize=8
    stopbits=1
    timeout=10

    # PGV head initialize
    ser.open()
    ser.write(b'\xec\x13') #PGV head 00 init
    time.sleep(0.3)
    ser.write(b'\xed\x12') #PGV head 01 init
    time.sleep(0.3)
    ser.close()
    print(time.ctime(), ': Serial Port closed...')
    time.sleep(0.3)

    # --- read 485 serial PGV end ---

def Setup():
    subscribe_mqtt()
    subscribe_mqtt_agv2()
    motor_config()
    GPIO_setting.setup_gpio()
    setup_servoKit()
    rs_485_setup()

#mixer.music.load("started.mp3")
#mixer.music.play()

if __name__ == "__main__":
    Setup()

    readPGVThread = threading.Thread(name="readPGV",target=pgv_detection.readPGVloop)
    readPGVThread.start()
    mqttThread = threading.Thread(name="mqttthread", target=mqtt_client_connection.mqttLoop)
    mqttThread.start()
    publishmqttThread = threading.Thread(name="publishmqttThread", target=mqtt_agv2_connection.mqttLoop)
    publishmqttThread.start()
    moveMotorsThread = threading.Thread(name="moveMotors", target=pgv_action.goMotorsLoop)
    moveMotorsThread.start()
