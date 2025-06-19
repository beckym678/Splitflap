"""
MicroPython 74HC595 8-Bit Shift Register daisy chain stepper motor controller

Sends commands for up to 6 stepper motors through a chain of 3 8-bit shift registers.

MIT License
Copyright (c) 2025 Becky Moyer

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from machine import Pin
import utime
import random
from time import sleep

dataPIN = 17   #ShiftReg Pin 11 (RPi CSn)
latchPIN = 16  #Gos to ShiftReg Pin 12
clockPIN = 18  #ShiftReg CLK Pin ( maybe 14?)(RPi SCLK)

dataPinout=Pin(dataPIN, Pin.OUT)
latchPinout=Pin(latchPIN, Pin.OUT)
clockPinout=Pin(clockPIN, Pin.OUT)

SHIFT_LENGTH=7  #How many bits of data get sent to the shift register (count starts at 0, so 7 = 8 bits)


motorLineup = 1 #if motor order is 1-6, this is 1.  If motor order is 6-1, this is -1

motorSequenceNibbles = ["0001", "0011", "0010", "0110", "0100", "1100", "1000", "1001"]

motorStepWord = "00010011001001100100110010001001"
zeroWord = "00000000000000000000000000000000"


class motorController:
    def __init__(self, dataPIN=17, latchPIN=16, clockPIN=18, motorLineup=1):    
        self.dataPIN = dataPIN
        self.latchPIN = latchPIN
        self.clockPIN = clockPIN
        self.motorLineup = motorLineup #if motor order is 1-6, this is 1.  If motor order is 6-1, this is -1

        #NOTE: I do not think it really matters how many motors they want to control...
        #             ...I just go by the distance array length.
        #self.SHIFT_LENGTH = 4*numMotors-1


    #Input distances is an array of ints
    def moveFlaps(self, distances):        
        outputword = ""
        mostStepsRequested = max(distances)
        numMotors = len(distances)
        #loop however many times the longest motor command needs to be.
        for steps in range(mostStepsRequested):
            #for each motor
            print("calculating step #", steps)
            for motorNum in range(numMotors):
                print("motor# ", motorNum,"]=", distances[motorNum])
                if (distances[motorNum] > steps):
                    outputword += motorStepWord
                else:
                    outputword += zeroWord
                
            self.shift_update(outputword)
            utime.sleep(0.001)

           
    #INTERNAL METHOD - do not call from outside this class.
    #Sends data to the shift register.  data, clock. and latch are the defined pins.
    def __shift_update(input,data,clock,latch):
        #put latch down to start data sending
        clockPinout.value(0)
        latchPinout.value(0)
        clockPinout.value(1)
        #load data in reverse order
        for i in range(self.SHIFT_LENGTH, -1, -1):
            clock.value(0)
            data.value(int(input[i]))
            print("Using value ", input[i], " for output # ", i)
            clock.value(1)
        print(" --- ")
        #put latch up to store data on register
        clock.value(0)
        latch.value(1)
        clock.value(1)
        return    









