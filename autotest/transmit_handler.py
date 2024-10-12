#!/usr/bin/env python
# -*- coding: utf-8 -*-


'''程序

@description
    说明
'''
from instrument_control import InstrumentControl


class TransmitHandler():
    def __init__(self):
        self.instrument_control = InstrumentControl()

    def transmit_close(self):
        self.instrument_control.write("CONFigure:SOURce:STATe OFF")

    def transmit_cw_signals(self, rf_port,frequency, power):
        self.frequency = frequency
        self.power = power
        self.rf_port=rf_port
        self.instrument_control.connect()

        # 设置端口
        # 设置端口
        self.instrument_control.write("CONFigure:SOURce:ROUTe:SCENario:SALone RF18")
        self.instrument_control.write("CONFigure:SOURce:ROUTe:USAGe:ALL RF18,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF")
        self.instrument_control.write(f"CONFigure:SOURce:ROUTe:USAGe {self.rf_port},ON")


        # 设置baseband mode 、list模式、external attenuation、dgai
        self.instrument_control.write(command="CONFigure:SOURce:BBMode CW")
        self.instrument_control.write(command="CONFigure:SOURce:LIST OFF")
        self.instrument_control.write(command="CONFigure:SOURce:RFSettings:EATTenuation 0")
        self.instrument_control.write(command="CONFigure:SOURce:RFSettings:DGAin 0")

        # 设置frequency、level
        self.instrument_control.write(f"CONFigure:SOURce:RFSettings:FREQuency {self.frequency}")
        self.instrument_control.write(f"CONFigure:SOURce:RFSettings:LEVel {self.power}")

        # 打开Generator并查询Generator当前状态
        self.instrument_control.write("CONFigure:SOURce:STATe ON")
        self.instrument_control.query("CONFigure:SOURce:STATe?")

        print(f"CW信号已发射：频率 = {self.frequency} Hz, 功率 = {self.power} dBm")

    # 控制仪表发射LTE波形函数
    def transmit_arb_signals(self, rf_port,frequency, power):

        # 设置端口
        self.instrument_control.send("CONFigure:SOURce:ROUTe:SCENario:SALone RF18")
        self.instrument_control.send("CONFigure:SOURce:ROUTe:USAGe:ALL RF18,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF")
        self.instrument_control.send("ONFigure:SOURce:ROUTe:USAGe RF1,ON")

        # 设置baseband mode 、list模式、external attenuation、dgain
        self.instrument_control.send("CONFigure:SOURce:BBMode ARB")
        self.instrument_control.send("CONFigure:SOURce:LIST OFF")
        self.instrument_control.send("CONFigure:SOURce:RFSettings:EATTenuation 0")
        self.instrument_control.send("CONFigure:SOURce:RFSettings:DGAin 0")

        # 设置frequency、level
        self.instrument_control.send("CONFigure:SOURce:RFSettings:FREQuency 1.000000E+009")
        self.instrument_control.send("CONFigure:SOURce:RFSettings:LEVel -70")

        # Load ARB波形，设置repetition，查询波形属性
        self.instrument_control.send("CONFigure:SOURce:ARB:FILE 'LTE_20MHz_64QAM_full_UL.wv'")
        self.instrument_control.send("CONFigure:SOURce:ARB:FILE?")
        self.instrument_control.send("CONFigure:SOURce:ARB:REPetition CONT")
        self.instrument_control.send("CONFigure:SOURce:ARB:FILE:DATE?")
        self.instrument_control.send("CONFigure:SOURce:ARB:FILE:VERSion?")
        self.instrument_control.send("CONFigure:SOURce:ARB:FILE:OPTion?")

        # 设置ARB波形autostart、trigger delay
        self.instrument_control.send("CONFigure:SOURce:TRIGger:ARB:RETRigger ON")
        self.instrument_control.send("CONFigure:SOURce:TRIG:ARB:AUTostart ON")
        self.instrument_control.send("CONFigure:SOURce:TRIGger:ARB:DELay 0")

        # 打开Generator并查询Generator当前状态
        self.instrument_control.send("CONFigure:SOURce:STATe ON")
        self.instrument_control.send("CONFigure:SOURce:STATe?")

        # 查询可靠性
        self.instrument_control.send("CONFigure:SOURce:RELiability:ALL?")

        # 关闭Generator
        self.instrument_control.send("CONFigure:SOURce:STATe OFF")




if __name__ == '__main__':
    cw_signals=TransmitHandler()
    cw_signals.transmit_cw_signals("RF6","1.2E+9", "-30")

