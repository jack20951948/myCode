# AGV & Python tutorial
## Basic Python knowledge
1. List
    - A list is a collection which is **ordered** and **changeable**. In Python lists are written with square brackets.
        - example:
            ```python=
            ls = [1, 2, 'a', [3, 4]]
            ```

        - method of list:
            ```python=
            print(ls)

            print(ls[2])

            print(ls[0:3])

            print(ls[-1])

            print(ls[3][1])
            ```
        - output:
            ```!
            [1, 2, 'a', [3, 4]]

            a

            [1, 2, 'a']

            [3, 4]

            4
            ```

2. `If` statement
    - prototype:
        ```python=
        if [CONDITION 1]:
            [what to do if condition 1 is true]
        elif [CONDITION 2]:
            [what to do if condition 2 is true]
        else:
            [what to do if none of the CONDITION above is true]
        ```
    - example:
        ```python=
        a = 200
        b = 33

        if b > a:
            print("b is greater than a")
        elif a == b:
            print("a and b are equal")
        else:
            print("a is greater than b")
        ```

    - output:
        ```!
        a is greater than b
        ```

3. `while` Loops
    - With the while loop we can execute a set of statements as long as a condition is `true`.
        - prototype:
            ```python=
            while [CONDITION]:
                [Loop will repeatly execute until the condition becomes False]
            ```
        - example:
            ```python=
            i = 1
            while i < 6:
                print(i)
                i += 1
            ```

        - output:
            ```!
            1
            2
            3
            4
            5
            ```

    - The break Statement
        - With the break statement we can stop the loop even if the while condition is `true`:
        - example:
            ```python=
            i = 1
            while i < 6:
                print(i)
                if i == 3:
                    break
                i += 1
            ```

        - output:
            ```!
            1
            2
            3
            ```

4. `For` Loops
    - A for loop is used for iterating over a sequence (that is either a list, a tuple, a dictionary, a set, or a string).
        - prototype:
            ```python=
            for [VARIBLE] in [SEQUENCE]:
                [Loop runs as the VARIBLE go through all the items]
            ```
        - example:
            ```python=
            fruits = ["apple", "banana", "cherry"]
            for x in fruits:
                print(x)
            ```

        - output:
            ```!
            apple
            banana
            cherry
            ```

    - The `range()` Function
        - The `range()` function returns a sequence of numbers, starting from 0 by default, and increments by 1 (by default), and ends at a specified number.
        - example:
            ```python=
            a = range(4)
            b = range(2, 6)
            c = range(3, 9, 2)

            print('a:', a)
            print('b:', b)
            print('c:', c)
            ```

        - output:
            ```!
            a: [0, 1, 2, 3]
            b: [2, 3, 4, 5]
            c: [3, 5, 7]
            ```
    - use `range()` function in `for` loop
        - example:
            ```python=
            for i in range(2, 20, 3):
                print(i) 
            ```

        - output:
            ```!
            2
            5
            8
            11
            14
            17
            ```
    - Nested Loops
        - A nested loop is a loop inside a loop. The "inner loop" will be executed one time for each iteration of the "outer loop":

        - example:
            ```python=
            adj = ["red", "big", "tasty"]
            fruits = ["apple", "banana", "cherry"]

            for x in adj:
                for y in fruits:
                    print(x, y)
            ```

        - output:
            ```!
            red apple
            red banana
            red cherry
            big apple
            big banana
            big cherry
            tasty apple
            tasty banana
            tasty cherry
            ```

5. Creating a Function `def`
    1. A function is a block of code which only runs when it is called.

    2. You can pass data, known as parameters, into a function.

    3. A function can return data as a result.
    
    - Calling a Function
        - example:
            ```python=
            def my_function():
                print("Hello from a function")

            my_function()
            ```

        - output:
            ```!
            Hello from a function
            ```

    - Calling with arguments
        - example:
            ```python=
            def my_function(fname):
                print(fname + " Refsnes")

            my_function("Emil")
            my_function("Tobias")
            my_function("Linus")
            ```

        - output:
            ```!
            Emil Refsnes
            Tobias Refsnes
            Linus Refsnes
            ```
        - you can call with multi-arguments:
            ```python=
            def my_function(fname, lname):
                print(fname + " " + lname)

            my_function("Emil", "Refsnes")
            ```

        - output:
            ```!
            Emil Refsnes
            ```
    - Keyword Arguments
        - You can also send arguments with the key = value syntax. This way the order of the arguments does not matter.
            ```python=
            def my_function(child3, child2, child1):
                print("The youngest child is " + child3)

            my_function(child1="Emil", child2="Tobias", child3="Linus")
            ```

        - output:
            ```!
            The youngest child is Linus
            ```

    - Default Parameter Value
        - The following example shows how to use a default parameter value. If we call the function without argument, it uses the default value:
            ```python=
            def my_function(country = "Norway"):
                print("I am from " + country)

            my_function("India")
            my_function()
            my_function("Brazil")
            ```

        - output:
            ```!
            I am from India
            I am from Norway
            I am from Brazil
            ```

    - Return Values
        - To let a function return a value, use the `return` statement:
            ```python=
            def my_function(x):
                return 5 * x

            a = my_function(3)
            b = my_function(5)

            print(a)
            print(b)
            print(my_function(9))
            ```

        - output:
            ```!
            15
            25
            45
            ```

