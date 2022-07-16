#!/usr/bin/python3

from reports_pdf import *
from mail import *
from xmlmbusresp import *
from xmlconfig import *
from mbusmaster import *
import time


class Reckoning:
    def __init__(self, config_filename, day, month, year):
        self.current_data = []
        self.day = day
        self.month = month
        self.year = year
        self.simulate = 1
        self.retry_interval = 60
        self.mbus_device_name = '/dev/ttyUSB0'
        self.xml_config_filename = config_filename

    def get_measures(self):

        if self.simulate == 0:
            mbusmaster = MBusMaster(self.mbus_device_name)

        # get config
        config = XmlConfig(self.xml_config_filename)
        self.meterlist = config.get_meter_list()

        # request all measures
        for flat_no in self.meterlist.keys():
            # print(flat_no)
            flat_meters = self.meterlist[flat_no]

            # xmlmbusresp = XmlMbusResp('tmp21710089B4090107.xml')
            # device_id = xml.get_deviceid()
            # value = xml.get_value()

            device_id = flat_meters['cw_meter_id']
            if self.simulate == 0:
                xmlmbusresp = mbusmaster.request_secondary(device_id)
                if xmlmbusresp == None:
                    print('cant read cw for ' + device_id)
                    return
                cw_count = xmlmbusresp.get_value()
            else:
                cw_count = 1.231

            device_id = flat_meters['hw_meter_id']
            if self.simulate == 0:
                xmlmbusresp = mbusmaster.request_secondary(device_id)
                if xmlmbusresp == None:
                    print('cant read hw for ' + device_id)
                    return
                hw_count = xmlmbusresp.get_value()
            else:
                hw_count = 1.232

            device_id = flat_meters['co_meter_id']
            if self.simulate == 0:
                xmlmbusresp = mbusmaster.request_secondary(device_id)
                if xmlmbusresp == None:
                    print('cant read co for ' + device_id)
                    return
                co_count = xmlmbusresp.get_value()
            else:
                co_count = 1.233

            self.current_data.append({'flatno' : flat_no, 'cw_count' : cw_count, 'hw_count' : hw_count, 'co_count' : co_count})

    def generate_report(self):
        report = Report([self.day, self.month, self.year])
        report.set_data(self.current_data)
        self.report_filename = report.generate(len(self.meterlist)+1)

    def send_report(self):
        mail = Mail()
        ret = True
        while ret == False:
            ret = mail.send(report_filename)
            if ret == False:
                print('retrying')
                time.sleep(self.retry_interval)

if __name__ == '__main__':
    month = 4
    year = 2022
    config_filename = 'flats.xml'
    reckoning = Reckoning(config_filename, month, year)
    reckoning.get_measures()

