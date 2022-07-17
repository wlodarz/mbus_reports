#!/usr/bin/python3

import xml.etree.ElementTree as ET

class XmlConfig:
    flat_no = -1
    config = {}

    def __init__(self, filename):
        tree = ET.parse(filename)
        root = tree.getroot()

        for flat in root.findall('Flat'):
                id = int(flat.find('Id').text)
                if id == None:
                    pass
                hw_meter_id = flat.find('HwMeterId')
                if hw_meter_id == None:
                    pass
                cw_meter_id = flat.find('CwMeterId')
                if cw_meter_id == None:
                    pass
                co_meter_id = flat.find('CoMeterId')
                if co_meter_id == None:
                    pass
                # self.config[id] = {'hw_meter_id' : int(hw_meter_id.text), 'cw_meter_id' : int(cw_meter_id.text), 'co_meter_id' : int(co_meter_id.text)}
                self.config[id] = {'hw_meter_id' : hw_meter_id.text, 'cw_meter_id' : cw_meter_id.text, 'co_meter_id' : co_meter_id.text}


    # should read config XML
    def get_meter_list(self):
        return self.config

