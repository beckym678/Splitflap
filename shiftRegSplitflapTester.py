from machine import Pin,ADC
import machine
import utime
from time import sleep


from SplitflapArray import Splitflap  #, SplitflapArray






splitflaps = []

splitflap = Splitflap(10)
#splitflaps[1] = Splitflap(13)
#splitflaps[2] = Splitflap(14)




#display = SplitflapArray(splitflaps)

print("Splitflap Array initialized")

splitflap.findHome()

print("End of program")


