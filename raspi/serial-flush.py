#!/usr/bin/python

import os
import sys
import datetime
from time import sleep
import serial
import argparse

ser = serial.Serial(
        port='/dev/ttyACM0', #Replace ttyS0 with ttyAM0 for Pi1,Pi2,Pi0
        baudrate = 9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
)


def main():
        sleep(1)
        ser.flushInput()
        ser.flushOutput()
        sleep(1)

if __name__ == "__main__":
    main()
