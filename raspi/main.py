##!/usr/bin/python3

import os
import sys
import datetime
from time import sleep
import serial
import RPi.GPIO as GPIO
from Logger import log
import DataLogger


# constant values
runtime = 30 * 60
morning = "07:00"
lunch = "11:00"
afternoon = "16:00"
dinner = "21:00"
night = "03:00"
EC_MIN = 1.90
EC_MAX = 2.20
PH_MIN = 4.50
PH_MAX = 5.50
correction = False

# Serial communication init
log("Setting up serial communication")
ser = serial.Serial(port='/dev/ttyACM0',
                    baudrate=9600,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS,
                    timeout=1)


def writeToSerial(msg):
    #ser.write(bytearray(msg + '\n', encoding='utf-8'))
    ser.write(str.encode(msg))


def addA():
    log("send command - add nutrient A")
    writeToSerial("a")
    sleep(1)


def addB():
    log("send command - add nutrient B")
    writeToSerial("b")
    sleep(1)


def addWater(switch):
    if switch:
        log("send add water START to serial")
        writeToSerial('won')
    else:
        log("send add water STOP to serial")
        writeToSerial('wof')


def addPhDown():
    log("send command - add ph down")
    writeToSerial("phd")
    sleep(1)


def air(switch):
    if switch:
        log("send air pump START to serial")
        writeToSerial('za')
    else:
        log("send air pump STOP to serial")
        writeToSerial('zb')


def getTemp():
    log("send get temp command to serial")
    writeToSerial('tmp')
    sleep(1)
    x = ser.readline()
    log("return temperature value:")
    log(x)
    return x


def getHum():
    log("send get humidity command to serial")
    writeToSerial('hum')
    sleep(1)
    x = ser.readline()
    log("return humidity value:")
    log(x)
    return x


def getEC():
    log("send get ec command to serial")
    writeToSerial('ec')
    sleep(3)
    x = ser.readline()
    log("return ec value:")
    log(x)
    return float(x)


def getPH():
    log("send get ph command to serial")
    writeToSerial('ph')
    sleep(3)
    x = ser.readline()
    log("return ph value:")
    log(x)
    return float(x)


def pump(switch):
    # serial to arduino
    if switch:
        log("send recycle pump START to serial")
        writeToSerial('pon')
    else:
        log("send recycle pump STOP to serial")
        writeToSerial('pof')


def checkSensors():
    log("get all sensors values")
    t = getTemp()
    sleep(3)
    h = getHum()
    sleep(3)
    ec = getEC()
    ts = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
    d = {
            "timestamp": ts,
            "temperature": t,
            "humidity": h,
            "conductivity": ec
    }
    log(d)
    DataLogger.writeDict(d)


def checkWaterQuality():
    ser.flushInput()
    ser.flushOutput()
    log("check water quality time")
    now_time = datetime.datetime.now().strftime('%H:%M')
    time_list = now_time.split(':')
    time_list = [int(i) for i in time_list]
    result = False

    if time_list[0] == int(lunch.split(':')[0])-3 or time_list[0] == int(dinner.split(':')[0])-3:
         log("adjust ec", "debug")
         checkSensors()
         sleep(5)
         ec = getEC()
         sleep(5)
         if EC_MIN < ec < EC_MAX:
             log("ec value is in range")
         elif ec < EC_MIN:
             log("ec value is below range")
             air(True)
             sleep(5)
             addA()
             sleep(30)
             addB()
             sleep(30)
         elif ec > EC_MAX:
             log("ec value is above range")
             addWater(True)
             sleep(30)
             addWater(False)
         sleep(120)
         air(False)

    elif time_list[0] == int(morning.split(':')[0])+1 or time_list[0] == int(lunch.split(':')[0])+1 or time_list[0] == int(afternoon.split(':')[0])+1 or time_list[0] == int(dinner.split(':')[0])+1:
         log("adjust pH", "debug")
         checkSensors()
         sleep(5)
         ph = getPH()
         sleep(5)
         if PH_MIN < ph < PH_MAX:
             log("ph value is in range")
         elif ph < PH_MIN:
             log("ph value is below range")
         elif ph > PH_MAX:
             log("ph value is above range")
             sleep(5)


         sleep(600)




def checkPump():
    log("checking if time to recycle pump")
    now_time = datetime.datetime.now().strftime('%H:%M')
    if now_time==morning or now_time==lunch or now_time==afternoon or now_time==dinner or now_time==night :
        pump(True)
        sleep(runtime)
        pump(False)


# Main loop
def main():
    log("Hydroponic main script start")
    while True:
        checkWaterQuality()
        sleep(5)
        checkPump()

    sleep(5)


if __name__ == "__main__":
    main()
