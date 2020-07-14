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
morning = "06:00"
lunch = "10:00"
afternoon = "15:00"
dinner = "20:00"
night = "23:00"
EC_MIN = 1.40
EC_MAX = 1.60
correction = False

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
    log("send add nutrient A")
    writeToSerial("a")
    sleep(1)


def addB():
    log("send add nutrient B")
    writeToSerial("b")
    sleep(1)


def addWater(switch):
    if switch:
        log("Sending pump START to serial")
        writeToSerial('won')
    else:
        log("Sending pump STOP to serial")
        writeToSerial('wof')


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


def pump(switch):
    # serial to arduino
    if switch:
        log("Sending pump START to serial")
        writeToSerial('pon')
    else:
        log("Sending pump STOP to serial")
        writeToSerial('pof')


def checkSensors():
    log("Checking for sensor data")
    #now_time = datetime.datetime.now().strftime('%H:%M')
    #if now_time == morning or now_time == lunch or now_time == dinner:
    log("Checking sensors...")
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
    log("checking water quality1")
    now_time = datetime.datetime.now().strftime('%H:%M')
    log(now_time)
    time_list = now_time.split(':')
    time_list = [int(i) for i in time_list]
    log(time_list[0])
    result = False

    if time_list[0] == int(morning.split(':')[0])-2 or time_list[0] == int(dinner.split(':')[0])-2:
         log("Checking water quality2")
         checkSensors()
         sleep(5)
         ec = getEC()
         sleep(5)
         if EC_MIN < ec < EC_MAX:
             log("EC value is in range")
             result = True
         elif ec < EC_MIN:
             log("EC value is below range")
             addA()
             sleep(30)
             addB()
             sleep(30)
         elif ec > EC_MAX:
             log("EC value is above range")
             addWater(True)
             sleep(30)
             addWater(False)

    sleep(120)
    return result



def checkPump():
    log("Checking if it is time to pump")
    now_time = datetime.datetime.now().strftime('%H:%M')
    if now_time==morning or now_time==lunch or now_time==afternoon or now_time==dinner or now_time==night :
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
