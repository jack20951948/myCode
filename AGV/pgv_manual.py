#!/usr/bin/python3
# coding=utf-8
import time

import math
import getch

import threading #多线程
import subprocess as sp

import RPi.GPIO as GPIO
from adafruit_servokit import ServoKit
    
class pgv_action():
    def checkSpeed(sp): # 检查避免超出PWM产生器范围
        if sp >= 100:
            sp = 100
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

    def move_forward(final_speed=10, time_constant=10):
        GPIO.output(stopPin, GPIO.LOW)
        GPIO.output(brakePin, GPIO.LOW)

        right_speed = 0
        left_speed = 0

        GPIO.output(rightDirPin, GPIO.LOW)
        GPIO.output(leftDirPin, GPIO.HIGH)

        right_speed = (final_speed-final_speed*(math.exp(-i/time_constant))) - (1/250)*final_speed*pgvData[2]
        left_speed = (final_speed-final_speed*(math.exp(-i/time_constant))) + (1/250)*final_speed*pgvData[2]
        kit.servo[0].angle = pgv_action.checkSpeed(right_speed)
        kit.servo[1].angle = pgv_action.checkSpeed(left_speed)

        time.sleep(0.01)

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

class keyboard():
    def readkeyboard():
        global event
        event = getch.getch().lower()
        if event != "w" and event != "a" and event != "s" and event != "d" and event != "n" and event != "m" and event != "p":
            event = None
    def keyboardLoop():
        while True:
            readkeyboard()

def setup_servoKit():
    global kit
    kit = ServoKit(channels=16)
    kit.servo[0].set_pulse_width_range(0,35500)
    kit.servo[1].set_pulse_width_range(0,35500)
    kit.servo[0].actuation_range = 100
    kit.servo[1].actuation_range = 100
    kit.servo[0].angle = 0
    kit.servo[1].angle = 0

def Setup():
    motor_config()
    GPIO_setting.setup_gpio()
    setup_servoKit()

if __name__ == "__main__":
    Setup()

    readkeyboardThread = threading.Thread(name="readkeyboard", target=keyboard.keyboardLoop)
    readkeyboardThread.start()

    moveMotorsThread = threading.Thread(name="moveMotors", target=pgv_action.goMotorsLoop)
    moveMotorsThread.start()