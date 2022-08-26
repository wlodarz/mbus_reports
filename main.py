#!/usr/bin/python3

import datetime
from reckoning import *
from db import *

def main():
    config_filename = 'flats.xml'
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    day = int(today.strftime("%d"))
    month = int(today.strftime("%m"))
    month_tomorrow = int(tomorrow.strftime("%m"))
    year = int(today.strftime("%Y"))

    reckoning = Reckoning(config_filename, day, month, year)
    reckoning.acquire_measures()
    if month != month_tomorrow:
        reckoning.generate_report()
        reckoning.send_report()
        print('sending')
    else:
        print('not sending')
    data = reckoning.get_measures()
    db = DB('mbus', 'mbus', 'bukowa')
    db.connect()
    db.insert(data)    
    db.close()

if __name__ == '__main__':
    main()

