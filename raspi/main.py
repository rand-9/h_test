#!/usr/bin/python

import os
import sys
import datetime
from time import sleep
import serial
import RPi.GPIO as GPIO


# GPIO SET UP
GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.OUT)

GPIO.output(17,GPIO.LOW)

# pump run time: 30 min
runtime = 30 * 3600
rest = 10 * 3600

# Serial communication init
ser = serial.Serial(port='/dev/ttyACM0', 
baudrate = 9600,
parity=serial.PARITY_NONE,
stopbits=serial.STOPBITS_ONE,
bytesize=serial.EIGHTBITS,
timeout=1
)


def getTemp():
    ser.write(str.encode('tmp'))


def getHum():
    ser.write(str.encode('hum'))


def pump(switch):
    # serial to arduino
    if switch:
        print("Pump start")
        ser.write(str.encode('pon'))
        #GPIO.output(17,GPIO.HIGH)
    else:
        print("Pump stop")
        ser.write(str.encode('pof'))
        #GPIO.output(17,GPIO.LOW)


def checkSensors():
    now_time = datetime.datetime.now().strftime('%H:%M')
    if now_time == '08.00' or now_time == '13.00' or now_time == '18.00':
        getTemp()


def checkPump():
    now_time = datetime.datetime.now().strftime('%H:%M')
    if now_time == '08.00' or now_time == '13.00' or now_time == '18.00':
        pump(True)
        sleep(runtime)
        pump(False)


# Main loop
def main():

    while True:

        checkPump()
        checkSensors()

        sleep(20)


if __name__ == "__main__":
    main()
