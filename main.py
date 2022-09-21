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
    data,error_flag,alarms = reckoning.get_measures()

    if error_flag == True or month != month_tomorrow:
    # if True:
        reckoning.generate_report()
        reckoning.send_report()
        print('sending')
    else:
        print('not sending')

        
    # data = reckoning.get_measures()
    db = DB('mbus', 'mbus', 'bukowa')
    db.connect()
    db.insert_odczyt(data)
    if error_flag == True:
        db.insert_alarms(alarms)
    db.close()

if __name__ == '__main__':
    main()

