#!/usr/bin/env python
# -*- coding: utf-8 -*-


'''程序

@description
    说明
'''
import time

from instrument_control import InstrumentControl
from transmit_handler import TransmitHandler


class ReceiveHandler():
    def __init__(self):
        self.InstrumentControl = InstrumentControl()

    def measure_power(self, rf_port, frequency, reference_power, magin, ):
        self.InstrumentControl.connect()

        # 设置端口、list模式、external attenuation 、freq、reference power、 mixLevOffset、freqoffset
        self.InstrumentControl.send(f"CONFigure:SENSe:POWer:ROUTe:GLOBal {rf_port}")
        self.InstrumentControl.send("CONFigure:SENSe:POWer:LIST OFF")
        self.InstrumentControl.send("CONFigure:SENSe:POWer:RFSettings:EATTenuation 0")
        self.InstrumentControl.send(f"CONFigure:SENSe:POWer:RFSettings:FREQuency {frequency}")
        self.InstrumentControl.send(f"CONFigure:SENSe:POWer:RFSettings:ENPower {reference_power}")
        self.InstrumentControl.send(f"CONFigure:SENSe:POWer:RFSettings:UMARgin {magin}")
        self.InstrumentControl.send("CONFigure:SENSe:POWer:RFSettings:MLOFfset 0")
        self.InstrumentControl.send("CONFigure:SENSe:POWer:RFSettings:FOFFset 0")

        # 设置超时时间、Step Length、Measurement Length
        self.InstrumentControl.send("CONFigure:SENSe:POWer:REPetition SINGleshot")
        self.InstrumentControl.send("CONFigure:SENSe:POWer:TOUT 1")
        self.InstrumentControl.send("CONFigure:SENSe:POWer:SLENgth 1ms")
        self.InstrumentControl.send("CONFigure:SENSe:POWer:MLENgth 400E-6")

        # 设置measurement statistics
        self.InstrumentControl.send("CONFigure:SENSe:POWer:SCOunt 5")

        # 选择30 kHz 高斯滤波器
        self.InstrumentControl.send("CONFigure:SENSe:POWer:FILTer:TYPE GAUSs")
        self.InstrumentControl.send("CONFigure:SENSe:POWer:FILTer:GAUSs:BWIDth 30kHz")

        # 设置trigger
        self.InstrumentControl.send("CONFigure:SENSe:POWer:TRIGger:CATalog:SOURce?")
        self.InstrumentControl.send("CONFigure:SENSe:POWer:TRIGger:SOURce 'Free Run'")
        self.InstrumentControl.send("CONFigure:SENSe:POWer:TRIGger:SLOPe REDGe")
        self.InstrumentControl.send("ONFigure:SENSe:POWer:TRIGger:THReshold -20")
        self.InstrumentControl.send("CONFigure:SENSe:POWer:TRIGger:OFFSet 0 ")
        self.InstrumentControl.send("CONFigure:SENSe:POWer:TRIGger:TOUT 10")
        self.InstrumentControl.send("CONFigure:SENSe:POWer:TRIGger:MGAP 0")
        self.InstrumentControl.send("CONFigure:SENSe:POWer:TRIGger:MODE ONCE")

        # 开始测量
        self.InstrumentControl.send("INITiate:SENSe:POWer")

        # 等待测量完成
        self.InstrumentControl.send("*OPC?")

        for i in range(100):

            # 查询测量状态
            state = self.InstrumentControl.send("FETCh:SENSe:POWer:STATe?")
            if "RDY" in state:
                break
            else:
                time.sleep(5)

        # 查询统计周期内的current及average功率
        current_power = self.InstrumentControl.send("FETCh:SENSe:POWer:CURRent?")
        average_power = self.InstrumentControl.send("FETCh:SENSe:POWer:AVERage?")
        print(current_power, average_power)

        # 结束测量
        self.InstrumentControl.send("ABORt:SENSe:POWer")


if __name__ == '__main__':
    cw_signals = TransmitHandler()
    cw_signals.transmit_cw_signals("RF6", "1.2E+9", "-30")
    measure_signal = ReceiveHandler()
    measure_signal.measure_power("RF8", "1.2E+9", "-30", "5")
