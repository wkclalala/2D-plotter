
# Authors: Kaichen Wei(kw573) & Zehua Yuan(zy393)
# Lab3
# blink.py
# Date: Nov 2, 2019
# Thie function is used to make the LED blink
# at the frequency of 0.5 Hz, which means it
# turn on for 1 second and turn off for 1 second in a cycle

import RPi.GPIO as GPIO 
import time
import os
import subprocess
import math
import threading

 
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

control_pin = [4, 5, 6, 17]
control_pin_2 = [23, 24, 25, 18]
control_pin_3 = [12, 16, 20, 21]
# Set the GPIO 19 as the output pin
for pin in control_pin:
    GPIO.setup(pin,GPIO.OUT)
    GPIO.output(pin,0)

for pin in control_pin_2:
    GPIO.setup(pin,GPIO.OUT)
    GPIO.output(pin,0)
    
for pin in control_pin_3:
    GPIO.setup(pin,GPIO.OUT)
    GPIO.output(pin,0)
    

seq = [ [1,0,0,0],
        [1,1,0,0],
        [0,1,0,0],
        [0,1,1,0],
        [0,0,1,0],
        [0,0,1,1],
        [0,0,0,1],
        [1,0,0,1],]
    
def rotate(step, direction,speed):
    for i in range(step):
        for halfstep in range(8):
            for pin in range(4):
                if(direction==True):
                    GPIO.output(control_pin[pin],seq[halfstep][pin])
                else:
                    GPIO.output(control_pin[pin],seq[7-halfstep][pin])
            time.sleep(speed)
            

def rotate_2(step, direction,speed):
    for i in range(step):
        for halfstep in range(8):
            for pin in range(4):
                if(direction==True):
                    GPIO.output(control_pin_2[pin],seq[halfstep][pin])
                else:
                    GPIO.output(control_pin_2[pin],seq[7-halfstep][pin])
            time.sleep(speed)
            

def rotate_3(step, direction,speed):
    for i in range(step):
        for halfstep in range(8):
            for pin in range(4):
                if(direction==True):
                    GPIO.output(control_pin_3[pin],seq[halfstep][pin])
                else:
                    GPIO.output(control_pin_3[pin],seq[7-halfstep][pin])
            time.sleep(speed)         

def motor():
    #down
    rotate(500,True,0.0008)
    #up
    #rotate(100,False,0.0008)

def motor_2():
    #right
    #rotate_2(100,False,0.0008)
    #left
    rotate_2(200,True,0.0008)
    
def motor_3():
    #upward
    rotate_3(34,True,0.0008)
    
    #downward
    #rotate_3(30,False,0.0008)
    
try:
    t1 = threading.Thread(target=motor,name='t1')
    t2 = threading.Thread(target=motor_2,name='t2')
    #t3 = threading.Thread(target=motor_3,name='t3')
    
    t1.start()
    t2.start()
    #t3.start()
    
    t1.join()
    t2.join()
    #t3.join()
except KeyboardInterrupt:
    pass

GPIO.cleanup()

    

