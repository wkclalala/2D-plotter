
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
import numpy as np
from PIL import Image


def rgb2gray(rgb):
    r,g,b = rgb[:,:,0],rgb[:,:,1],rgb[:,:,2]
    gray = 0.2989*r+ 0.5870*g+0.1140*b
    return gray.astype(np.uint8)

'''
pic = Image.open('7.jpg')
np_pic = np.array(pic)
print np_pic.dtype
img = rgb2gray(np_pic)
#np_pic_bw = np_pic_bw.reshape(np_pic_bw.shape[0],np_pic_bw.shape[1],1)
print(img.dtype)
print(img.shape)
print(img[1])
'''

pic = Image.open('2.png').convert('L')
img = np.array(pic)
print(img.dtype)
print(img.shape)

initial_m_3 = 0

'''
img = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,255,255,255,255,255,255,255,255,255,255,255,255, 255,255,255,255,255,255, 255,255,255,255,255,255, 255,255,255,255,255,255, 255,255,255,255,255,255] 
img = np.array(img)
img = np.append(img,[img,img,img,img,img,img])
img = np.reshape(img,(1,img.shape[0]))
print(img.shape)
'''
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
    rotate(512,True,0.0008)
    rotate(512,False,0.0008)

def motor_2():
    rotate_2(750,False,0.0008)
    rotate_2(750,True,0.0008)
    
def motor_3():
    rotate_3(10,False,0.0008)
    rotate_3(20,False,0.0008)
    time.sleep(1)
    rotate_3(5,False,0.0008)
    time.sleep(1)
    rotate_3(5,False,0.0008)
    time.sleep(1)
    rotate_3(5,False,0.0008)
    time.sleep(1)
    rotate_3(5,False,0.0008)
    time.sleep(1)
    rotate_3(5,False,0.0008)
    time.sleep(1)
    
    
    rotate_3(45,True,0.0008)
    rotate_3(10,True,0.0008)

def recover(length,width):
    if length%2 is 1:
        rotate_2(width,True,0.0008)
    rotate(length,False,0.0008)
    rotate_3(initial_m_3,True,0.0008)
    
def plot():
    r_3 = 0
    width, length = img.shape
    rotate_3(initial_m_3,False,0.0008)
    flag = False
    for i in range(width):
        for j in range(length):
            if flag is False:
                rotate(6, flag,0.0008)
                target = 17-img[i][j]/15
            else:
                rotate(6,flag,0.0008)
                target = 17-img[i][length-1-j]/15
            '''
            if(r_3<target):
                rotate_3(target-r_3,False,0.0008)
            elif(r_3>target):
                rotate_3(r_3-target, True, 0.0008)
            r_3 = target
            '''
            
            
            if(target>3):
                if(r_3==0):
                    rotate_3(50,False,0.0008)
                    r_3=1
            else:
                if(r_3==1):
                    rotate_3(50,True,0.0008)
                    r_3=0
            
            
            
        if flag is False: flag = True
        else: flag = False
        rotate_2(6,False,0.0008)

    recover(width,length)

try:

    

    #t1 = threading.Thread(target=motor,name='t1')
    #t2 = threading.Thread(target=motor_2,name='t2')
    #t3 = threading.Thread(target=motor_3,name='t3')
    t_plot = threading.Thread(target=plot,name='plot')
    
    #t1.start()
    #t2.start()
    #t3.start()
    t_plot.start()
    
    #t1.join()
    #t2.join()
    #t3.join()
    t_plot.join()


    
except KeyboardInterrupt:
    rotate_3(initial_m_3,True,0.0008)
    pass

    

GPIO.cleanup()