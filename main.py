#!/usr/bin/python3

from reports import *
from mail import *
from xmlmbusresp import *
from xmlconfig import *
from mbusmaster import *
import time


def main():
    retry_interval = 60
    data = []
    month = 4
    year = 2022
    mbus_device_name = '/dev/ttyUSB0'
    xml_config_filename = 'flats.xml'
    simulate = 1

    if simulate == 0:
        mbusmaster = MBusMaster(mbus_device_name)

    # get config
    config = XmlConfig(xml_config_filename)
    meterlist = config.get_meter_list()

    # request all measures
    for flat_no in meterlist.keys():
        # print(flat_no)
        flat_meters = meterlist[flat_no]

        # xmlmbusresp = XmlMbusResp('tmp21710089B4090107.xml')
        # device_id = xml.get_deviceid()
        # value = xml.get_value()

        device_id = flat_meters['cw_meter_id']
        if simulate == 0:
            xmlmbusresp = mbusmaster.request_secondary(device_id)
            if xmlmbusresp == None:
                print('cant read cw for ' + device_id)
                return
            cw_count = xmlmbusresp.get_value()
        else:
            cw_count = 1.231

        device_id = flat_meters['hw_meter_id']
        if simulate == 0:
            xmlmbusresp = mbusmaster.request_secondary(device_id)
            if xmlmbusresp == None:
                print('cant read hw for ' + device_id)
                return
            hw_count = xmlmbusresp.get_value()
        else:
            hw_count = 1.232

        device_id = flat_meters['co_meter_id']
        if simulate == 0:
            xmlmbusresp = mbusmaster.request_secondary(device_id)
            if xmlmbusresp == None:
                print('cant read co for ' + device_id)
                return
            co_count = xmlmbusresp.get_value()
        else:
            co_count = 1.233

        data.append({'flatno' : flat_no, 'cw_count' : cw_count, 'hw_count' : hw_count, 'co_count' : co_count})

    report = Report([month, year])
    report.set_data(data)
    filename = report.generate(len(meterlist)+1)

    return

    mail = Mail()
    ret = True
    while ret == False:
        ret = mail.send(filename)
        if ret == False:
            print('retrying')
            time.sleep(retry_interval)

if __name__ == '__main__':
    main()

