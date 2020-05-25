#!/usr/bin/python3

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
morning = "08:00"
lunch = "13:00"
dinner = "20:20"

# Serial communication init
ser = serial.Serial(port='/dev/ttyACM0', 
baudrate = 9600,
parity=serial.PARITY_NONE,
stopbits=serial.STOPBITS_ONE,
bytesize=serial.EIGHTBITS,
timeout=1
)


def write(msg):
    ser.write(bytearray(msg + '\n', encoding='utf-8'))



def getTemp():
    write('tmp')


def getHum():
    ser.write('hum')


def pump(switch):
    # serial to arduino
    if switch:
        print("Pump start")
        write('pon')
        #GPIO.output(17,GPIO.HIGH)
    else:
        print("Pump stop")
        write('pof')
        #GPIO.output(17,GPIO.LOW)


def checkSensors():
    now_time = datetime.datetime.now().strftime('%H:%M')
    if now_time == morning  or now_time == lunch  or now_time == dinner:
        getTemp()
	sleep(3)
	getHum()
	sleep(3)

def checkPump():
    now_time = datetime.datetime.now().strftime('%H:%M')
    if now_time == morning or now_time == lunch or now_time == dinner:
        pump(True)
        sleep(runtime)
        pump(False)


# Main loop
def main():

    while True:

        checkSensors()
	sleep(5)
	checkPump()

	sleep(5)



if __name__ == "__main__":
    main()
