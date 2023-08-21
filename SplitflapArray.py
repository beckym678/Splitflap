"""
This file contains types Splitflap and Splitflap Array.

SPLITFLAP ARRAY:
   This is a virtual object that contains 1 to X splitflaps.  It sends commands to the
   shift registers to rotate all motors simeultaneously.
   
   to initialize, it needs to be given all the connected splitflap objects.
   
   It needs the following functions:
   
       find_home (?)
       changeFunction (changes what the current action the splitflap display is doing)
       displayWord
       displayTime  (Continuously displays the current time, until some type of interrupt is pressed)
       displayWords (multiple phrases one after another - input is multiple (x or less) letter words)
       displayDate  (shows current month in 3 letter code, plus 2 digits of day of month.  Only workds
                       with an array of 5 or more splitflaps)
   
SPLITFLAP:
   A physical splitflap device has a spool of 40 flaps, a stepper motor (4 bit input),
   a Hall Sensor (1 output), and possibly will have an LED available in the future.
   The motor and LED will be accessed via a shift register.  This code will need to send
   the commands to the motor via the shift register.  Therefore, to initialize the splitflap
   object, it will need to be initialized with:
   1) its hall sensor pin
   2) its order
   3) any offset the flaps have from standard setup (e.g. how far extra it takes to get to each flap.)
   
   Other than init, it will need to have the following information/function:
   
    functions:
        find_home
        status of some sort
        displayLetter
        
        
        
        

The big challenge: in order for the motors to spin simeultaneously, I'll need to interact with all of them at each change.
Another option: figure out the ENTIRE list of commands to send to each motor, then bundle it into one giant send.

For example, ask each individual splitflap to move to the correct letter, then have it return the bit sequence needed.
Once you get those return bit sequences, concat them into the right format for display and send them all at once.

"""
from machine import Pin,ADC
import machine
import utime
from time import sleep



seq_pointer=[0,1,2,3,4,5,6,7]
stepper_obj = []


#The 8 possible commands to send to the motor 
arrSeq = ['0001',\
          '0011',\
          '0010',\
          '0110',\
          '0100',\
          '1100',\
          '1000',\
          '1001']

class Splitflap:
    def __init__(self, hall_pin, motor_offset=0):  #Note - to control these individually, you'd need to spec a data_pin.
        
        global DIN
        DIN = Pin(hall_pin,Pin.IN)

        #Note - this is the offset needed for steps on a specific splitflap module to have letters match up.  Assumed at no offset.
        global offset
        offset = motor_offset 
        

#    def displayChar(character):
        #This will determine the correct amount of motor rotation to display the input character
        #It will return an array of nibbles? bytes? to send to the shift registers.
        
    """def findHome():
        #read the hall sensor to check on if we found home
        if hall==0:
            self.atHome = True
            
        if self.atHome:
            return 00000000
        elif:
            #return the next part of the motor rotation sequence"""
        
"""
****************************
"""

atHome = False
hallPins = []


class SplitflapArray:
    def _init_(self, *displayDevices, dataPINnum = 5, clockPINnum=14, latchPINnum = 15):  #Hopefullt this means that to create a splitflap array object I need to input an array of splitflaps.
        #I'm pretty sure I have the syntax wrong.
        #determines the pico pin that the shift registers are attached to.

        
        global devices
        devices = displayDevices
        
        global hallPins
        hallPins = self.getHallPins()
        

        global dataPIN
        global latchPIN
        global clockPIN
        
        dataPIN=Pin(dataPINnum, Pin.OUT)
        latchPIN=Pin(latchPINnum, Pin.OUT)
        clockPIN=Pin(clockPINnum, Pin.OUT)
        


        
    def getHallPins(self):
        #Returns an array of pins to check hall sensors for.  First letter is array item 0.
        
        for a in range(len(self.devices)):
            hallPinStorage[a] = self.devices[a].DIN
        return hallPinStorage
        
            
  
    def findHome(self):
        #function tells each motor to move UNTIL its hall pin is (de)activted.
        #pointer tells me which motor movement command I'm currently on.
        pointer = 0
        
        while not(self.hallPins.all() == 0):
            command = ""
        
            #cycle through each display to see if it still needs to move, and make a string
            #of commands to send.
            for m in range(len(self.devices)):
                #If the current device is "at home", tell it to stay put.
                if hallPin[m] == 0:
                    command = command + "0000"
                #otherwise, send the next movement command.
                else:
                    command = command + arrSeq[pointer]
                command += "0000" #Fill in the unused 4 bits that we need to fill each shift register
                
                
            #send the commands to the shift register pin
            self.shiftCommand(command)
            #increment to the next movement command.  This is simplistic
            #because I'm only ever rotating one direction for this application.
            #Hopefully I chose the right way!
            if pointer == 7:
                pointer = 0
            else:
                pointer += 1
        print("Found home for all motors")
    
    def shiftCommand(self, input):
      #put latch down to start data sending
      clockPIN.value(0)
      latchPIN.value(0)
      clockPIN.value(1)
  
      #load data in reverse order  (DO I NEED THIS IN REVERSE HERE??)
      for i in range(SHIFT_LENGTH, -1, -1):
        clockPIN.value(0)
        dataPIN.value(int(input[i]))
        #print("Using value ", input[i], " for output # ", i)
        clockPIN.value(1)
      #print(" --- ")
      
      #put latch up to store data on register
      clockPIN.value(0)
      latchPIN.value(1)
      clockPIN.value(1)