6. Python Classes/Objects
    - Python is an object oriented programming language. Almost everything in Python is an object, with its properties and methods. A Class is like an object constructor, or a "blueprint" for creating objects.

        - Example:
            ```python=
            class Person:
                def __init__(self, name, age):
                    self.name = name
                    self.age = age

            p1 = Person("John", 36)

            print(p1.name)
            print(p1.age)
            ```

        - output:
            ```!
            John
            36
            ```

    - use multiple `class` to identify the function
        - Example:
            ```python=
            class Name:
                def my_function(name):
                    print("My name is" + name)


            class Country:
                def my_function(country = "Norway"):
                    print("I am from " + country)

            Name.my_function('John')
            Country.my_function('USA')
            ```

        - output:
            ```!
            John
            36
            ```

7. Try Except

    - The `try` block lets you test a block of code for errors.

    - The `except` block lets you handle the error.

    - THE `else` block lets you execute code, only any except error.

    - The `finally` block lets you execute code, regardless of the result of the try- and except blocks.

        - Example:
            ```python=
            def print_value(num):
                try:
                    print(num)
                except:
                    print('something error!')
                else:
                    print('print success!')
                finally:
                    print('function end!')


            ls = range(6) # [0, 1, 2, 3, 4, 5]

            print(ls[0])
            print("-------")
            print(ls[7])
            ```

        - output:
            ```!
            0
            print success!
            function end!
            -------
            something error!
            function end!
            ```

## AGV navigation
- Using `main()` loop
    1. `main()`
        ```python=
        def a_function():
            print('this is function a')

        def b_function():
            print('this is function b')

        def main():
            print('this is the main code')
            a_funcyion()
            b_function()

        main()
        ```

    2. `if __name__ == "__main__":`
        ```python=
        def a_function():
            print('this is function a')

        def b_function():
            print('this is function b')

        if __name__ == "__main__":
            print('this is the main code')
            a_funcyion()
            b_function()
        ```
    3. combine the two:
        ```python=
        def a_function():
            print('this is function a')

        def b_function():
            print('this is function b')

        def main():
            print('this is the main code')
            a_funcyion()
            b_function()

        if __name__ == "__main__":
            main()
        ```
    - new_pgv.py:
        ```python=
                                            .
                                            .
                                            .
                print('ser closed')
            time.sleep(0.3)

            # --- read 485 serial PGV end ---

        def Setup():
            subscribe_mqtt()
            motor_config()
            GPIO_setting.setup_gpio()
            setup_servoKit()
            rs_485_setup()

        if __name__ == "__main__":
            Setup()

            moveMotorsThread = threading.Thread(name="moveMotors", 
                                            target=pgv_action.goMotorsLoop)
            
            readPGVThread = threading.Thread(name="readPGV",
                                            target=pgv_detection.readPGVloop)
            
            mqttThread = threading.Thread(name="mqttthread", 
                                    target=mqtt_client_connection.mqttLoop)

            moveMotorsThread.start()
            readPGVThread.start()
            mqttThread.start()
        ```
