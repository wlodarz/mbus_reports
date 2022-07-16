#!/usr/bin/python3

from datetime import date
from reckoning import *

def main():
    config_filename = 'flats.xml'
    today = date.today()
    print(today)
    day = int(today.strftime("%d"))
    month = int(today.strftime("%m"))
    year = int(today.strftime("%Y"))
    reckoning = Reckoning(config_filename, day, month, year)
    reckoning.get_measures()
    reckoning.generate_report()

if __name__ == '__main__':
    main()

