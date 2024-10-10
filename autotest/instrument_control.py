#!/usr/bin/env python
# -*- coding: utf-8 -*-


'''程序

@description
    说明
'''
import pyvisa


class InstrumentControl():
    def __init__(self, ip="192.168.3.244"):
        self.ip = ip
        self.rm = pyvisa.ResourceManager()

    def connect(self):
        # self.resource_name = "TCPIP0::" + self.ip + "::inst0::INSTR"
        self.resource_name = f"TCPIP0::{self.ip}::inst0::INSTR"
        print(self.resource_name)
        self.instrument = self.rm.open_resource(self.resource_name)

    def write(self, command):
        ret = self.instrument.write(command)
        print("command: ",command)
        print("ret: ",ret)

    def read(self):
        return self.instrument.read()

    def query(self, command):
        self.write(command)
        ret = self.read()
        print("ret: ",ret)
        return ret

    def send(self, command):
        if "?" in command:
            ret = self.query(command)
        else:
            ret =self.write(command)
            
        return ret





if __name__ == '__main__':
    inst1 = InstrumentControl()
    inst1.connect()
    inst1.send("*IDN?")