- `Setup()`
    - for setting up the MQTT connection, GPIO, rs485, wheels of Servo and perameter of the AGV.
    ```python=
    def Setup():
        subscribe_mqtt()
        motor_config()
        GPIO_setting.setup_gpio()
        setup_servoKit()
        rs_485_setup()
    ```
    1. `subscribe_mqtt()`: setting the ip, port, of the Broker. define the Topic.
        ```python=
        def subscribe_mqtt():
            global mqttTarget, client

            broker_url = "127.0.0.1"
            broker_port = 1883  
            mqttTopic = "pgv01/target" 
            mqttTargetInit = 600 
            mqttTarget = [0,]
            mqttTarget[0] = mqttTargetInit

            client = mqtt.Client(clean_session=True)
            client.on_connect = mqtt_client_connection.on_connect
            client.on_message = mqtt_client_connection.on_message
            client.connect(broker_url, broker_port)

            client.subscribe(mqttTopic, qos=0)
        ```
    2. `motor_config()`: for setting up some perameter of the motor, ex: speed, accleration
        ```python=
        def motor_config():
            global pgvHeadShift, maxSpeed, minSpeed, safeDistance, correctAngleSpeed, correctYDistanceSpeed, softStartTimer, direction

            pgvHeadShift=[72, 511]
            maxSpeed = 15.0
            minSpeed = 3.0
            safeDistance = 300.0
            correctAngleSpeed = 0.001
            correctYDistanceSpeed = 0.08

            softStartTimer = 3
            direction = 1
        ```
    3. `GPIO_setting.setup_gpio()`
        ```python=
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
        ```
    4. `setup_servoKit()`: set up the servos on the wheels
        ```python=
        def setup_servoKit():
            global kit
            kit = ServoKit(channels=16)
            kit.servo[0].set_pulse_width_range(0,35500)
            kit.servo[1].set_pulse_width_range(0,35500)
            kit.servo[0].actuation_range = 100
            kit.servo[1].actuation_range = 100
            kit.servo[0].angle = 0
            kit.servo[1].angle = 0
        ```
    5. `rs_485_setup()`: set up the rs485 serial for the pgv detector
        ```python=
        def rs_485_setup():
            global ser

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
        ```
- `mqtt_client_connection.mqttLoop()`
    - recieve the data through MQTT
    ```python=
    class mqtt_client_connection():
        def on_connect(client, userdata, flags, rc):
            print("Connected With Result Code "+rc)

        def on_message(client, userdata, message):
            mqttTarget[0] = int(message.payload.decode())
            print("MQTT Recieved: %d" % mqttTarget[0])

        def mqttLoop():
            global client
            while True:
                client.loop()
    ```

- `pgv_detection.readPGVloop()`
    - recieve the data from pgv detector
    ```python=
    class pgv_detection:  
        def readPGV(): 
            ser.open()
            if pgvData[0] == 0:
                ser.write(b'\xc8\x37') #read head 0
            else:
                ser.write(b'\xc9\x36') #read head 1

            s=ser.read(21)
            sHEX=s.hex()

            ## GET PGV ERROR, LOST AND WARNING
            pgvError =  bin(int(sHEX[0:2], 16))[2:].zfill(8)[7:8] != '0'
            pgvData[4]=pgvError
            pgvLost =  bin(int(sHEX[0:2], 16))[2:].zfill(8)[6:7] != '0'
            pgvData[5]=pgvLost
            pgvWarn =  bin(int(sHEX[0:2], 16))[2:].zfill(8)[5:6] != '0'
            pgvData[6]=pgvWarn

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

            ## GET YP
            ## extract Y bytes and convert to binary numbers
            yBytes=bin(int(sHEX[12:16], 16))[2:].zfill(16)

            ## remove useless bit7 = 0 in every byte (0,8)
            ## and use Bits to convert minus (-) bit into int
            YP=Bits(bin=yBytes[1:8]+yBytes[9:16]).int
            pgvData[2]=YP

            ## GET ANG
            ## extract ANG bytes and convert to binary numbers
            angBytes = bin(int(sHEX[20:24], 16))[2:].zfill(16)

            ANG=int(angBytes[1:8]+angBytes[9:16], 2)

            pgvData[3]=ANG
            ser.close()

            pgvData[7] = time.time()

        def readPGVloop():
            while True:
                pgv_detection.readPGV()
    ```
- `pgv_action.goMotorsLoop()`
    - AGV navigation main loop
    ```python=
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

            print('move!')
            for i in range(2):
                if i == 1:
                    pgv_action.move_n_step(direction='forward', step=1000, final_speed=10, time_constant=20)
                else:
                    pgv_action.move_n_step(direction='backward', step=1000, final_speed=10, time_constant=20)

                pgv_action.stop_agv(breaker=False)
                time.sleep(3)
            print('stop!')

            print('move!')
            while pgvData[1] == 0:
                pass
            pgv_action.move_to_position(traget_position=38360)

            
            print('Rolling Start')
            pgv_action.rolling_test()
    ```