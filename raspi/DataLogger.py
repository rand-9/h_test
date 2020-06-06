#!/usr/bin/python3

import os.path
import csv
from Logger import log

fileloc = "./data.csv"


def writeDataSamples():
    writer.writeheader()
    writer.writerow({'timestamp': 0,
                     'temperature': 0,
                     'humidity': 0,
                     "conductivity": 0.00})


def writeDict(dict):
    log("Writing values to csv...")
    with open('document.csv', 'a') as data_csv:
        fieldnames = ['timestamp', 'temperature', 'humidity', "conductivity"]
        writer = csv.DictWriter(data_csv, fieldnames=fieldnames)
        writer.writerow(dict)


if os.path.isfile(fileloc):
    print ("csv data file exist")
else:
    print ("csv data file not exist, create...")
    with open(fileloc, mode='w') as data_csv:
        fieldnames = ['timestamp', 'temperature', 'humidity', "conductivity"]
        writer = csv.DictWriter(data_csv, fieldnames=fieldnames)
        writeDataSamples()

