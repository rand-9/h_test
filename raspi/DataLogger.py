#!/usr/bin/python3

import csv
from Logger import log

fileloc = "./data.csv"


def writeData():
    writer.writeheader()
    writer.writerow(
        {'timestamp': 0,
         'temperature': 10,
         'humidity': 2})
    writer.writerow({'timestamp': 1, 'temperature': 12, 'humidity': 3})


def writeDict(dict):
    log("Writing values to csv...")
    writer.writerow(dict)


with open(fileloc, mode='w') as data_csv:
    fieldnames = ['timestamp', 'temperature', 'humidity']
    writer = csv.DictWriter(data_csv, fieldnames=fieldnames)
    writeData()