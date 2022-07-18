#!/usr/bin/python3

from mbus.MBus import MBus
import time

class MBusMaster:

    debug = True
    default_short_address = 253
    default_secondary_address = ""
    retries = 8

    def __init__(self, device_name):
        self.mbus = MBus(device=device_name)
        self.mbus.connect()

    def request_primary(self, address):
        for retry in range(1, self.retries):
            print('trying ' + str(retry) + ' addr ' + address)
            try:
                return self.request(address)
            except:
                time.sleep(3.0)
        return None

    def request_secondary(self, secondary_address):
        for retry in range(1, self.retries):
            print('trying ' + str(retry) + ' addr ' + secondary_address)
            try:
                self.mbus.select_secondary_address(secondary_address)
                return self.request(self.default_short_address)
            except:
                time.sleep(3.0)
        return None

    def request(self, address):
        self.mbus.send_request_frame(address)
        reply = self.mbus.recv_frame()
        if reply == None:
            return None

        reply_data = self.mbus.frame_data_parse(reply)
        # if debug:
        #     print("reply_data =", reply_data)

        xml_buff = self.mbus.frame_data_xml(reply_data)
        # print("xml_buff =", xml_buff)

        self.mbus.frame_data_free(reply_data)

        return xml_buff

    def __del__(self):
            self.mbus.disconnect()
