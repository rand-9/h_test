#!/usr/bin/python3

import os
import sys
import datetime
from time import sleep
import serial
import RPi.GPIO as GPIO
from Logger import log


# GPIO SET UP
GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.OUT)

GPIO.output(17,GPIO.LOW)

# pump run time: 30 min
runtime = 30 * 3600
rest = 10 * 3600
morning = "08:00"
lunch = "13:00"
dinner = "20:20"

# Serial communication init
log("Setinng up serial comm")
ser = serial.Serial(port='/dev/ttyACM0', 
baudrate = 9600,
parity=serial.PARITY_NONE,
stopbits=serial.STOPBITS_ONE,
bytesize=serial.EIGHTBITS,
timeout=1
)


def getTemp():
    log("send get temp command to serial")
    ser.write(str.encode('tmp'))


def getHum():
    log("send get humidity command to serial")
    ser.write(str.encode('hum'))


def pump(switch):
    # serial to arduino
    if switch:
        log("Sending pump start to serial")
        print("Pump start")
        ser.write(str.encode('pon'))
        #GPIO.output(17,GPIO.HIGH)
    else:
        log("Sending pump stop to serial")
        print("Pump stop")
        ser.write(str.encode('pof'))
        #GPIO.output(17,GPIO.LOW)


def checkSensors():
    log("Checking for sensor data")
    now_time = datetime.datetime.now().strftime('%H:%M')
    if now_time == morning  or now_time == lunch  or now_time == dinner:
        getTemp()
	sleep(3)
	getHum()
	sleep(3)

def checkPump():
    log("Checking if it is time to pump")
    now_time = datetime.datetime.now().strftime('%H:%M')
    if now_time == morning or now_time == lunch or now_time == dinner:
        pump(True)
        sleep(runtime)
        pump(False)


# Main loop
def main():
    log("Hydroponic START")

    while True:
    checkSensors()
	sleep(5)
	checkPump()
	sleep(5)

        sleep(20)


if __name__ == "__main__":
    main()
