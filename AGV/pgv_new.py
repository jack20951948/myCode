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

from pygame import mixer
mixer.init()

# --- Demo loop running begin ---
## [0= True will continue demo running. 1= demoTrips stop positions
demoData = [True, 0]
#station
#from big 
demoTrips = [38480,36140,38480,32740,38480,29720]

# tripData = [0=direction, 1=Target, 2=startTimeStamp, 3=pauseFlag, 4=rollingFlag ]
tripData = [0, 0,time.time(), False, False ]

scanTimeStamp = time.time()
# pgvData = [0=which PGV camera,1=XP(shifted),2=YP,3=ANG,4=Error,5=Lost,6=Warn,7=scanTimeStamp]
pgvData = [1, 0, 0, 0, True, True, True, scanTimeStamp]

class demo_setting():
    def nextDemoTrip():
        if demoData[1]==len(demoTrips)-1:
            demoData[1]=0
        else:
            demoData[1]+=1

    def demoLoop():
        if demoData[0]==True:
            if mqttTarget[0]==demoTrips[demoData[1]]:
                demo_setting.nextDemoTrip() # 略过重复的站点
            mqttTarget[0] = demoTrips[demoData[1]]
            print('set new demo destination %d' % demoTrips[demoData[1]])
            demo_setting.nextDemoTrip()
            time.sleep(1)
    # --- Demo loop running end ---

class mqtt_client_connection():
    def on_connect(client, userdata, flags, rc):
        print("Connected With Result Code "+rc)

    def on_message(client, userdata, message):
        #global mqttTarget
        #print("Message Recieved: "+message.payload.decode())
        mqttTarget[0] = int(message.payload.decode())
        print("MQTT Recieved: %d" % mqttTarget[0])
        #client.disconnect()

    def mqttLoop():
        global client
        while True:
            client.loop()
            #print(mqttTarget)
    
