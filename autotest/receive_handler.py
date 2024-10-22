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

    def measure_lte(self, dic_data):
        """

        :param dic_data: 字典
        :return:
        """
        rf_port = dic_data.get('rf_ports')
        frequency = dic_data.get('frequency')
        signal_type = dic_data.get('signal_type')
        duplex_mode = dic_data.get('duplex_mode')
        bandwidth = dic_data.get('bandwidth')
        ULDL_configuration = dic_data.get('ULDL_configuration', "")
        SpecialSubframe = dic_data.get('SpecialSubframe', "")
        PhsLayerCellID = dic_data.get('PhsLayerCellID')
        DeltaSeqShift = dic_data.get('DeltaSeqShift')
        Repetition = dic_data.get('Repetition')
        ModScheme = dic_data.get('ModScheme', "AUTO")
        trigger_source = dic_data.get('trigger_source', "IF Power")
        TrigThreshold = dic_data.get('TrigThreshold', "-30")

        # 设置signal routing、OFF List模式、external attenuation 、freq、freqoffset、reference power 、mixLevOffset
        self.instrument_control.send(f"CONFigure:SENSe:LTE:ROUTe:GLOBal {rf_port}")
        self.instrument_control.send("CONFigure:SENSe:LTE:MEValuation:LIST OFF")
        self.instrument_control.send("CONFigure:SENSe:LTE:RFSettings:EATTenuation 0")
        self.instrument_control.send(f"CONFigure:SENSe:LTE[:PCC]:RFSettings:FREQuency {frequency}")
        self.instrument_control.send("CONFigure:SENSe:LTE:RFSettings:FOFFset 0")
        self.instrument_control.send("CONFigure:SENSe:LTE:RFSettings:ENPower 20")
        self.instrument_control.send("CONFigure:SENSe:LTE:RFSettings:UMARgin 10")
        self.instrument_control.send("CONFigure:SENSe:LTE:RFSettings:MLOFfset 10")

        # 此命令用于LTE

        self.instrument_control.send(f"CONF:SENS:LTE:STYP {signal_type}")
        if signal_type == 'UL':
            self.instrument_control.send("CONF:SENS:LTE:MEV:SCTYpe PUSCh")

        # 此命令用于LTEV
        if signal_type == 'SL':
            self.instrument_control.send("CONF:SENS:LTE:STYP SL")
            self.instrument_control.send("CONF:SENS:LTE:MEV:SCTYpe PSSCh")
            self.instrument_control.send("")
            self.instrument_control.send("")
            self.instrument_control.send("")
            self.instrument_control.send("")

        # 设置双工模式
        self.instrument_control.send(f"CONFigure:SENSe:LTE:DMODe {duplex_mode}")

        # 设置channel bandwidth、UL-DL configuration、special subframe、cyclic prefix PUCCH format、physical layer cell ID、delta sequence shift value、group hopping
        # B014 | B030 | B050 | B100 | B150 | B200
        self.instrument_control.send(f"CONFigure:SENSe:LTE:CBANdwidth {bandwidth}")
        if duplex_mode == "TDD":
            self.instrument_control.send(f"CONFigure:SENSe:LTE:MEValuation:ULDL {ULDL_configuration}")
            self.instrument_control.send(f"CONFigure:SENSe:LTE:MEValuation:SSUBframe {SpecialSubframe}")
        self.instrument_control.send("CONFigure:SENSe:LTE:MEValuation:CPRefix NORM")
        self.instrument_control.send("CONFigure:SENSe:LTE:MEValuation:PFORmat F1")
        self.instrument_control.send(f"CONFigure:SENSe:LTE:MEValuation:PLCid {PhsLayerCellID}")
        self.instrument_control.send(f"CONFigure:SENSe:LTE:MEValuation:DSSPusch {DeltaSeqShift}")
        self.instrument_control.send("CONFigure:SENSe:LTE:MEValuation:GHOPping OFF")

        # 设置repetition mode 、stop condition,、measurement mode 、error handling、timeout channel type detection、network signaled value、number of resource blocks view filter channel type filter
        self.instrument_control.send(f"CONFigure:SENSe:LTE:MEValuation:REPetition {Repetition}")
        self.instrument_control.send("CONFigure:SENSe:LTE:MEValuation:SCONdition NONE")
        self.instrument_control.send("CONFigure:SENSe:LTE:MEValuation:MMODe NORMal")
        self.instrument_control.send("CONFigure:SENSe:LTE:MEValuation:MOEXception OFF")
        self.instrument_control.send("CONFigure:SENSe:LTE:MEValuation:TOUT 10")
        self.instrument_control.send("CONFigure:SENSe:LTE:MEValuation:CTYPe PUSCh")
        self.instrument_control.send("CONFigure:SENSe:LTE:MEValuation:NSValue NS01")
        self.instrument_control.send("CONFigure:SENSe:LTE:MEValuation:NVFilter OFF")
        self.instrument_control.send("CONFigure:SENSe:LTE:MEValuation:CTVFilter PUSCh")

        # 设置RB检测机制
        # 设置RB number及RB offset
        self.instrument_control.send("CONFigure:SENSe:LTE:MEValuation:RBALlocation:AUTO OFF")
        self.instrument_control.send("CONFigure:SENSe:LTE:MEValuation:RBALlocation:NRB 1")
        self.instrument_control.send("CONFigure:SENSe:LTE:MEValuation:RBALlocation:ORB 0")

        # 设置测量范围：设置Subframe Offset、Subframe Count、Meas Subframe、MeasureSlot/
        self.instrument_control.send("CONFigure:SENSe:LTE:MEValuation:MSUBframes 0,10,2")
        self.instrument_control.send("CONFigure:SENSe:LTE:MEValuation:MSLot ALL")

        # 调制测量设置 ：
        # 设置meas statistics count、modulation scheme、SRS
        # 设置PUCCH和PUSCH的exclusion periods
        # <ModScheme> AUTO | QPSK | Q16 | Q64 | Q256
        self.instrument_control.send("CONFigure:SENSe:LTE:MEValuation:SCOunt:MODulation 20")
        self.instrument_control.send(f"CONFigure:SENSe:LTE:MEValuation:MODulation:MSCHeme {ModScheme}")
        self.instrument_control.send("CONFigure:SENSe:LTE:MEValuation:SRS:ENABle OFF")
        self.instrument_control.send(
            "CONF:SENSe:LTE:MEValuation:MODulation:EWLength 5,12,35,66,102,136,28,58,124,250,374,504")

        # 频谱测量设置：
        # 设置meas statistics count
        # 设置resolution filter type
        # 启用ACLR所有adjacent channels evaluation
        self.instrument_control.send("CONFigure:SENSe:LTE:MEValuation:SCOunt:SPECtrum:ACLR 30")
        self.instrument_control.send("CONFigure:SENSe:LTE:MEValuation:SCOunt:SPECtrum:SEMask 30")
        self.instrument_control.send("CONFigure:SENSe:LTE:MEValuation:SPECtrum:SEMask:MFILter GAUSs")
        self.instrument_control.send("CONFigure:SENSe:LTE:MEValuation:SPECtrum:ACLR:ENABle ON,ON,ON")

        # 功率测量设置:
        # 设置 high dynamic mode、statistic count
        self.instrument_control.send("CONFigure:SENSe:LTE:MEValuation:POWer:HDMode OFF")
        self.instrument_control.send("CONFigure:SENSe:LTE:MEValuation:SCOunt:POWer 30")

        # 设置trigger source、timeout、 trigger level、 slope、delay、minimum trigger gap、synchronization mode、acquisition mode
        self.instrument_control.send("CONFigure:SENSe:LTE:MEValuation:TRIGger:CATalog:SOURce?")
        self.instrument_control.send(f"CONFigure:SENSe:LTE:MEValuation:TRIGger:SOURce '{trigger_source}'")
        self.instrument_control.send("CONFigure:SENSe:LTE:MEValuation:TRIGger:TOUT 1")
        self.instrument_control.send(f"CONFigure:SENSe:LTE:MEValuation:TRIGger:THReshold {TrigThreshold}")
        self.instrument_control.send("CONFigure:SENSe:LTE:MEValuation:TRIGger:SLOPe REDGe")
        self.instrument_control.send("CONFigure:SENSe:LTE:MEValuation:TRIGger:DELay 0")
        self.instrument_control.send("CONFigure:SENSe:LTE:MEValuation:TRIGger:MGAP 1")

        # 设置QPSK modulation limits
        self.instrument_control.send("CONFigure:SENSe:LTE:MEValuation:LIMit:QPSK:EVMagnitude 20, 40")
        self.instrument_control.send("CONFigure:SENSe:LTE:MEValuation:LIMit:QPSK:MERRor 20, OFF")
        self.instrument_control.send("CONFigure:SENSe:LTE:MEValuation:LIMit:QPSK:PERRor 20, OFF")
        self.instrument_control.send("CONFigure:SENSe:LTE:MEValuation:LIMit:QPSK:FERRor 0.15")
        self.instrument_control.send("CONFigure:SENSe:LTE:MEValuation:LIMit:QPSK:IQOFfset ON, -26, -21, -11")
        self.instrument_control.send("CONFigure:SENSe:LTE:MEValuation:LIMit:QPSK:IBE ON, -20, 20, -60, -27")
        self.instrument_control.send("CONFigure:SENSe:LTE:MEValuation:LIMit:QPSK:IBE:IQOFfset -26, -21, -11")
        self.instrument_control.send("CONFigure:SENSe:LTE:MEValuation:LIMit:QPSK:ESFLatness ON, 5, 9, 6, 8, 3MHz")

        # 设置ACLR limits
        self.instrument_control.send("CONFigure:SENSe:LTE:MEValuation:LIMit:ACLR:UTRA1:CBANdwidth100 35, -50")
        self.instrument_control.send("CONFigure:SENSe:LTE:MEValuation:LIMit:ACLR:EUTRa:CBANdwidth100 32, -50")

        # 设置spectrum emission limits
        self.instrument_control.send("CONFigure:SENSe:LTE:MEValuation:LIMit:SEMask:OBWLimit:CBANdwidth100 1.2E+6")
        self.instrument_control.send("CONFigure:SENSe:LTE:MEV:LIMit:SEM:LIMit1:CBANdwidth100 ON,1e+006, -16.5, K030")
        self.instrument_control.send(
            "CONFigure:SENSe:LTE:MEV:LIMit:SEM:LIMit1:ADD3:CBANdwidth100 ON,2E+4,1E+6,-15,K030")

        # 使能测量项
        self.instrument_control.send(
            "CONFigure:SENSe:LTE:MEValuation:RESult:ALL ON,ON,ON,ON,ON,ON,ON,ON,ON,ON,ON,ON,ON,ON")

        # 开启测量
        self.instrument_control.send("INITiate:SENSe:LTE:MEValuation")
        self.instrument_control.send("CONFigure:SENSe:LTE:MEValuation:RELiability:ALL?")

        # # 等待测量完成
        # self.instrument_control.send("*OPC?")

        for i in range(100):

        # 查询测量状态
            state = self.instrument_control.send("FETCh:SENSe:LTE:MEValuation:STATe:ALL?")
            if "RDY" in state:
                break
            else:
                time.sleep(5)

        # 查询modulation结果
        self.instrument_control.send("FETCh:SENSe:LTE:MEValuation:EVMagnitude:MAXimum?")
        self.instrument_control.send("FETCh:SENSe:LTE:MEValuation:TRACe:EVMC?")
        self.instrument_control.send("FETCh:SENSe:LTE:MEValuation:MERRor:AVERage?")
        self.instrument_control.send("FETCh:SENSe:LTE:MEValuation:MERRor:MAXimum?")
        self.instrument_control.send("FETCh:SENSe:LTE:MEValuation:PERRor:AVERage?")
        self.instrument_control.send("FETCh:SENSe:LTE:MEValuation:PERRor:MAXimum?")
        self.instrument_control.send("FETCh:SENSe:LTE:MEValuation:MODulation:CURRent?")
        self.instrument_control.send("FETCh:SENSe:LTE:MEValuation:MODulation:EXTReme?")

        # 查询inband emission结果
        self.instrument_control.send("FETCh:SENSe:LTE:MEValuation:TRACe:IEMissions?")
        self.instrument_control.send("FETCh:SENSe:LTE:MEValuation:IEMission:MARGin:CURRent?")
        self.instrument_control.send("FETCh:SENSe:LTE:MEValuation:IEMission:MARGin:CURRent:RBINdex?")

        # 查询equalizer spectrum flatness结果
        # self.instrument_control.send("FETCh:SENSe:LTE:MEValuation:TRACe:ESFLatness?")
        self.instrument_control.send("FETCh:SENSe:LTE:MEValuation:ESFLatness:AVERage?")
        self.instrument_control.send("FETCh:SENSe:LTE:MEValuation:ESFLatness:CURRent:SCINdex?")

        # 查询spectrum emission结果
        self.instrument_control.send("FETCh:SENSe:LTE:MEValuation:TRACe:SEMask:RBW30:CURRent?")
        self.instrument_control.send("FETCh:SENSe:LTE:MEValuation:TRACe:SEMask:RBW100:AVERage?")
        self.instrument_control.send("FETCh:SENSe:LTE:MEValuation:SEMask:CURRent?")
        self.instrument_control.send("FETCh:SENSe:LTE:MEValuation:SEMask:EXTReme?")
        self.instrument_control.send("FETCh:SENSe:LTE:MEValuation:SEMask:MARGin?")
        self.instrument_control.send("FETCh:SENSe:LTE:MEValuation:SEMask:MARGin:MINimum:POSitiv?")
        self.instrument_control.send("FETCh:SENSe:LTE:MEValuation:SEMask:MARGin:CURRent:NEGativ?")

        # 查询ACLR结果
        self.instrument_control.send("FETCh:SENSe:LTE:MEValuation:TRACe:ACLR:CURRent?")
        self.instrument_control.send("FETCh:SENSe:LTE:MEValuation:TRACe:ACLR:AVERage?")
        self.instrument_control.send("FETCh:SENSe:LTE:MEValuation:ACLR:CURRent?")

        # 查询power monitor结果
        self.instrument_control.send("FETCh:SENSe:LTE:MEValuation:TRACe:PMONitor?")
        self.instrument_control.send("FETCh:SENSe:LTE:MEValuation:PMONitor:AVERage?")

        # 查询测试结果
        self.instrument_control.send("CALCulate:SENSe:LTE:MEValuation:ACLR:CURRent?")
        self.instrument_control.send("CALCulate:SENSe:LTE:MEValuation:SEMask:CURRent?")
        self.instrument_control.send("CALCulate:SENSe:LTE:MEValuation:ESFLatness:CURRent?")
        self.instrument_control.send("CALCulate:SENSe:LTE:MEValuation:MODulation:CURRent?")

        # 结束测量
        self.instrument_control.send("ABORt:SENSe:LTE:MEValuation")


if __name__ == '__main__':
    # cw_signals = TransmitHandler()
    # cw_signals.transmit_cw_signals("RF6", "1.2E+9", "-30")
    # measure_signal = ReceiveHandler()
    # measure_signal.measure_power("RF8", "1.2E+9", "-30", "5")
    # cw_signals.transmit_close()
    # measure_signal.close_instrument()

    lte_signals = TransmitHandler()
    arb_file = "MTK_LTE_FDD_5M_OCNG.wv"
    lte_signals.transmit_arb_signals("RF6", "1.2E+9", "-30", arb_file)
    measure_lte_signal = ReceiveHandler()
    dic_data = {
        "rf_port": "RF8",
        "frequency": "1.2E+9",
        "signal_type": "UL",
        "duplex_mode": "FDD",
        "bandwidth": "B050",
        "ULDL_configuration": "1",
        "SpecialSubframe": "0",
        "PhsLayerCellID": "1",
        "DeltaSeqShift": "0",
        "Repetition": "SING",
        "ModScheme": "QPSK",
        "trigger_source": "Free Run (Fast Sync)",
        "TrigThreshold": "-30",
    }
    measure_lte_signal.measure_lte(dic_data)
    # measure_lte_signal.close_instrument()
