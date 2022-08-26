#!/usr/bin/python3

from datetime import date
from reckoning import *
from db import *

def main():
    config_filename = 'flats.xml'
    today = date.today()
    day = int(today.strftime("%d"))
    month = int(today.strftime("%m"))
    year = int(today.strftime("%Y"))
    reckoning = Reckoning(config_filename, day, month, year)
    reckoning.acquire_measures()
    reckoning.generate_report()
    reckoning.send_report()
    data = reckoning.get_measures()
    db = DB('mbus', 'mbus', 'bukowa')
    db.connect()
    db.insert(data)    
    db.close()

if __name__ == '__main__':
    main()

