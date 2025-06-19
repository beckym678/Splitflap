#Code from:
#  https://peppe8o.com/stepper-motor-with-raspberry-pi-pico-28byj-48-and-uln2003-wiring-and-micropython-code/
from machine import Pin
from time import sleep

#IN1, IN2, IN3, and IN4. are attached in order to pico pins GP0, GP1, GP2, and GP3:
#motor_GP = [0,1,2,3]
motor_GP = [12,13,14,15]

seq_pointer=[0,1,2,3,4,5,6,7]
stepper_obj = []


#The 7 possible commands to send to the motor (step 8 is 0000 and does nothing)
arrSeq = [[0,0,0,1],\
          [0,0,1,1],\
          [0,0,1,0],\
          [0,1,1,0],\
          [0,1,0,0],\
          [1,1,0,0],\
          [1,0,0,0],\
          [1,0,0,1]]

#Pin setup:
print("Setup.ff pins...")
for gp in motor_GP: stepper_obj.append(Pin(gp, Pin.OUT))

#Rotates the motor 1 step
def stepper_move(direction):  # direction must be +1 or -1
    global seq_pointer
    seq_pointer=seq_pointer[direction:]+seq_pointer[:direction]
    for a in range(4):
        print("Sending command:", arrSeq[seq_pointer[0]][a])
        stepper_obj[a].value(arrSeq[seq_pointer[0]][a])
    sleep(0.001)

    
#moves motor in direction 1  
while True:
    stepper_move(1)

"""
#moves motor in direction -1.
while True:
    stepper_move(-1) """

