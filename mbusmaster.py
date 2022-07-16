#!/usr/bin/env python3

from mbus.MBus import MBus
import time

class MBusMaster:

    debug = True
    default_short_address = 253
    # default_secondary_address = "21710096B4090107"
    default_secondary_address = ""
    retries = 8

    def __init__(self, device_name):
        self.mbus = MBus(device=device_name)
        self.mbus.connect()

    def request_secondary(self, secondary_address):
        self.mbus.select_secondary_address(secondary_address)
        return self.request(default_short_address)

    def request(self, address):
        retok = 0
        for retry in range(1, retries):
            self.mbus.send_request_frame(address)
            reply = self.mbus.recv_frame()
            if reply != None:
                retok = 1
                break
            time.sleep(10.0)

        if debug:
            print("reply =", reply)

        if retok == 0:
            return None

        reply_data = self.mbus.frame_data_parse(reply)
        if debug:
            print("reply_data =", reply_data)

        xml_buff = self.mbus.frame_data_xml(reply_data)
        print("xml_buff =", xml_buff)

        self.mbus.frame_data_free(reply_data)

        return xml_buff

    def __del__(self):
            self.mbus.disconnect()
