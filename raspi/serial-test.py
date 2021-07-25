#!/usr/bin/python

import os
import sys
import datetime
from time import sleep
import serial
import argparse



def get_arguments():
    parser = argparse.ArgumentParser(description='Send a single command to the serial port.')
    parser.add_argument('--command',
                        type=str,
                        default='tmp',
                        help='the command to send to serial')
    return parser.parse_args()


args = get_arguments()

ser = serial.Serial(
        #port='/dev/ttyACM0', #Replace ttyS0 with ttyAM0 for Pi1,Pi2,Pi0
        baudrate = 9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
)


def main():
        #ser.flushInput()
        #ser.flushOutput()
        print("Command: ", args.command)
        ser.write(str.encode(args.command))
        sleep(1)
        x = ser.readline()
        sleep(1) 
        print(x)
        sleep(1)
        #ser.flushInput()
        #ser.flushOutput()
        #sleep(1)

if __name__ == "__main__":
    main()
