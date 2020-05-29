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
GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.OUT)

GPIO.output(17,GPIO.LOW)

# pump run time: 30 min
runtime = 30 * 60
testtime = 2 * 60
rest = 10 * 3600
morning = "08:00"
lunch = "14:00"
dinner = "20:00"

# Serial communication init
log("Setting up serial comm")
ser = serial.Serial(port='/dev/ttyACM0', 
baudrate = 9600,
parity=serial.PARITY_NONE,
stopbits=serial.STOPBITS_ONE,
bytesize=serial.EIGHTBITS,
timeout=1
)


def writeToSerial(msg):
    #ser.write(bytearray(msg + '\n', encoding='utf-8'))
    ser.write(str.encode(msg))


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

def pump(switch):
    # serial to arduino
    if switch:
        log("Sending pump START to serial")
        writeToSerial('pon')
        #GPIO.output(17,GPIO.HIGH)
    else:
        log("Sending pump STOP to serial")
        writeToSerial('pof')
        #GPIO.output(17,GPIO.LOW)


def checkSensors():
    #log("Checking for sensor data")
    now_time = datetime.datetime.now().strftime('%H:%M')
    if now_time == morning or now_time == lunch or now_time == dinner:
        log("Checking sensors...")
        t = getTemp()
        sleep(3)
        h = getHum()
        sleep(3)

        ts = datetime.datetime.now().strftime('%H:%M:%S')

        d = {
            "timestamp": ts,
            "temperature": t,
            "humidity": h
        }
        DataLogger.writeData(d)

def checkPump():
    #log("Checking if it is time to pump")
    now_time = datetime.datetime.now().strftime('%H:%M')
    if now_time == morning or now_time == lunch or now_time == dinner:
	pump(True)
        sleep(runtime)
        pump(False)


# Main loop
def main():
    log("Hydroponic main Starting")

    while True:
	checkSensors()
	sleep(5)
	checkPump()

	sleep(5)



if __name__ == "__main__":
    main()
