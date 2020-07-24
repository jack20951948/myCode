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

    def move_forward(final_speed=10, time_constant=10, acc=1):
        GPIO.output(stopPin, GPIO.LOW)
        GPIO.output(brakePin, GPIO.LOW)

        GPIO.output(rightDirPin, GPIO.LOW)
        GPIO.output(leftDirPin, GPIO.HIGH)

        if right_speed < final_speed:
            right_speed += acc
        if left_speed < final_speed:
            left_speed += acc
        kit.servo[0].angle = pgv_action.checkSpeed(right_speed)
        kit.servo[1].angle = pgv_action.checkSpeed(left_speed)

        time.sleep(0.01)

    def move_backward(final_speed=10, time_constant=10, acc=1):
        GPIO.output(stopPin, GPIO.LOW)
        GPIO.output(brakePin, GPIO.LOW)

        GPIO.output(rightDirPin, GPIO.HIGH)
        GPIO.output(leftDirPin, GPIO.LOW)

        if right_speed < final_speed:
            right_speed += acc
        if left_speed < final_speed:
            left_speed += acc
        kit.servo[0].angle = pgv_action.checkSpeed(right_speed)
        kit.servo[1].angle = pgv_action.checkSpeed(left_speed)

        time.sleep(0.01) 

    def move_left(final_speed=10, time_constant=10, acc=1):
        GPIO.output(stopPin, GPIO.LOW)
        GPIO.output(brakePin, GPIO.LOW)

        GPIO.output(rightDirPin, GPIO.HIGH)
        GPIO.output(leftDirPin, GPIO.LOW)

        if right_speed < final_speed:
            right_speed += acc
        if left_speed < (final_speed / 2):
            left_speed += (acc / 2)
        kit.servo[0].angle = pgv_action.checkSpeed(right_speed)
        kit.servo[1].angle = pgv_action.checkSpeed(left_speed)

        time.sleep(0.01) 

    def move_right(final_speed=10, time_constant=10, acc=1):
        GPIO.output(stopPin, GPIO.LOW)
        GPIO.output(brakePin, GPIO.LOW)

        GPIO.output(rightDirPin, GPIO.HIGH)
        GPIO.output(leftDirPin, GPIO.LOW)

        if right_speed < (final_speed / 2):
            right_speed += (acc / 2)
        if left_speed < final_speed:
            left_speed += acc
        kit.servo[0].angle = pgv_action.checkSpeed(right_speed)
        kit.servo[1].angle = pgv_action.checkSpeed(left_speed)

        time.sleep(0.01) 
    
    def rolling_L():
        GPIO.output(rollerRun, GPIO.HIGH)
        GPIO.output(rollerDir,GPIO.LOW)

        GPIO.output(rollerRun, GPIO.LOW)
        GPIO.output(rollerDir,GPIO.HIGH)
        GPIO.output(rollerRun, GPIO.HIGH)
        time.sleep(0.01)

    def rolling_R():
        GPIO.output(rollerRun, GPIO.LOW)
        GPIO.output(rollerDir,GPIO.LOW)
        GPIO.output(rollerRun, GPIO.HIGH)
        time.sleep(0.01)

    def goMotorsLoop():
        global kit, right_speed, left_speed

        right_speed = 0
        left_speed = 0

        print('move!')
        while True:
            if event == 'p':
                pgv_action.stop_agv()
            elif event == 'w':
                pgv_action.move_forward()
            elif event == 's':
                pgv_action.move_backward()
            elif event == 'a':
                pgv_action.move_left()
            elif event == 'd':
                pgv_action.move_right()
            else:
                GPIO.output(rollerRun, GPIO.LOW)
                if right_speed > 0:
                    right_speed -= 0.5
                if left_speed > 0:
                    left_speed -= 0.5

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