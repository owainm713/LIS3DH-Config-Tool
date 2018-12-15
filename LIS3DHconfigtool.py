#!/usr/bin/env python3
"""LIS3DHconfigtool, configuration tool to help manually
configure the registers of an LIS3DH accelerometer

created December 9, 2018
modified December 15, 2018 """

"""
Copyright 2018 Owain Martin

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from tkinter import *  

    
class LIS3DHConfigGui:

    def __init__(self, master):


        #-------- accelerometer set up ---------------

        # set up registers to match default value

        self.CTRL_REG1 = 0x07
        self.CTRL_REG2 = 0x00
        self.CTRL_REG3 = 0x00
        self.CTRL_REG4 = 0x00
        self.CTRL_REG5 = 0x00
        self.CTRL_REG6 = 0x00

        self.TEMP_CFG_REG = 0x00
        self.FIFO_CTRL_REG = 0x00
        
        self.INT1_CFG = 0x00        
        self.INT1_THS = 0x00
        self.INT1_DURATION = 0x00

        self.CLICK_CFG = 0x00        
        self.CLICK_THS = 0x00
        self.TIME_LIMIT = 0x00
        self.TIME_LATENCY = 0x00
        self.TIME_WINDOW = 0x00
        
        # misc variable declarations
        self.adc = StringVar(value = 'off')         # ADC enable/disable
        self.bdu = StringVar(value = 'off')         # Block Data Update - BDU
        self.endian = StringVar(value = 'little')
        self.fourD = StringVar(value = 'off')       # 4D detection enable (default is 6D)
        self.intLevel = StringVar(value = 'high')   # interrupt active level   
        self.latch = StringVar(value = 'off')       # interrupt latch         
        self.odr = IntVar(value = 50)
        self.powerMode = StringVar(value = 'Off')
        self.resolution = StringVar(value = 'low')         
        self.scale = IntVar(value = 2)
        self.temperature = StringVar(value = 'off') # On board temperature sensor reading enable/disable
        self.xAxis = StringVar(value = 'on')
        self.yAxis = StringVar(value = 'on')
        self.zAxis = StringVar(value = 'on')

        # FIFO variables
        self.fifoEnable = StringVar(value = 'off')
        self.fifoMode = StringVar(value = 'bypass')
        self.fifoThreshold = IntVar(value = 0)

        # High pass filter variables
        self.hpfMode= StringVar(value = 'normalreset')
        self.hpfCutOff = IntVar(value = 0)
        self.hpfFDS = StringVar(value = 'off')
        self.hpfClick = StringVar(value = 'off')
        self.hpfIS2 = StringVar(value = 'off')
        self.hpfIS1 = StringVar(value = 'off')
        

        # int1 variables - CTRL_REG3
        self.int1_aoi1 =IntVar(value = 0)
        self.int1_aoi2 =IntVar(value = 0)
        self.int1_click =IntVar(value = 0)
        self.int1_drdy1 =IntVar(value = 0)
        self.int1_drdy2 =IntVar(value = 0)
        self.int1_wtm =IntVar(value = 0)
        self.int1_overrun =IntVar(value = 0)

        # int1 config variables - INT1_CFG
        self.int1_aoi = IntVar(value = 0)
        self.int1_d6 = IntVar(value = 0)
        self.int1_zh = IntVar(value = 0)
        self.int1_zl = IntVar(value = 0)
        self.int1_yh = IntVar(value = 0)
        self.int1_yl = IntVar(value = 0)
        self.int1_xh = IntVar(value = 0)
        self.int1_xl = IntVar(value = 0)

        self.int1_duration = IntVar(value = 0)
        self.int1_threshold = IntVar(value = 0)

        # click config variables - CLICK_CFG
        self.click_zd = IntVar(value = 0)
        self.click_zs = IntVar(value = 0)
        self.click_yd = IntVar(value = 0)
        self.click_ys = IntVar(value = 0)
        self.click_xd = IntVar(value = 0)
        self.click_xs = IntVar(value = 0)

        self.click_threshold = IntVar(value = 0)
        self.click_timelimit = IntVar(value = 0)
        self.click_timelatency = IntVar(value = 0)
        self.click_timewindow = IntVar(value = 0)
        
        self.regValueText = StringVar()

        #------------ GUI set up --------------------------

        fgColour = 'green'

        # set up main options frame area
        self.optionFrame = LabelFrame(master, text = 'LIS3DH Options', fg = fgColour)
        self.optionFrame.grid(row = 0, column = 0, padx= 5, pady= 5, sticky = (N,S,W,E))

        # set up power mode options
        self.pwrModeOptionsFrame = LabelFrame(self.optionFrame, text = 'Power Mode Options', fg = fgColour)
        self.pwrModeOptionsFrame.grid(row = 0, column = 0, padx= 5, pady= 5, sticky = (N,S,W,E))
        pmButton1 = Radiobutton(self.pwrModeOptionsFrame,text = 'Normal',variable = self.powerMode, value = 'Normal'
                                ,command = self.set_ODR, fg = fgColour)
        pmButton1.grid(row = 0, column = 0)
        pmButton2 = Radiobutton(self.pwrModeOptionsFrame,text = 'Low',variable = self.powerMode, value = 'Low'
                                ,command = self.set_ODR, fg = fgColour)
        pmButton2.grid(row = 0, column = 1)
        pmButton3 = Radiobutton(self.pwrModeOptionsFrame,text = 'Off',variable = self.powerMode, value = 'Off'
                                ,command = self.set_ODR, fg = fgColour)
        pmButton3.grid(row = 0, column = 2)

        #set up output data rate (ODR) options
        self.odrOptionsFrame = LabelFrame(self.optionFrame, text = 'ODR Options (Hz)', fg = fgColour)
        self.odrOptionsFrame.grid(row = 1, column = 0, columnspan = 2, padx= 5, pady= 5, sticky = (N,S,W,E))
        odrButton1 = Radiobutton(self.odrOptionsFrame,text = '1',variable = self.odr, value = 1
                                ,command = self.set_ODR, fg = fgColour)
        odrButton1.grid(row = 0, column = 0, sticky = W)
        odrButton2 = Radiobutton(self.odrOptionsFrame,text = '10',variable = self.odr, value = 10
                                ,command = self.set_ODR, fg = fgColour)
        odrButton2.grid(row = 0, column = 1, sticky = W)
        odrButton3 = Radiobutton(self.odrOptionsFrame,text = '25',variable = self.odr, value = 25
                                ,command = self.set_ODR, fg = fgColour)
        odrButton3.grid(row = 0, column = 2, sticky = W)
        odrButton4 = Radiobutton(self.odrOptionsFrame,text = '50' ,variable = self.odr, value = 50
                                ,command = self.set_ODR, fg = fgColour)
        odrButton4.grid(row = 0, column = 3)
        odrButton5 = Radiobutton(self.odrOptionsFrame,text = '100' ,variable = self.odr, value = 100
                                ,command = self.set_ODR, fg = fgColour)
        odrButton5.grid(row = 0, column = 4)
        odrButton6 = Radiobutton(self.odrOptionsFrame,text = '200',variable = self.odr, value = 200
                                ,command = self.set_ODR, fg = fgColour)
        odrButton6.grid(row = 0, column = 5)
        odrButton7 = Radiobutton(self.odrOptionsFrame,text = '400',variable = self.odr, value = 400
                                ,command = self.set_ODR, fg = fgColour)
        odrButton7.grid(row = 1, column = 0)
        odrButton8 = Radiobutton(self.odrOptionsFrame,text = '1.6k',variable = self.odr, value = 1600
                                ,command = self.set_ODR, fg = fgColour)
        odrButton8.grid(row = 1, column = 1)
        odrButton9 = Radiobutton(self.odrOptionsFrame,text = '1.25k',variable = self.odr, value = 1250
                                ,command = self.set_ODR, fg = fgColour)
        odrButton9.grid(row = 1, column = 2)
        odrButton10 = Radiobutton(self.odrOptionsFrame,text = '5k',variable = self.odr, value = 5000
                                ,command = self.set_ODR, fg = fgColour)
        odrButton10.grid(row = 1, column = 3)

        # set up scale options
        self.scaleOptionsFrame = LabelFrame(self.optionFrame, text = 'Scale Options (+/-g)', fg = fgColour)
        self.scaleOptionsFrame.grid(row = 0, column = 1, padx= 5, pady= 5, sticky = (N,S,W,E))
        scaleButton1 = Radiobutton(self.scaleOptionsFrame,text = '2',variable = self.scale, value = 2
                                ,command = self.set_scale, fg = fgColour)
        scaleButton1.grid(row = 0, column = 0, sticky = W)
        
        scaleButton2 = Radiobutton(self.scaleOptionsFrame,text = '4',variable = self.scale, value = 4
                                ,command = self.set_scale, fg = fgColour)
        scaleButton2.grid(row = 0, column = 1, sticky = W)
        
        scaleButton3 = Radiobutton(self.scaleOptionsFrame,text = '8',variable = self.scale, value = 8
                                ,command = self.set_scale, fg = fgColour)
        scaleButton3.grid(row = 0, column = 2, sticky = W)
        
        scaleButton4 = Radiobutton(self.scaleOptionsFrame,text = '16',variable = self.scale, value = 16
                                ,command = self.set_scale, fg = fgColour)
        scaleButton4.grid(row = 0, column = 3, sticky = W)

        # set up x, y & z axis enable options
        self.axisOptionsFrame = LabelFrame(self.optionFrame, text = 'Axis Enables', fg = fgColour)
        self.axisOptionsFrame.grid(row = 2, column = 0, padx= 5, pady= 5, sticky = (N,S,W,E))
        xButton = Checkbutton(self.axisOptionsFrame, text = 'x-axis', variable = self.xAxis, onvalue = 'on',
                              offvalue = 'off', command = self.axis_enable, fg = fgColour)
        xButton.grid(row = 0, column = 0)
        
        yButton = Checkbutton(self.axisOptionsFrame, text = 'y-axis', variable = self.yAxis, onvalue = 'on',
                              offvalue = 'off', command = self.axis_enable, fg = fgColour)
        yButton.grid(row = 0, column = 1)

        zButton = Checkbutton(self.axisOptionsFrame, text = 'z-axis', variable = self.zAxis, onvalue = 'on',
                              offvalue = 'off', command = self.axis_enable, fg = fgColour)
        zButton.grid(row = 0, column = 2)
        
        # set up resolution option area
        self.resolutionOptionsFrame = LabelFrame(self.optionFrame, text = 'Resolution Options', fg = fgColour)
        self.resolutionOptionsFrame.grid(row = 2, column = 1, columnspan = 2, padx= 5, pady= 5, sticky = (N,S,W,E))
        resLowButton = Radiobutton(self.resolutionOptionsFrame,text = 'Low',variable = self.resolution, value = 'low'
                                ,command = self.set_resolution, fg = fgColour)
        resLowButton.grid(row = 0, column = 0, sticky = W)
        
        resHighButton = Radiobutton(self.resolutionOptionsFrame,text = 'High',variable = self.resolution, value = 'high'
                                ,command = self.set_resolution, fg = fgColour)
        resHighButton.grid(row = 0, column = 1, sticky = W)

        # set up misc options area - includes BDU, 4D/6D, ADC & Temperature enable
        self.miscOptionsFrame = LabelFrame(self.optionFrame, text = 'Miscellaneous Options', fg = fgColour)
        self.miscOptionsFrame.grid(row = 3, column = 0, padx= 5, pady= 5, sticky = (N,S,W,E))
        bduButton = Checkbutton(self.miscOptionsFrame, text = 'BDU', variable = self.bdu, onvalue = 'on',
                              offvalue = 'off', command = self.set_BDU, fg = fgColour)
        bduButton.grid(row = 0, column = 0)        

        fourDButton = Radiobutton(self.miscOptionsFrame,text = '4D',variable = self.fourD, value = 'on'
                                ,command = self.set_4D, fg = fgColour)
        fourDButton.grid(row = 0, column = 1)
        
        sixDButton = Radiobutton(self.miscOptionsFrame,text = '6D',variable = self.fourD, value = 'off'
                                ,command = self.set_4D, fg = fgColour)
        sixDButton.grid(row = 0, column = 2)

        adcButton = Checkbutton(self.miscOptionsFrame, text = 'ADC', variable = self.adc, onvalue = 'on',
                              offvalue = 'off', command = self.set_adc, fg = fgColour)
        adcButton.grid(row = 1, column = 0)

        tempButton = Checkbutton(self.miscOptionsFrame, text = 'Temperature', variable = self.temperature, onvalue = 'on',
                              offvalue = 'off', command = self.set_temperature, fg = fgColour)
        tempButton.grid(row = 1, column = 1, columnspan = 2)

        # set up endian option area
        self.endianOptionsFrame = LabelFrame(self.optionFrame, text = 'Endian Options', fg = fgColour)
        self.endianOptionsFrame.grid(row = 3, column = 1, columnspan = 2, padx= 5, pady= 5, sticky = (N,S,W,E))
        littleEndButton = Radiobutton(self.endianOptionsFrame,text = 'Little',variable = self.endian, value = 'little'
                                ,command = self.set_endian, fg = fgColour)
        littleEndButton.grid(row = 0, column = 0, sticky = W)
        
        bigEndButton = Radiobutton(self.endianOptionsFrame,text = 'Big',variable = self.endian, value = 'big'
                                ,command = self.set_endian, fg = fgColour)
        bigEndButton.grid(row = 0, column = 1, sticky = W)

        # set up FIFO options area
        self.fifoOptionsFrame = LabelFrame(self.optionFrame, text = 'FIFO Options', fg = fgColour)
        self.fifoOptionsFrame.grid(row = 4, column = 0, columnspan = 2, padx= 5, pady= 5, sticky = (N,S,W,E))
        fifoEnButton = Checkbutton(self.fifoOptionsFrame, text = 'FIFO Enable', variable = self.fifoEnable, onvalue = 'on',
                              offvalue = 'off', command = self.set_fifo_mode, fg = fgColour)
        fifoEnButton.grid(row = 0, column = 0, columnspan = 2, sticky = W)

        fifoBypassButton = Radiobutton(self.fifoOptionsFrame,text = 'Bypass',variable = self.fifoMode, value = 'bypass'
                                ,command = self.set_fifo_mode, fg = fgColour)
        fifoBypassButton.grid(row = 1, column = 0, sticky = W)

        fifofifoButton = Radiobutton(self.fifoOptionsFrame,text = 'FIFO',variable = self.fifoMode, value = 'fifo'
                                ,command = self.set_fifo_mode, fg = fgColour)
        fifofifoButton.grid(row = 1, column = 1)

        fifoStreamButton = Radiobutton(self.fifoOptionsFrame,text = 'Stream',variable = self.fifoMode, value = 'stream'
                                ,command = self.set_fifo_mode, fg = fgColour)
        fifoStreamButton.grid(row = 1, column = 2)

        fifoTriggerButton = Radiobutton(self.fifoOptionsFrame,text = 'Trigger/Stream2FIFO',variable = self.fifoMode, value = 'streamfifo'
                                ,command = self.set_fifo_mode, fg = fgColour)
        fifoTriggerButton.grid(row = 1, column = 3)

        # set up FIFO threshold text entry
        fifoThresholdLabel = Label(self.fifoOptionsFrame, text = 'Threshold (0-31):', fg = fgColour, anchor = W)
        fifoThresholdLabel.grid(row = 2, column = 0, columnspan = 2)
        fifoThresholdText = Entry(self.fifoOptionsFrame, width = 3, fg = fgColour,textvariable = self.fifoThreshold)
        fifoThresholdText.grid(row = 2, column = 2, sticky = W)
        fifoThresholdText.bind("<Return>", self.set_fifo_threshold)
        fifoThresholdText.bind("<FocusOut>", self.set_fifo_threshold)

        # set up High Pass Filter Mode options area
        self.HPFModeOptionsFrame = LabelFrame(self.optionFrame, text = 'High Pass Filter Mode Options', fg = fgColour)
        self.HPFModeOptionsFrame.grid(row = 5, column = 0, columnspan = 2, padx= 5, pady= 5, sticky = (N,S,W,E))        

        hpNormalButton = Radiobutton(self.HPFModeOptionsFrame,text = 'Normal',variable = self.hpfMode, value = 'normal'
                                ,command = self.set_highpass_filter, fg = fgColour)
        hpNormalButton.grid(row = 0, column = 0, sticky = W)
        
        hpNormalResetButton = Radiobutton(self.HPFModeOptionsFrame,text = 'Normal Reset',variable = self.hpfMode, value = 'normalreset'
                                ,command = self.set_highpass_filter, fg = fgColour)
        hpNormalResetButton.grid(row = 0, column = 1, sticky = W)

        hpReferenceButton = Radiobutton(self.HPFModeOptionsFrame,text = 'Reference',variable = self.hpfMode, value = 'reference'
                                ,command = self.set_highpass_filter, fg = fgColour)
        hpReferenceButton.grid(row = 0, column = 2, sticky = W)

        hpAutoresetButton = Radiobutton(self.HPFModeOptionsFrame,text = 'Autoreset',variable = self.hpfMode, value = 'autoreset'
                                ,command = self.set_highpass_filter, fg = fgColour)
        hpAutoresetButton.grid(row = 0, column = 3, sticky = W)

        hpFDSButton = Checkbutton(self.HPFModeOptionsFrame, text = 'FDS', variable = self.hpfFDS, onvalue = 'on',
                              offvalue = 'off', command = self.set_highpass_filter, fg = fgColour)
        hpFDSButton.grid(row = 1, column = 0, sticky = W)

        hpClickButton = Checkbutton(self.HPFModeOptionsFrame, text = 'HPCLICK', variable = self.hpfClick, onvalue = 'on',
                              offvalue = 'off', command = self.set_highpass_filter, fg = fgColour)
        hpClickButton.grid(row = 1, column = 1, sticky = W)

        hpIS2Button = Checkbutton(self.HPFModeOptionsFrame, text = 'HPIS2', variable = self.hpfIS2, onvalue = 'on',
                              offvalue = 'off', command = self.set_highpass_filter, fg = fgColour)
        hpIS2Button.grid(row = 1, column = 2, sticky = W)

        hpIS1Button = Checkbutton(self.HPFModeOptionsFrame, text = 'HPIS1', variable = self.hpfIS1, onvalue = 'on',
                              offvalue = 'off', command = self.set_highpass_filter, fg = fgColour)
        hpIS1Button.grid(row = 1, column = 3, sticky = W)

        # set up High Pass Filter Cut-off frequency text entry
        hpCutOffLabel = Label(self.HPFModeOptionsFrame, text = 'HPC Value (0-3):', fg = fgColour, anchor = W)
        hpCutOffLabel.grid(row = 2, column = 0, columnspan = 1, sticky = W)
        hpCutOffText = Entry(self.HPFModeOptionsFrame, width = 3, fg = fgColour,textvariable = self.hpfCutOff)
        hpCutOffText.grid(row = 2, column = 1, sticky = W)
        hpCutOffText.bind("<Return>", self.set_highpass_filter)
        hpCutOffText.bind("<FocusOut>", self.set_highpass_filter)

        

        # set up interrupt pin output options - Active High/Low and Latch On/Off
        self.interruptOptionsFrame = LabelFrame(self.optionFrame, text = 'Interrupt Options', fg = fgColour)
        self.interruptOptionsFrame.grid(row = 6, column = 0, columnspan = 2, padx= 5, pady= 5, sticky = (N,S,W,E))
        latchButton = Checkbutton(self.interruptOptionsFrame, text = 'Latch', variable = self.latch, onvalue = 'on',
                              offvalue = 'off', command = self.latch_interrupt, fg = fgColour)
        latchButton.grid(row = 0, column = 2)

        intLowButton = Radiobutton(self.interruptOptionsFrame,text = 'Active Low',variable = self.intLevel, value = 'low'
                                ,command = self.interrupt_high_low, fg = fgColour)
        intLowButton.grid(row = 0, column = 0, sticky = W)
        
        intHighButton = Radiobutton(self.interruptOptionsFrame,text = 'Active High',variable = self.intLevel, value = 'high'
                                ,command = self.interrupt_high_low, fg = fgColour)
        intHighButton.grid(row = 0, column = 1, sticky = W)

        # set up Interrupt 1 output options        
        self.int1OptionsFrame = LabelFrame(self.optionFrame, text = 'Int1 Output Options - CTRL_REG3', fg = fgColour)
        self.int1OptionsFrame.grid(row = 7, column = 0, columnspan = 2, padx= 5, pady= 5, sticky = (N,S,W,E))
        click1Button = Checkbutton(self.int1OptionsFrame, text = 'Click', variable = self.int1_click, onvalue = 1,
                              offvalue = 0, command = self.set_int1_pin, fg = fgColour)
        click1Button.grid(row = 0, column = 0, sticky = W)
        
        aoi1Button = Checkbutton(self.int1OptionsFrame, text = 'AOI1', variable = self.int1_aoi1, onvalue = 1,
                              offvalue = 0, command = self.set_int1_pin, fg = fgColour)
        aoi1Button.grid(row = 0, column = 1, sticky = W)
        
        aoi2Button = Checkbutton(self.int1OptionsFrame, text = 'AOI2', variable = self.int1_aoi2, onvalue = 1,
                              offvalue = 0, command = self.set_int1_pin, fg = fgColour)
        aoi2Button.grid(row = 0, column = 2)
        
        drdy1Button = Checkbutton(self.int1OptionsFrame, text = 'DRDY1', variable = self.int1_drdy1, onvalue = 1,
                              offvalue = 0, command = self.set_int1_pin, fg = fgColour)
        drdy1Button.grid(row = 0, column = 3)
        
        drdy2Button = Checkbutton(self.int1OptionsFrame, text = 'DRDY2', variable = self.int1_drdy2, onvalue = 1,
                              offvalue = 0, command = self.set_int1_pin, fg = fgColour)
        drdy2Button.grid(row = 0, column = 4)
        
        wtm1Button = Checkbutton(self.int1OptionsFrame, text = 'Watermark', variable = self.int1_wtm, onvalue = 1,
                              offvalue = 0, command = self.set_int1_pin, fg = fgColour)
        wtm1Button.grid(row = 1, column = 0, sticky = W)
        
        overrun1Button = Checkbutton(self.int1OptionsFrame, text = 'Overrun', variable = self.int1_overrun, onvalue = 1,
                              offvalue = 0, command = self.set_int1_pin, fg = fgColour)
        overrun1Button.grid(row = 1, column = 1)

        # set up Interrupt 1 configuration area       
        self.int1ConfigFrame = LabelFrame(self.optionFrame, text = 'Int1 Configuration', fg = fgColour)
        self.int1ConfigFrame.grid(row = 8, column = 0, columnspan = 2, padx= 5, pady= 5, sticky = (N,S,W,E))        
        aoiButton = Checkbutton(self.int1ConfigFrame, text = 'AOI', variable = self.int1_aoi, onvalue = 1,
                              offvalue = 0, command = self.set_int1_config, fg = fgColour)
        aoiButton.grid(row = 0, column = 0, sticky = W)
        
        d6Button = Checkbutton(self.int1ConfigFrame, text = '6D', variable = self.int1_d6, onvalue = 1,
                              offvalue = 0, command = self.set_int1_config, fg = fgColour)
        d6Button.grid(row = 0, column = 1, sticky = W)
        
        zhButton = Checkbutton(self.int1ConfigFrame, text = 'ZH/ZUP', variable = self.int1_zh, onvalue = 1,
                              offvalue = 0, command = self.set_int1_config, fg = fgColour)
        zhButton.grid(row = 0, column = 2, sticky = W)
        
        zlButton = Checkbutton(self.int1ConfigFrame, text = 'ZL/ZDOWN', variable = self.int1_zl, onvalue = 1,
                              offvalue = 0, command = self.set_int1_config, fg = fgColour)
        zlButton.grid(row = 0, column = 3, sticky = W)
        
        yhButton = Checkbutton(self.int1ConfigFrame, text = 'YH/YUP', variable = self.int1_yh, onvalue = 1,
                              offvalue = 0, command = self.set_int1_config, fg = fgColour)
        yhButton.grid(row = 1, column = 0, sticky = W)
        
        ylButton = Checkbutton(self.int1ConfigFrame, text = 'YL/YDOWN', variable = self.int1_yl, onvalue = 1,
                              offvalue = 0, command = self.set_int1_config, fg = fgColour)
        ylButton.grid(row = 1, column = 1, sticky = W)

        xhButton = Checkbutton(self.int1ConfigFrame, text = 'XH/XUP', variable = self.int1_xh, onvalue = 1,
                              offvalue = 0, command = self.set_int1_config, fg = fgColour)
        xhButton.grid(row = 1, column = 2, sticky = W)
        
        xlButton = Checkbutton(self.int1ConfigFrame, text = 'XL/XDOWN', variable = self.int1_xl, onvalue = 1,
                              offvalue = 0, command = self.set_int1_config, fg = fgColour)
        xlButton.grid(row = 1, column = 3, sticky = W)

        # set up INT1 duration text entry
        durationLabel = Label(self.int1ConfigFrame, text = 'Duration (ms):', fg = fgColour, anchor = W)
        durationLabel.grid(row = 2, column = 0)
        durationText = Entry(self.int1ConfigFrame, width=6, fg = fgColour,textvariable = self.int1_duration)
        durationText.grid(row = 2, column = 1)
        durationText.bind("<Return>", self.set_int1_duration)
        durationText.bind("<FocusOut>", self.set_int1_duration)

        # set up INT1 threshold text entry
        thresholdLabel = Label(self.int1ConfigFrame, text = 'Threshold (mg):', fg = fgColour, anchor = W)
        thresholdLabel.grid(row = 2, column = 2)
        thresholdText = Entry(self.int1ConfigFrame, width=6, fg = fgColour,textvariable = self.int1_threshold)
        thresholdText.grid(row = 2, column = 3)
        thresholdText.bind("<Return>", self.set_int1_threshold)
        thresholdText.bind("<FocusOut>", self.set_int1_threshold)

        # set up click configuration area       
        self.clickConfigFrame = LabelFrame(self.optionFrame, text = 'Click Configuration', fg = fgColour)
        self.clickConfigFrame.grid(row = 9, column = 0, columnspan = 2, padx= 5, pady= 5, sticky = (N,S,W,E))
        zdButton = Checkbutton(self.clickConfigFrame, text = 'ZD', variable = self.click_zd, onvalue = 1,
                              offvalue = 0, command = self.set_click_config, fg = fgColour)
        zdButton.grid(row = 0, column = 0, sticky = W)

        zsButton = Checkbutton(self.clickConfigFrame, text = 'ZS', variable = self.click_zs, onvalue = 1,
                              offvalue = 0, command = self.set_click_config, fg = fgColour)
        zsButton.grid(row = 0, column = 1, sticky = W)
        
        ydButton = Checkbutton(self.clickConfigFrame, text = 'YD', variable = self.click_yd, onvalue = 1,
                              offvalue = 0, command = self.set_click_config, fg = fgColour)
        ydButton.grid(row = 0, column = 2, sticky = W)

        ysButton = Checkbutton(self.clickConfigFrame, text = 'YS', variable = self.click_ys, onvalue = 1,
                              offvalue = 0, command = self.set_click_config, fg = fgColour)
        ysButton.grid(row = 0, column = 3, sticky = W)

        xdButton = Checkbutton(self.clickConfigFrame, text = 'XD', variable = self.click_xd, onvalue = 1,
                              offvalue = 0, command = self.set_click_config, fg = fgColour)
        xdButton.grid(row = 0, column = 4, sticky = W)

        xsButton = Checkbutton(self.clickConfigFrame, text = 'XS', variable = self.click_xs, onvalue = 1,
                              offvalue = 0, command = self.set_click_config, fg = fgColour)
        xsButton.grid(row = 0, column = 5, sticky = W)

        # set up click threshold text entry
        clickThresholdLabel = Label(self.clickConfigFrame, text = 'Threshold (mg):', fg = fgColour, anchor = W)
        clickThresholdLabel.grid(row = 1, column = 0, columnspan = 2)
        clickThresholdText = Entry(self.clickConfigFrame, width=6, fg = fgColour,textvariable = self.click_threshold)
        clickThresholdText.grid(row = 1, column = 2)
        clickThresholdText.bind("<Return>", self.set_click_threshold)
        clickThresholdText.bind("<FocusOut>", self.set_click_threshold)

        # set up click time limit text entry
        clickTimeLimitLabel = Label(self.clickConfigFrame, text = 'Time Limit (ms):', fg = fgColour, anchor = W)
        clickTimeLimitLabel.grid(row = 1, column = 3, columnspan = 2)
        clickTimeLimitText = Entry(self.clickConfigFrame, width=6, fg = fgColour,textvariable = self.click_timelimit)
        clickTimeLimitText.grid(row = 1, column = 5)
        clickTimeLimitText.bind("<Return>", self.set_click_timelimit)
        clickTimeLimitText.bind("<FocusOut>", self.set_click_timelimit)

        # set up click time latency text entry
        clickTimeLatencyLabel = Label(self.clickConfigFrame, text = 'Time Latency (ms):', fg = fgColour, anchor = W)
        clickTimeLatencyLabel.grid(row = 2, column = 0, columnspan = 2)
        clickTimeLatencyText = Entry(self.clickConfigFrame, width=6, fg = fgColour,textvariable = self.click_timelatency)
        clickTimeLatencyText.grid(row = 2, column = 2)
        clickTimeLatencyText.bind("<Return>", self.set_click_timelatency)
        clickTimeLatencyText.bind("<FocusOut>", self.set_click_timelatency)

        # set up click time window text entry
        clickTimeWindowLabel = Label(self.clickConfigFrame, text = 'Time Window (ms):', fg = fgColour, anchor = W)
        clickTimeWindowLabel.grid(row = 2, column = 3, columnspan = 2)
        clickTimeWindowText = Entry(self.clickConfigFrame, width=6, fg = fgColour,textvariable = self.click_timewindow)
        clickTimeWindowText.grid(row = 2, column = 5)
        clickTimeWindowText.bind("<Return>", self.set_click_timewindow)
        clickTimeWindowText.bind("<FocusOut>", self.set_click_timewindow)
        

        # items to still include:             
        # HP filter
        

        # set up main register info display area
        self.regValueFrame = LabelFrame(master, text = 'Register Values', fg = fgColour)
        self.regValueFrame.grid(row = 0, column =1, padx=5, pady=5, sticky = (N,S,W,E))
        self.regValueTextArea = Label(self.regValueFrame, textvariable=self.regValueText, width = 40, anchor = W,
                                      justify = LEFT, fg = fgColour )
        self.regValueTextArea.grid(row = 0, column = 0)

        self.print_reg_values() # update the text screen

        return    

    def print_reg_values(self):

        info = "CTRL_REG1: "+str(hex(self.CTRL_REG1))+" "+str(bin(self.CTRL_REG1))+" "+str(self.CTRL_REG1)+"\n"
        info = info + "CTRL_REG2: "+str(hex(self.CTRL_REG2))+" "+str(bin(self.CTRL_REG2))+" "+str(self.CTRL_REG2)+"\n"
        info = info + "CTRL_REG3: "+str(hex(self.CTRL_REG3))+" "+str(bin(self.CTRL_REG3))+" "+str(self.CTRL_REG3)+"\n"
        info = info + "CTRL_REG4: "+str(hex(self.CTRL_REG4))+" "+str(bin(self.CTRL_REG4))+" "+str(self.CTRL_REG4)+"\n"
        info = info + "CTRL_REG5: "+str(hex(self.CTRL_REG5))+" "+str(bin(self.CTRL_REG5))+" "+str(self.CTRL_REG5)+"\n"
        info = info + "CTRL_REG6: "+str(hex(self.CTRL_REG6))+" "+str(bin(self.CTRL_REG6))+" "+str(self.CTRL_REG6)+"\n\n"
        info = info + "TEMP_CFG_REG: "+str(hex(self.TEMP_CFG_REG))+" "+str(bin(self.TEMP_CFG_REG))+" "+str(self.TEMP_CFG_REG)+"\n"
        info = info + "FIFO_CTRL_REG: "+str(hex(self.FIFO_CTRL_REG))+" "+str(bin(self.FIFO_CTRL_REG))+" "+str(self.FIFO_CTRL_REG)+"\n\n"
        info = info + "INT1_CFG: "+str(hex(self.INT1_CFG))+" "+str(bin(self.INT1_CFG))+" "+str(self.INT1_CFG)+"\n"        
        info = info + "INT1_THS: "+str(hex(self.INT1_THS))+" "+str(bin(self.INT1_THS))+" "+str(self.INT1_THS)+"\n"
        info = info + "INT1_DURATION: "+str(hex(self.INT1_DURATION))+" "+str(bin(self.INT1_DURATION))+" "+str(self.INT1_DURATION)+"\n\n"
        info = info + "CLICK_CFG: "+str(hex(self.CLICK_CFG))+" "+str(bin(self.CLICK_CFG))+" "+str(self.CLICK_CFG)+"\n"        
        info = info + "CLICK_THS: "+str(hex(self.CLICK_THS))+" "+str(bin(self.CLICK_THS))+" "+str(self.CLICK_THS)+"\n"
        info = info + "TIME_LIMIT: "+str(hex(self.TIME_LIMIT))+" "+str(bin(self.TIME_LIMIT))+" "+str(self.TIME_LIMIT)+"\n"
        info = info + "TIME_LATENCY: "+str(hex(self.TIME_LATENCY))+" "+str(bin(self.TIME_LATENCY))+" "+str(self.TIME_LATENCY)+"\n"
        info = info + "TIME_WINDOW: "+str(hex(self.TIME_WINDOW))+" "+str(bin(self.TIME_WINDOW))+" "+str(self.TIME_WINDOW)+"\n"        

        self.regValueText.set(info)

        return

    def axis_enable(self):
        """axis_enable, function to enable/disable the x, y and z axis"""

        xBit = 0b1   # default value - 'on'
        yBit = 0b1   # default value - 'on'
        zBit = 0b1   # default value - 'on'

        CTRL_REG1 = self.CTRL_REG1
        x = self.xAxis.get()
        y = self.yAxis.get()
        z = self.zAxis.get()

        if x == 'off':
            xBit = 0b0

        if y == 'off':
            yBit = 0b0

        if z == 'off':
            zBit = 0b0

        CTRL_REG1 = CTRL_REG1 & 0b11111000
        CTRL_REG1 = CTRL_REG1 | ((zBit<<2) + (yBit<<1) + xBit)
        

        self.CTRL_REG1 = CTRL_REG1
        
        self.print_reg_values() # update the text screen

        return

    def interrupt_high_low(self):
        """interrupt_high_low, function to set the interrupt pins to either
        active high or active low"""

        CTRL_REG6 = self.CTRL_REG6
        level = self.intLevel.get()

        if level == 'low':
            highlowBit = 0b1
        else:
            highlowBit = 0b0

        CTRL_REG6 = CTRL_REG6 & 0b11111101
        CTRL_REG6 = CTRL_REG6 | (highlowBit<<1)        

        self.CTRL_REG6 = CTRL_REG6

        self.print_reg_values() # update the text screen

        return

    def latch_interrupt(self):
        """latch_interrupt, function to turn the latch feature on interrupt1
        on or off"""

        CTRL_REG5 = self.CTRL_REG5

        latch = self.latch.get()

        if latch == 'off':
            latchBit = 0b0
        else:
            latchBit = 0b1

        CTRL_REG5 = CTRL_REG5 & 0b11110111
        CTRL_REG5 = CTRL_REG5 | (latchBit<<3)        

        self.CTRL_REG5 = CTRL_REG5
        
        self.print_reg_values() # update the text screen

        return

    def set_4D(self):
        """set_4D, function to turn 4D detection on or off. This sets
        bit 3 of CTRL_REG5 (0x24)"""

        CTRL_REG5 = self.CTRL_REG5
        enable = self.fourD.get()

        if enable == 'off':
            enableBit = 0b0
        else:
            enableBit = 0b1

        CTRL_REG5 = CTRL_REG5 & 0b11111011
        CTRL_REG5 = CTRL_REG5 | (enableBit<<2)        

        self.CTRL_REG5 = CTRL_REG5

        self.print_reg_values() # update the text screen

        return

    def set_adc(self):
        """set_adc, function to enable/disable the aux 10 bit adc
        converter feature.  This sets bit 7 of TEMP_CFG_REG (0x1F)"""

        TEMP_CFG_REG = self.TEMP_CFG_REG
        adcOn = self.adc.get()

        adcBit = 0b0  # default value

        if adcOn == 'on':
            adcBit = 0b1

        TEMP_CFG_REG = TEMP_CFG_REG & 0b01111111
        TEMP_CFG_REG = TEMP_CFG_REG | (adcBit<<7)        

        self.TEMP_CFG_REG = TEMP_CFG_REG

        self.print_reg_values() # update the text screen

        return    

    def set_BDU(self):
        """set_BDU, function to enable/disable the block data update
        feature.  This sets bit 7 of CTRL_REG4 (0x23)"""

        CTRL_REG4 = self.CTRL_REG4
        bdu = self.bdu.get()

        bduBit = 0b0  # default value

        if bdu == 'on':
            bduBit = 0b1

        CTRL_REG4 = CTRL_REG4 & 0b01111111
        CTRL_REG4 = CTRL_REG4 | (bduBit<<7)        

        self.CTRL_REG4 = CTRL_REG4

        self.print_reg_values() # update the text screen

        return

    def set_click_config(self):
        """set_click_config, function to set the CLICK_CFG regisiter
        (0x38) options"""

        zd = self.click_zd.get()
        zs = self.click_zs.get()
        yd = self.click_yd.get()
        ys = self.click_ys.get()
        xd = self.click_xd.get()
        xs = self.click_xs.get()

        CLICK_CFG = ((zd<<5) + (zs<<4) +(yd<<3) + (ys<<2) + (xd<<1)
                     + xs)        

        self.CLICK_CFG = CLICK_CFG
        self.print_reg_values() # update the text screen

        return

    def set_click_threshold(self, event):
        """set_click_threshold, function to set the click threshold (mg).
        This sets CLICK_THS (0x3A)"""        

        try:
            threshold = abs(self.click_threshold.get())
            scale = self.scale.get()
            thresholdBits = 0b0      

            if scale == 2:
                scaleOffset = 4
            elif scale == 4:
                scaleOffset = 5
            elif scale == 8:
                scaleOffset = 6
            else: # scale == 16
                scaleOffset = 7

            for i in range (6,-1,-1):

                if threshold >= 2**(i+scaleOffset):
                    thresholdBits = thresholdBits | (1<<i)
                    threshold = threshold - 2**(i+scaleOffset)

        except ValueError:
            self.click_threshold.set(0)
            thresholdBits = 0x00
        except:
            self.click_threshold.set(0)
            thresholdBits = 0x00

        

        self.CLICK_THS = thresholdBits
        
        self.print_reg_values() # update the text screen

        return

    def set_click_timelimit(self, event):
        """set_click_timelimit, function to set the click time limit
        duration (ms). This sets TIME_LIMIT (0x3B)"""

        try:
            duration = abs(self.click_timelimit.get())
            odr = self.odr.get()
            
            if duration > (float(127000)/float(odr)):
                durationBits = 0b01111111

            else:
                durationBits = int((float(duration) / float(1000)) * odr)
                durationBits = durationBits & 0b01111111

        except ValueError:
            self.click_timelimit.set(0)
            durationBits = 0x00
        except:
            self.click_timelimit.set(0)
            durationBits = 0x00

        self.TIME_LIMIT = durationBits

        self.print_reg_values() # update the text screen

        return

    def set_click_timelatency(self, event):
        """set_click_timelatency, function to set the click time latency
        duration (ms). This sets TIME_LATENCY (0x3C)"""

        try:
            duration = abs(self.click_timelatency.get())
            odr = self.odr.get()
            
            if duration > (float(255000)/float(odr)):
                durationBits = 0b11111111

            else:
                durationBits = int((float(duration) / float(1000)) * odr)
                durationBits = durationBits & 0b11111111

        except ValueError:
            self.click_timelatency.set(0)
            durationBits = 0x00
        except:
            self.click_timelatency.set(0)
            durationBits = 0x00

        self.TIME_LATENCY = durationBits

        self.print_reg_values() # update the text screen

        return

    def set_click_timewindow(self, event):
        """set_click_timewindow, function to set the click time window
        duration (ms). This sets TIME_WINDOW (0x3D)"""

        try:
            duration = abs(self.click_timewindow.get())
            odr = self.odr.get()
            
            if duration > (float(255000)/float(odr)):
                durationBits = 0b11111111

            else:
                durationBits = int((float(duration) / float(1000)) * odr)
                durationBits = durationBits & 0b11111111

        except ValueError:
            self.click_timewindow.set(0)
            durationBits = 0x00
        except:
            self.click_timewindow.set(0)
            durationBits = 0x00

        self.TIME_WINDOW = durationBits

        self.print_reg_values() # update the text screen

        return

    def set_endian(self):
        """set_endian, function to set the endian option to big 
        or little.  This sets bit 6 of CTRL_REG4 (0x23)"""

        CTRL_REG4 = self.CTRL_REG4
        endian = self.endian.get()

        endianBit = 0b0  # default value

        if endian == 'big':
            endianBit = 0b1

        CTRL_REG4 = CTRL_REG4 & 0b10111111
        CTRL_REG4 = CTRL_REG4 | (endianBit<<6)        

        self.CTRL_REG4 = CTRL_REG4

        self.print_reg_values() # update the text screen

        return

    def set_fifo_mode(self):
        """set_fifo_mode, function to set the fifo mode of the accelerometer,
        valid value for mode are; off, bypass, fifo, stream and streamfifo.
        This sets bit 6 of CTRL_REG5 (0x24) and bits 6 & 7 of FIFO_CTRL_REG
        (0x2E)"""

        CTRL_REG5 = self.CTRL_REG5
        FIFO_CTRL_REG = self.FIFO_CTRL_REG

        fifoEnable = self.fifoEnable.get()
        mode = self.fifoMode.get()               

        enableBit = 0b0 # default value: disable
        modeBits = 0b00 # default value: bypass

        if fifoEnable == 'on':
            enableBit = 0b1
        
        if mode == 'fifo':
            modeBits = 0b01
        elif mode == 'stream':
            modeBits = 0b10
        elif mode == 'streamfifo':
            modeBits = 0b11 

        CTRL_REG5 = CTRL_REG5 & 0b10111111
        CTRL_REG5 = CTRL_REG5 | (enableBit<<6)
        self.CTRL_REG5 = CTRL_REG5

        FIFO_CTRL_REG = FIFO_CTRL_REG & 0b00111111
        FIFO_CTRL_REG = FIFO_CTRL_REG | (modeBits<<6)
        self.FIFO_CTRL_REG = FIFO_CTRL_REG

        self.print_reg_values() # update the text screen
        
        return

    def set_fifo_threshold(self, event):
        """set_fifo_threshold, function to the fifo threshold level.
        This sets bits 0-4 of FIFO_CTRL_REG (0x2E)"""

        FIFO_CTRL_REG = self.FIFO_CTRL_REG

        try:
            threshold = int(abs(self.fifoThreshold.get()))

            if threshold > 31:
                threshold = 31

        except ValueError:
            threshold = 0
            self.fifoThreshold.set(0)
        except:
            threshold = 0
            self.fifoThreshold.set(0)

        FIFO_CTRL_REG = FIFO_CTRL_REG & 0b11100000
        FIFO_CTRL_REG = FIFO_CTRL_REG | threshold
        self.FIFO_CTRL_REG = FIFO_CTRL_REG

        self.print_reg_values() # update the text screen        

        return

    def set_highpass_filter(self, event = None):
        """set_highpass_filter, function to set the various high pass filter
        options.  This sets CTRL_REG2 (0x21)

        mode - normal, reference, normalreset, autoreset
        freq - see table 8 of the LIS3DH app note
        FDS (filtered data selection) bypass - on or off """

        mode = self.hpfMode.get()        
        FDS = self.hpfFDS.get()
        hpClick = self.hpfClick.get()
        hpIS2 = self.hpfIS2.get()
        hpIS1 = self.hpfIS1.get()

        fdsBit = 0b0  # default value
        hpClickBit = 0b0  # default value
        hpIS2Bit = 0b0  # default value
        hpIS1Bit = 0b0  # default value

        if mode == 'normalreset':
            modeBits = 0b0
        elif mode == 'reference':
            modeBits = 0b1
        elif mode == 'autoreset':
            modeBits = 0b11
        else: # mode = 'normal'
            modeBits = 0b10

        try:
            freq = int(abs(self.hpfCutOff.get()))           

        except ValueError:
            freq = 0
            self.hpfCutOff.set(0)
        except:
            freq = 0
            self.hpfCutOff.set(0)        

        if freq > 0b11:
            freqBits = 0b11
        else:
            freqBits = freq

        if FDS == 'on':
            fdsBit = 0b1

        if hpClick == 'on':
            hpClickBit = 0b1

        if hpIS2 == 'on':
            hpIS2Bit = 0b1

        if hpIS1 == 'on':
            hpIS1Bit = 0b1

        CTRL_REG2 = ((modeBits<<6) + (freqBits<<4) + (fdsBit<<3) + (hpClickBit<<2)
                     + (hpIS2Bit<<1) +hpIS1Bit)
        

        self.CTRL_REG2 = CTRL_REG2

        self.print_reg_values() # update the text screen 

        return

    def set_int1_config(self):
        """set_int1_config, function to set the INT1_CFG regisiter (0x30) options"""

        aoi = self.int1_aoi.get()
        d6 = self.int1_d6.get()
        zh = self.int1_zh.get()
        zl = self.int1_zl.get()
        yh = self.int1_yh.get()
        yl = self.int1_yl.get()
        xh = self.int1_xh.get()
        xl = self.int1_xl.get()        

        INT1_CFG = ((aoi<<7) + (d6<<6) + (zh<<5) + (zl<<4) +(yh<<3) +
                (yl<<2) + (xh<<1) + xl)       

        self.INT1_CFG = INT1_CFG
        self.print_reg_values() # update the text screen

        return

    def set_int1_duration(self, event):
        """set_int1_duration, function to set the minimum interrupt 1 duration (ms).
        This sets INT1_DURATION(0x33)"""        

        try:
            duration = abs(self.int1_duration.get())
            odr = self.odr.get()
            
            if duration > (float(127000)/float(odr)):
                durationBits = 0b01111111

            else:
                durationBits = int((float(duration) / float(1000)) * odr)
                durationBits = durationBits & 0b01111111

        except ValueError:
            self.int1_duration.set(0)
            durationBits = 0x00
        except:
            self.int1_duration.set(0)
            durationBits = 0x00

        self.INT1_DURATION = durationBits

        self.print_reg_values() # update the text screen

        return

    def set_int1_pin(self):
        """set_int1, function to which interrupt signals get pushed to
        the int1 pin. This sets CTRL_REG3 (0x22)"""        

        click = self.int1_click.get()
        aoi1 = self.int1_aoi1.get()
        aoi2 = self.int1_aoi2.get()
        drdy1 = self.int1_drdy1.get()
        drdy2 = self.int1_drdy2.get()
        wtm = self.int1_wtm.get()
        overrun = self.int1_overrun.get()

        CTRL_REG3 = ((click<<7) + (aoi1<<6) + (aoi2<<5) + (drdy1<<4) +(drdy2<<3) +
                (wtm<<2) + (overrun<<1))        

        self.CTRL_REG3 = CTRL_REG3
        self.print_reg_values() # update the text screen

        return

    def set_int1_threshold(self, event):
        """set_int1_threshold, function to set the interrupt1 threshold (mg).
        This sets INT1_THS (0x32)"""

        try:
            threshold = abs(self.int1_threshold.get())
            scale = self.scale.get()
            thresholdBits = 0b0      

            if scale == 2:
                scaleOffset = 4
            elif scale == 4:
                scaleOffset = 5
            elif scale == 8:
                scaleOffset = 6
            else: # scale == 16
                scaleOffset = 7

            for i in range (6,-1,-1):

                if threshold >= 2**(i+scaleOffset):
                    thresholdBits = thresholdBits | (1<<i)
                    threshold = threshold - 2**(i+scaleOffset)

        except ValueError:
            self.int1_threshold.set(0)
            thresholdBits = 0x00
        except:
            self.int1_threshold.set(0)
            thresholdBits = 0x00

        

        self.INT1_THS = thresholdBits
        
        self.print_reg_values() # update the text screen

        return

    def set_ODR(self):
        """set_ODR, function to set the output data rate (ODR) and the power
        mode (normal, low, or off). This sets bits 3-7 of CTRL_REG1 (0x20)"""

        CTRL_REG1 = self.CTRL_REG1

        powerMode = self.powerMode.get()
        odr = self.odr.get()        
        
        lowPowerBit = 0b0 # default value 'normal' power mode        

        odrOptions = [(1,0b0001),(10,0b0010),(25,0b0011),(50,0b0100),
                      (100,0b0101),(200,0b0110),(400,0b0111),(1600,0b1000),
                      (1250,0b1001),(5000,0b1001)]

        for dataRate in odrOptions:
            if dataRate[0] == odr:
                odrBits = dataRate[1]                

        if powerMode == 'Off':
            odrBits = 0b0000

        elif powerMode == 'Low':
            lowPowerBit = 0b1
            

        CTRL_REG1 = CTRL_REG1 & 0b00000111
        CTRL_REG1 = CTRL_REG1 | ((odrBits<<4) + (lowPowerBit<<3))        

        self.CTRL_REG1 = CTRL_REG1

        self.set_int1_duration(event = None)    # update INT1_DURATION as it is dependent on ODR
        self.set_click_timelimit(event = None)  # update TIME_LIMIT as it is dependent on ODR
        self.set_click_timelatency(event = None)  # update TIME_LATENCY as it is dependent on ODR
        self.set_click_timewindow(event = None)  # update TIME_WINDOW as it is dependent on ODR

        self.print_reg_values() # update the text screen

        return

    def set_resolution(self):
        """set_resolution, function to set the accelerometer resolution
        to either high or low.  This sets bit 3 of CTRL_REG4 (0x23)"""

        CTRL_REG4 = self.CTRL_REG4
        res = self.resolution.get()

        resBit = 0b0  # default value: low

        if res == 'high':
            resBit = 0b1

        CTRL_REG4 = CTRL_REG4 & 0b11110111
        CTRL_REG4 = CTRL_REG4 | (resBit<<3)

        self.CTRL_REG4 = CTRL_REG4

        self.print_reg_values() # update the text screen

        return

    def set_scale(self):
        """set_scale, function to set the scale used by the
        accelerometer; +-2g, 4g, 8g, 16g"""

        CTRL_REG4 = self.CTRL_REG4         
        scale = self.scale.get()

        if scale == 2:
            scaleBits = 0b00
        elif scale == 4:
            scaleBits = 0b01            
        elif scale == 8:
            scaleBits = 0b10            
        else: ## scale == 16
            scaleBits = 0b11       

        CTRL_REG4 = CTRL_REG4 & 0b11001111
        CTRL_REG4 = CTRL_REG4 | (scaleBits<<4)        

        self.CTRL_REG4 = CTRL_REG4

        self.set_int1_threshold(event = None)  # update INT1_THS as it is dependent on scale
        self.set_click_threshold(event = None) # update CLICK_THS as it is dependent on scale

        self.print_reg_values() # update the text screen

        return

    def set_temperature(self):
        """set_temperature, function to enable/disable the on board temperature
        sensor. This sets bit 6 of TEMP_CFG_REG (0x1F)"""

        TEMP_CFG_REG = self.TEMP_CFG_REG        
        temperature = self.temperature.get()

        tempBit = 0b0  # default value

        if temperature == 'on':
            tempBit = 0b1

        TEMP_CFG_REG = TEMP_CFG_REG & 0b10111111
        TEMP_CFG_REG = TEMP_CFG_REG | (tempBit<<6)        

        self.TEMP_CFG_REG = TEMP_CFG_REG

        self.print_reg_values() # update the text screen

        return


    






root = Tk()
root.title("LIS3DH Configuration Tool - v1.0 121518")
configTool = LIS3DHConfigGui(root)
root.mainloop()

# program clean up statements
print('Program Halt')
