#!/usr/bin/python

import os
import sys
import datetime
from time import sleep
import serial
import RPi.GPIO as GPIO


#GPIO SET UP
GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.OUT)

GPIO.output(17,GPIO.LOW)

#pump run time: 30 min
runtime = 15
rest = 10 * 3600

#Serial communication init
ser = serial.Serial(port='/dev/ttyACM0', 
baudrate = 9600,
parity=serial.PARITY_NONE,
stopbits=serial.STOPBITS_ONE,
bytesize=serial.EIGHTBITS,
timeout=1
)


def pump(switch):
    # serial to arduino
    if switch:
        print("Pump start")
        ser.write(str.encode('pon'))
	GPIO.output(17,GPIO.HIGH)
    else:
        print("Pump stop")
        ser.write(str.encode('pof'))
	GPIO.output(17,GPIO.LOW)


# Main loop
def main():

    while True:

        now_time = datetime.datetime.now().strftime('%H')
        if (now_time == '17'):
            pump(True)
            sleep(runtime)
            pump(False)
            sleep(runtime)


if __name__ == "__main__":
    main()
