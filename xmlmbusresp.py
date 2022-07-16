#!/usr/bin/python3

import xml.etree.ElementTree as ET

class XmlMbusResp:
    device_id = ''
    device_value = ''

    def __init__(self, filename):
        tree = ET.parse(filename)
        root = tree.getroot()

        slaveinfo = root.find('SlaveInformation')
        if slaveinfo != None:
            idinfo = slaveinfo.find('Id')
            if idinfo != None:
                self.device_id = idinfo.text
                # print(idinfo.text)

        for datarecord in root.findall('DataRecord'):
            if datarecord.get('id') != '0':
                continue
            function = datarecord.find('Function')
            if function != None and function.text == 'Instantaneous value':
                value = datarecord.find('Value')
                if value != None:
                    self.device_value = value.text
                    # print(self.device_value)

    def get_deviceid(self):
        return self.device_id

    def get_value(self):
        return self.device_value
