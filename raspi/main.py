#!/usr/bin/python

import os
import sys
import datetime
from time import sleep
import serial


runtime = 30 * 3600

ser = serial.Serial(
        port='/dev/serial0', #Replace ttyS0 with ttyAM0 for Pi1,Pi2,Pi0
        baudrate = 9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
)

def pump():
    # serial to arduino
    print("Guarda come pompo")
    ser.write(str.encode('serialTest'))

# Returns current time in format yyyy-mm-dd HH:MM:SS
now_time = datetime.datetime.now().strftime('%H:%M')

# Main method
#   3.  Runs sprinkler if rainfall falls below threshold
def main(): 

     while True:
        now_time = datetime.datetime.now().strftime('%H:%M')
         
        if (now_time == '19:21'):
            print(now_time)
            pump()
            t = 0
            while(t < 100):
                print('while')
                sleep(1)
                t += 1
        print("esc")
        #pump()
    

if __name__ == "__main__":
    main()
