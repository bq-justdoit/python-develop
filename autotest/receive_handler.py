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
        self.instrument_control = InstrumentControl()
        self.instrument_control.connect()

    def measure_power(self, rf_port, frequency, reference_power, margin):

        # 设置端口、list模式、external attenuation 、freq、reference power、 mixLevOffset、freqoffset
        self.instrument_control.send(f"CONFigure:SENSe:POWer:ROUTe:GLOBal {rf_port}")
        self.instrument_control.send("CONFigure:SENSe:POWer:LIST OFF")
        self.instrument_control.send("CONFigure:SENSe:POWer:RFSettings:EATTenuation 0")
        self.instrument_control.send(f"CONFigure:SENSe:POWer:RFSettings:FREQuency {frequency}")
        self.instrument_control.send(f"CONFigure:SENSe:POWer:RFSettings:ENPower {reference_power}")
        self.instrument_control.send(f"CONFigure:SENSe:POWer:RFSettings:UMARgin {margin}")
        self.instrument_control.send("CONFigure:SENSe:POWer:RFSettings:MLOFfset 0")
        self.instrument_control.send("CONFigure:SENSe:POWer:RFSettings:FOFFset 0")

        # 设置超时时间、Step Length、Measurement Length
        self.instrument_control.send("CONFigure:SENSe:POWer:REPetition SINGleshot")
        self.instrument_control.send("CONFigure:SENSe:POWer:TOUT 1")
        self.instrument_control.send("CONFigure:SENSe:POWer:SLENgth 1ms")
        self.instrument_control.send("CONFigure:SENSe:POWer:MLENgth 400E-6")

        # 设置measurement statistics
        self.instrument_control.send("CONFigure:SENSe:POWer:SCOunt 5")

        # 选择30 kHz 高斯滤波器
        self.instrument_control.send("CONFigure:SENSe:POWer:FILTer:TYPE GAUSs")
        self.instrument_control.send("CONFigure:SENSe:POWer:FILTer:GAUSs:BWIDth 30kHz")

        # 设置trigger
        self.instrument_control.send("CONFigure:SENSe:POWer:TRIGger:CATalog:SOURce?")
        self.instrument_control.send("CONFigure:SENSe:POWer:TRIGger:SOURce 'Free Run'")
        self.instrument_control.send("CONFigure:SENSe:POWer:TRIGger:SLOPe REDGe")
        self.instrument_control.send("ONFigure:SENSe:POWer:TRIGger:THReshold -20")
        self.instrument_control.send("CONFigure:SENSe:POWer:TRIGger:OFFSet 0 ")
        self.instrument_control.send("CONFigure:SENSe:POWer:TRIGger:TOUT 10")
        self.instrument_control.send("CONFigure:SENSe:POWer:TRIGger:MGAP 0")
        self.instrument_control.send("CONFigure:SENSe:POWer:TRIGger:MODE ONCE")

        # 开始测量
        self.instrument_control.send("INITiate:SENSe:POWer")

        # 等待测量完成
        self.instrument_control.send("*OPC?")

        for i in range(100):

            # 查询测量状态
            state = self.instrument_control.send("FETCh:SENSe:POWer:STATe?")
            if "RDY" in state:
                break
            else:
                time.sleep(5)

        # 查询统计周期内的current及average功率
        current_power = self.instrument_control.send("FETCh:SENSe:POWer:CURRent?")
        average_power = self.instrument_control.send("FETCh:SENSe:POWer:AVERage?")
        print(current_power, average_power)

        # 结束测量
        self.instrument_control.send("ABORt:SENSe:POWer")

    def close_instrument(self):
        self.instrument_control.close()


if __name__ == '__main__':
    cw_signals = TransmitHandler()
    cw_signals.transmit_cw_signals("RF6", "1.2E+9", "-30")
    measure_signal = ReceiveHandler()
    measure_signal.measure_power("RF8", "1.2E+9", "-30", "5")
    cw_signals.transmit_close()
    measure_signal.close_instrument()
