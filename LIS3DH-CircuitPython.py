# LIS3DH-CircuitPython, program to practice using
# a Circuit Python with the LIS3DH accelerometer.

# The LIS3DH will be set up for a simple interrupt - AND. 
# These settings will produce an interrupt when both the
# x-axis and y-axis go above the 256mg threshold.

# A Trinket M0 connected to an Adafruit LIS3DH breakout
# board was used.

# Tested with Circuit Python 3

# note Trinket M0 does not have internal pullups
# on the i2c lines, needed if not using an adafruit 
# breakout board 

# Trinket Pin 0 - LIS3DH SDA
# Trinket Pin 2 - LIS3DH SCL
# 3.3V - LIS3DH SD0
# 3.3V - LIS3DH CS
# Connect LED & resistor to LIS3DH Int to see when the interrupt occurs
# Interrupt is set to Active High

# created Dec 15, 2019
# modified Dec 16, 2019

import board
import busio
import time
from adafruit_bus_device.i2c_device import I2CDevice

i2c = busio.I2C(board.SCL, board.SDA)
device = I2CDevice(i2c, 0x19)

def single_access_read(regAddr):
    
    with device as bus_device:
        bus_device.write(bytes([regAddr]))
        result = bytearray(1)
        bus_device.readinto(result)
        
    return result[0]
    
def single_access_write(regAddr, regValue):
    
    with device as bus_device:
        bus_device.write(bytes([regAddr, regValue]), stop = True)
        
    return
    
def multiple_access_write(regAddr, regValues):
    
    cmdBit = 0b1  #indicates  multiple reads of consecutive registers
    #cmdBit = 0b0  #indicates  multiple reads of the same register - default behavior
    
    regAddr = (cmdBit<<7) + regAddr
    
    value2write = []
    value2write.append(regAddr)
    for value in regValues:
        value2write.append(value)        
    
    with device as bus_device:        
        bus_device.write(bytes(value2write), stop = True)
        
    return
    
def number_conversion(lsb, msb):
    """number_conversion, function to convert the 10 bit
    2 complement left justified number to a normal number"""
    
    signBit = (msb & 0b10000000)>>7
    msb = msb & 0x7F  # strip off sign bit
    
    if signBit == 1:
        # negative number
        x = (msb<<8)+ lsb
        x = x^0x7FFF
        x = -(x+1)
    else:
        # positive number
        x = (msb<<8)+ lsb
    
    x = x>>6  # remove left justification of data
    
    return x
    
def simple_interrupt_and():
    """simple_interrupt, function to set the LIS3DH registers
    for simple interrupt operation - AND - x & y-axis"""
    
    CTRL_REG1 = 0x47
    CTRL_REG2 = 0x00
    CTRL_REG3 = 0x40    # AOI1 interrupt
    CTRL_REG4 = 0x00    # no BDU, +/- 2g
    CTRL_REG5 = 0x00
    CTRL_REG6 = 0x00
    
    INT1_CFG = 0x8A     # AOI1, YH, XH
    INT1_THS = 0x10     # 256 mg
    INT1_DURATION = 0x00 # 0 ms
    
    CLICK_CFG = 0x00    # 
    CLICK_THS = 0x00    # 0 mg
    TIME_LIMIT = 0x00   # 0 ms
    TIME_LATENCY = 0x00 # 0 ms
    TIME_WINDOW = 0x00  # 0 ms
    
    # write Control register values starting at CTRL_REG1 address - 0x20    
    multiple_access_write(0x20, [CTRL_REG1,CTRL_REG2,CTRL_REG3,CTRL_REG4, CTRL_REG5, CTRL_REG6])    
    
    # write INT1_CFG value to INT1_CFG register at address - 0x30
    single_access_write(0x30, INT1_CFG)
    
    # write Interrupt threshold and duration values starting at INT1_THS address - 0x32
    multiple_access_write(0x32, [INT1_THS, INT1_DURATION])
    
    # write CLICK_CFG value to CLICK_CFG register at address - 0x38
    single_access_write(0x38, CLICK_CFG)
    
    # write Click threshold and time register values starting at CLICK_THS address - 0x3A
    multiple_access_write(0x3A, [CLICK_THS, TIME_LIMIT, TIME_LATENCY, TIME_WINDOW])
    
    return

# LIS3DH Set up code    
print("Starting")
simple_interrupt_and()
print(single_access_read(0x0F)) # print whoami register - should print 51 (0x33)
print(single_access_read(0x20)) # print CTRL_REG1 - should print 71 (0x47)
print("Done Setting up LIS3DH")

# Code to do something with output from LIS3DH
# Below just prints out the Interrupt Status register (0x31) 
# if both the x and y axis go above the set threshold

while True:
    interruptStatus = single_access_read(0x31) # get interrupt status register
    if interruptStatus & 0x40 != 0:
        print("Interrupt Register " + str(bin(interruptStatus)))
    
    # print off x-axis acceleration values
    xH = single_access_read(0x29)
    xL = single_access_read(0x28)
    
    print(number_conversion(xL, xH))
    time.sleep(1)
    
    