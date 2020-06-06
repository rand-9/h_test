#!/usr/bin/python3

import os
import sys
import datetime
from time import sleep
import serial
import RPi.GPIO as GPIO
from Logger import log
import DataLogger


# GPIO SET UP
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(17,GPIO.OUT)
# GPIO.output(17,GPIO.LOW)

# pump run time: 30 min
runtime = 30 * 60
testtime = 2 * 60
rest = 10 * 3600
morning = "08:00"
lunch = "14:00"
dinner = "20:00"
EC_MIN = 1.40
EC_MAX = 1.60

# Serial communication init
log("Setting up serial comm")
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
    log("adding nutrient A")
    writeToSerial("a")
    sleep(1)


def addB():
    log("adding nutrient B")
    writeToSerial("b")
    sleep(1)


def addWater(switch):
    if switch:
        log("Sending pump START to serial")
        writeToSerial('w0')
    else:
        log("Sending pump STOP to serial")
        writeToSerial('wof')


def getTemp():
    log("send get temp command to serial")
    writeToSerial('tmp')
    sleep(1)
    x = ser.readline()
    return x


def getHum():
    log("send get humidity command to serial")
    writeToSerial('hum')
    sleep(1)
    x = ser.readline()
    return x


def getEC():
    log("send get humidity command to serial")
    writeToSerial('ec')
    sleep(1)
    x = ser.readline()
    return x


def pump(switch):
    # serial to arduino
    if switch:
        log("Sending pump START to serial")
        writeToSerial('pon')
    else:
        log("Sending pump STOP to serial")
        writeToSerial('pof')


def checkSensors():
    #log("Checking for sensor data")
    now_time = datetime.datetime.now().strftime('%H:%M')
    if now_time == morning or now_time == lunch or now_time == dinner:
        log("Checking sensors...")
        t = getTemp()
        sleep(3)
        h = getHum()
        sleep(3)
        ec = getEC()
        ts = datetime.datetime.now().strftime('%H:%M:%S')
        d = {
            "timestamp": ts,
            "temperature": t,
            "humidity": h,
            "conductivity": ec
        }
        DataLogger.writeData(d)


def checkWaterQuality():
    # log("checking water quality")
    now_time = datetime.datetime.now().strftime('%H:%M')
    time_list = now_time.split(':')
    [int(i) for i in time_list]

    if time_list[0] == int(morning.split(':')[0])-1 or time_list[0] == int(lunch.split(':')[0])-1 or time_list[0] == int(dinner.split(':')[0])-1:
        log("Checking water quality")
        checkSensors()
        ec = getEC()
        sleep(3)
        
        if EC_MIN < ec < EC_MAX:
            log("EC value is in range")
        elif ec < EC_MIN:
            log("EC value is below range")
            addA()
            sleep(30)
            addB()
            sleep(30)
        elif ec > EC_MAX:
            log("EC value is above range")
            addWater()
            sleep(30)

    sleep(90)


def checkPump():
    # log("Checking if it is time to pump")
    now_time = datetime.datetime.now().strftime('%H:%M')
    if now_time == morning or now_time == lunch or now_time == dinner:
        pump(True)
        sleep(runtime)
        pump(False)


# Main loop
def main():
    log("Hydroponic main Starting")

    while True:
        checkWaterQuality()
        sleep(5)
        checkPump()

    sleep(5)


if __name__ == "__main__":
    main()
