#!/usr/bin/env python
# -*- coding: utf-8 -*-


'''程序

@description
    说明
'''
from instrument_control import InstrumentControl


class TransmitHandler():
    def __init__(self):
        self.InstrumentControl = InstrumentControl()

    def transmit_cw_signals(self, RF,frequency, power):
        self.frequency = frequency
        self.power = power
        self.RF=RF
        self.InstrumentControl.connect()

        # 设置端口
        # 设置端口
        self.InstrumentControl.write("CONFigure:SOURce:ROUTe:SCENario:SALone RF18")
        self.InstrumentControl.write("CONFigure:SOURce:ROUTe:USAGe:ALL RF18,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF")
        self.InstrumentControl.write(f"CONFigure:SOURce:ROUTe:USAGe {self.RF},ON")


        # 设置baseband mode 、list模式、external attenuation、dgai
        self.InstrumentControl.write(command="CONFigure:SOURce:BBMode CW")
        self.InstrumentControl.write(command="CONFigure:SOURce:LIST OFF")
        self.InstrumentControl.write(command="CONFigure:SOURce:RFSettings:EATTenuation 0")
        self.InstrumentControl.write(command="CONFigure:SOURce:RFSettings:DGAin 0")

        # 设置frequency、level
        self.InstrumentControl.write(f"CONFigure:SOURce:RFSettings:FREQuency {self.frequency}")
        self.InstrumentControl.write(f"CONFigure:SOURce:RFSettings:LEVel {self.power}")

        # 打开Generator并查询Generator当前状态
        self.InstrumentControl.write("CONFigure:SOURce:STATe ON")
        self.InstrumentControl.query("CONFigure:SOURce:STATe?")

        print(f"CW信号已发射：频率 = {self.frequency} Hz, 功率 = {self.power} dBm")



if __name__ == '__main__':
    cw_signals=TransmitHandler()
    cw_signals.transmit_cw_signals("RF6","1.2E+9", "-30")

