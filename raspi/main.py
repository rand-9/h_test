#!/usr/bin/python

import os
import sys
import datetime
from time import sleep
import serial
import RPi.GPIO as GPIO


#GPIO SET UP
GPIO.setmode(GPIO.BCM)
GPIO.setup(17,out)

GPIO.output(17,GPIO.HIGH)

#pump run time: 30 min
runtime = 30 * 3600
rest = 10 * 3600

#Serial communication init
ser = serial.Serial(port='/dev/serial0', 
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
        ser.write(str.encode('pon\n'))
		GPIO.output(17,GPIO.LOW)
    else:
        print("Pump stop")
        ser.write(str.encode('poff\n'))
		GPIO.output(17,GPIO.HIGH)


# Main loop
def main():

    while True:

        now_time = datetime.datetime.now().strftime('%H:%M')
        if (now_time == '08:00' | now_time == '13:00' | now_time == '18:00' ):
            pump(True)
            sleep(runtime)
            pump(False)


if __name__ == "__main__":
    main()