class pgv_action():
    # --- Roller begin ---
    def rolling():
        print('Rolling Start')
        direction = 0
        GPIO.output(rollerRun, GPIO.HIGH)
        GPIO.output(rollerDir,GPIO.LOW)
        rollingTimeStamp = time.time()
        while time.time()-rollingTimeStamp < 10:
            # print(GPIO.input(rollerSensorL))
            if GPIO.input(rollerSensorL) == 1 :
                GPIO.output(rollerRun, GPIO.LOW)
                GPIO.output(rollerDir,GPIO.HIGH)
                #time.sleep(1.0)
                GPIO.output(rollerRun, GPIO.HIGH)
                time.sleep(08.01)

            else :
                GPIO.output(rollerRun, GPIO.LOW)
                GPIO.output(rollerDir,GPIO.LOW)
                #time.sleep(1.0)
                GPIO.output(rollerRun, GPIO.HIGH)
                time.sleep(14.45)
        GPIO.output(rollerRun, GPIO.LOW)
    # --- roller end ---

    def setTrip():
        if mqttTarget[0] != tripData[1]: #if have new mqttTarget
            tripData[1] = mqttTarget[0]
            tripData[2] = time.time() # reset the start softStartTimer
            tripData[3]=True
            tripData[4]=False
            if tripData[1] > pgvData[1]: # if the direction is forward
                tripData[0] = 0
                pgvData[0]=0 #设置PGV00开始读取
            else: # if the direction is backward
                tripData[0] = 1
                pgvData[0]=1 #设置PGV01开始读取

    def checkSpeed(sp): # 检查避免超出PWM产生器范围
        if sp >= 100:
            sp = 100
        if sp <= 0:
            sp = 0
        return sp

    def goMotors():
        elapsedTime = time.time() - tripData[2]     #soft start
        if elapsedTime > softStartTimer:
            softStartSpeed = maxSpeed
        if elapsedTime <= softStartTimer:
            softStartSpeed = elapsedTime/softStartTimer*(maxSpeed-minSpeed)+minSpeed
        # if lost
        if pgvData[4] or pgvData[5]:
            GPIO.output(stopPin, GPIO.HIGH)
            GPIO.output(brakePin, GPIO.HIGH)
            safeSpeed = 0
        else:
            GPIO.output(stopPin, GPIO.LOW)
            GPIO.output(brakePin, GPIO.LOW)
            safeSpeed = maxSpeed

        #if go forward
        if tripData[0] == 0:
            GPIO.output(rightDirPin, GPIO.LOW)
            GPIO.output(leftDirPin, GPIO.HIGH)
            GPIO.output(brakePin, GPIO.LOW)

            distance = tripData[1]-pgvData[1]
            if distance > safeDistance:
                baseSpeed = maxSpeed
            elif distance <= safeDistance:
                baseSpeed = (maxSpeed-minSpeed)*(distance/safeDistance)+minSpeed

            speed = min(baseSpeed,safeSpeed,softStartSpeed)
            rightSpeed = speed - correctYDistanceSpeed*pgvData[2]
            leftSpeed = speed + correctYDistanceSpeed*pgvData[2]

        #if go backward
        if tripData[0] == 1:
            GPIO.output(rightDirPin, GPIO.HIGH)
            GPIO.output(leftDirPin, GPIO.LOW)
            GPIO.output(brakePin, GPIO.LOW)

            distance = pgvData[1]-tripData[1]
            if distance > safeDistance:
                baseSpeed = maxSpeed
            elif distance <= safeDistance:
                baseSpeed = (maxSpeed-minSpeed)*(distance/safeDistance)+minSpeed
            if distance <= 0:
                baseSpeed = 0
            speed = min(baseSpeed,safeSpeed,softStartSpeed)
            rightSpeed = speed - correctYDistanceSpeed*pgvData[2]
            leftSpeed = speed + correctYDistanceSpeed*pgvData[2]

        if distance <= 0:
            rightSpeed = 0
            leftSpeed = 0
            GPIO.output(brakePin, GPIO.HIGH)
            if tripData[4] == False:
                pgv_action.rolling()
                tripData[4] = True
                demo_setting.demoLoop()

        if tripData[3] == True:
            rightSpeed=0
            leftSpeed=0
            tripData[3] = False
            print('Pause finish')

        #print(distance)
        #print(pgvData)
        #print(tripData)
        #print(mqttTarget)
        # print(rightSpeed, leftSpeed)
        kit.servo[0].angle = pgv_action.checkSpeed(rightSpeed)
        kit.servo[1].angle = pgv_action.checkSpeed(leftSpeed)

    def stop_agv(breaker=True):
        GPIO.output(stopPin, GPIO.HIGH)
        kit.servo[0].angle = 0
        kit.servo[1].angle = 0
        if breaker:
            GPIO.output(brakePin, GPIO.HIGH)
        else:
            GPIO.output(brakePin, GPIO.LOW)

    def move_n_step(direction='forward', step=200, final_speed=10, time_constant=10): # 5*time_constant = step when agv arrive final speed
        GPIO.output(stopPin, GPIO.LOW)
        GPIO.output(brakePin, GPIO.LOW)

        right_speed = 0
        left_speed = 0

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

        for i in range(int(step/2)):
            try:
                right_speed = (final_speed-final_speed*(math.exp(-i/time_constant))) - (1/250)*final_speed*pgvData[2]
                left_speed = (final_speed-final_speed*(math.exp(-i/time_constant))) + (1/250)*final_speed*pgvData[2]
                kit.servo[0].angle = pgv_action.checkSpeed(right_speed)
                kit.servo[1].angle = pgv_action.checkSpeed(left_speed)
            except Exception as e:
                print(e)
                print("stop agv!")
                pgv_action.stop_agv()

            time.sleep(0.01)
        for i in range(int(step/2)):
            try:
                right_speed = (final_speed*(math.exp(-i/time_constant))) - (1/250)*final_speed*pgvData[2]
                left_speed = (final_speed*(math.exp(-i/time_constant))) + (1/250)*final_speed*pgvData[2]
                kit.servo[0].angle = pgv_action.checkSpeed(right_speed)
                kit.servo[1].angle = pgv_action.checkSpeed(left_speed)
            except Exception as e:
                print(e)
                print("stop agv!")
                pgv_action.stop_agv()

            time.sleep(0.01)

    def move_to_position(traget_position=0, final_speed=10, time_constant=10, safe_distance=100):
        GPIO.output(stopPin, GPIO.LOW)
        GPIO.output(brakePin, GPIO.LOW)

        # print('read pgv')
        # pgv_detection.readPGV()
        # print('read complete')

        right_speed = 0
        left_speed = 0

        if traget_position - pgvData[1] > 0:
            pgvData[0] = 0 #设置PGV00开始读取
            GPIO.output(rightDirPin, GPIO.LOW)
            GPIO.output(leftDirPin, GPIO.HIGH)

        elif traget_position - pgvData[1] < 0:
            pgvData[0] = 1 #设置PGV01开始读取
            GPIO.output(rightDirPin, GPIO.HIGH)
            GPIO.output(leftDirPin, GPIO.LOW)

        else:
            pgv_action.stop_agv()

        time_step = 0

        while abs(traget_position - pgvData[1]) > safe_distance:
            try:
                right_speed = (final_speed-final_speed*(math.exp(-time_step/time_constant))) - (1/250)*final_speed*pgvData[2]
                left_speed = (final_speed-final_speed*(math.exp(-time_step/time_constant))) + (1/250)*final_speed*pgvData[2]
                kit.servo[0].angle = pgv_action.checkSpeed(right_speed)
                kit.servo[1].angle = pgv_action.checkSpeed(left_speed)
            except Exception as e:
                print(e)
                print("stop agv!")
                pgv_action.stop_agv()

            time.sleep(0.01)
            time_step += 1

        while abs(traget_position - pgvData[1]) <= safe_distance:
            if abs(traget_position - pgvData[1]) <= 0:
                pgv_action.stop_agv()

            try:
                right_speed = (final_speed*(math.exp(-time_step/time_constant))) - (1/250)*final_speed*pgvData[2]
                left_speed = (final_speed*(math.exp(-time_step/time_constant))) + (1/250)*final_speed*pgvData[2]
                kit.servo[0].angle = pgv_action.checkSpeed(right_speed)
                kit.servo[1].angle = pgv_action.checkSpeed(left_speed)
            except Exception as e:
                print(e)
                print("stop agv!")
                pgv_action.stop_agv()

            time.sleep(0.01)
            time_step += 1
    
    def rolling_test():
        # print('Rolling Start')
        direction = 0
        GPIO.output(rollerRun, GPIO.HIGH)
        GPIO.output(rollerDir,GPIO.LOW)
        # print(GPIO.input(rollerSensorL))
        if GPIO.input(rollerSensorL) == 1 :
            print("rolling reverse!")
            GPIO.output(rollerRun, GPIO.LOW)
            GPIO.output(rollerDir,GPIO.HIGH)
            #time.sleep(1.0)
            GPIO.output(rollerRun, GPIO.HIGH)
            time.sleep(0.01)

        else :
            GPIO.output(rollerRun, GPIO.LOW)
            GPIO.output(rollerDir,GPIO.LOW)
            #time.sleep(1.0)
            GPIO.output(rollerRun, GPIO.HIGH)
            time.sleep(0.01)
        GPIO.output(rollerRun, GPIO.LOW)

    def goMotorsLoop():
        global kit
        while True:
            break
            pgv_action.setTrip()
            pgv_action.goMotors()

        # print('move!')
        # for i in range(2):
        #     if i == 1:
        #         pgv_action.move_n_step(direction='forward', step=1000, final_speed=10, time_constant=20)
        #     else:
        #         pgv_action.move_n_step(direction='backward', step=1000, final_speed=10, time_constant=20)

        #     pgv_action.stop_agv(breaker=False)
        #     time.sleep(3)
        # print('stop!')

        print('move!')
        while pgvData[1] == 0:
            # break
            pass
        pgv_action.move_to_position(traget_position=38360)

        
        print('Rolling Start')
        while True:
            break
            pgv_action.rolling_test()

    # --- move Motors end ---

