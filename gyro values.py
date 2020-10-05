#!/usr/bin/env micropython
from ev3dev2.motor import LargeMotor, OUTPUT_B, OUTPUT_D, OUTPUT_C, SpeedPercent, MoveTank, MoveSteering
from ev3dev2.sensor.lego import GyroSensor, ColorSensor
from ev3dev2.sensor import INPUT_2, INPUT_3
import time
import sys

arm = LargeMotor(OUTPUT_D)
tank = MoveTank(OUTPUT_C, OUTPUT_B)
steering_tank = MoveSteering(OUTPUT_C, OUTPUT_B)
gyro = GyroSensor(INPUT_2)
color = ColorSensor(INPUT_3)

#Global Variables 
leftBias = -48
rightBias = -51

def slowDown(leftSpeedSlowDown, rightSpeedSlowDown):
    unifiedSpeed = 50
    while leftSpeedSlowDown > 50:
        leftSpeedSlowDown = leftSpeedSlowDown - 10
        rightSpeedSlowDown = rightSpeedSlowDown - 10
        tank.on_for_seconds(leftSpeedSlowDown, rightSpeedSlowDown, 0.05, brake=True)
    while unifiedSpeed > 10:
        tank.on_for_seconds(unifiedSpeed, unifiedSpeed, 0.05, brake=True)
        unifiedSpeed = unifiedSpeed - 10
    
    tank.off(brake=True)

def gyroCalibrate():
    global leftBias
    global rightBias
    
    if gyro.angle > leftBias and gyro.angle < rightBias:
        print("Seems to be there", file=sys.stderr)
    elif gyro.angle < leftBias:
       while gyro.angle < leftBias:
           steering_tank.on_for_degrees(100, SpeedPercent(100), 5)
    elif gyro.angle > rightBias:
        while gyro.angle > rightBias:
            steering_tank.on_for_degrees(-100, SpeedPercent(100), 5)
    tank.off(brake=True)

def gyroReset():
    #yep, this is how we have to reset the gyro angle to 0
    gyro.mode = 'GYRO-RATE'
    gyro.mode = 'GYRO-ANG'

gyroReset()

time.sleep(10)

while True:
    print(gyro.angle, file=sys.stderr)