class pgv_detection:  
    def readPGV(): 
        ser.open()
        if pgvData[0] == 0:
            ser.write(b'\xc8\x37') #read head 0
        else:
            ser.write(b'\xc9\x36') #read head 1
        s=ser.read(21)

        ## clean screen
        #tmp=sp.call('clear',shell=True)

        #print(s)
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
        #print("Position X: %d" % pgvData[1])

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
    mqttTargetInit = 600  #设置mqttTarget 的初始值
    mqttTarget = [0,]
    mqttTarget[0] = mqttTargetInit  #定义mqttTarget

    client = mqtt.Client(clean_session=True)
    client.on_connect = mqtt_client_connection.on_connect
    client.on_message = mqtt_client_connection.on_message
    client.connect(broker_url, broker_port)

    client.subscribe(mqttTopic, qos=0)
    # --- subscribe mqtt end ---

def motor_config():
    global pgvHeadShift, maxSpeed, minSpeed, safeDistance, correctAngleSpeed, correctYDistanceSpeed, softStartTimer, direction

    # --- motor config
    pgvHeadShift=[72, 511]
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
    print('ser closed')
    time.sleep(0.3)

    # --- read 485 serial PGV end ---

def Setup():
    subscribe_mqtt()
    motor_config()
    GPIO_setting.setup_gpio()
    setup_servoKit()
    rs_485_setup()

#mixer.music.load("started.mp3")
#mixer.music.play()

if __name__ == "__main__":
    Setup()

    moveMotorsThread = threading.Thread(name="moveMotors", target=pgv_action.goMotorsLoop)
    moveMotorsThread.start()
    readPGVThread = threading.Thread(name="readPGV",target=pgv_detection.readPGVloop)
    readPGVThread.start()
    mqttThread = threading.Thread(name="mqttthread", target=mqtt_client_connection.mqttLoop)
    mqttThread.start()