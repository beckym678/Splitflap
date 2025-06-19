from machine import Pin,ADC
import utime
from time import sleep

#Select ADC input 0 (GPIO26)
ADC_ConvertedValue = machine.ADC(0)
DIN = Pin(15,Pin.IN)
conversion_factor = 3.3 / (65535)
offset = 2
#This is correct for display #1.  Others may need some type of adjustment to this.
letter_places = [306, 408, 510, 612, 714, 816, 918, #ABCDEFG 
                 1020, 1122, 1224, 1326, 1428, 1530, 1632, 1734, 1836, #HIJKLMNOP
                 1938, 2040, 2142, 2244, 2346, 2448, #QRSTUV
                 2560, 2662, 2764, 2866, #WXYZ
                 2968, 3070, 3172, 3274, 3376,  #12345
                 3478, 3580, 3682,3784, 3886,#67890
                 3988, 4096, 102, 204] #blank blank blank home

flap_name = ['A', 'B', 'C', 'D', 'E', 'F', 'G',\
             'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', \
             'Q', 'R', 'S', 'T', 'U', 'V',\
             'W', 'X', 'Y', 'Z',\
             '1', '2', '3', '4', '5',\
             '6', '7', '8', '9', '0',\
             'b', 'b', 'b', 'h']


#Code from:
#  https://peppe8o.com/stepper-motor-with-raspberry-pi-pico-28byj-48-and-uln2003-wiring-and-micropython-code/

#IN1, IN2, IN3, and IN4. are attached in order to pico pins GP0, GP1, GP2, and GP3:
motor_GP = [0,1,2,3]

seq_pointer=[0,1,2,3,4,5,6,7]
stepper_obj = []


#The 7 possible commands to send to the motor (step 8 is 0000 and does nothing?)
arrSeq = [[0,0,0,1],\
          [0,0,1,1],\
          [0,0,1,0],\
          [0,1,1,0],\
          [0,1,0,0],\
          [1,1,0,0],\
          [1,0,0,0],\
          [1,0,0,1]]

print("Setup pins...")
for gp in motor_GP: stepper_obj.append(Pin(gp, Pin.OUT))



#Rotates the motor 1 step
def stepper_move(direction):  # direction must be +1 or -1
    global seq_pointer
    seq_pointer=seq_pointer[direction:]+seq_pointer[:direction]
    for a in range(4): stepper_obj[a].value(arrSeq[seq_pointer[0]][a])
    sleep(0.001)


def find_home():
    while (DIN.value() ==0):
        stepper_move(1)
        utime.sleep(0.001)
    while (DIN.value() == 1) :
        stepper_move(1)
        utime.sleep(0.001)
    print("found magnet")
    return 0

def advance_one_flap(current_position):
    return select_letter(flap_name[letter_places.index(current_position)+1], current_position)

def flip_one_flap():
    for a in range(102):
        stepper_move(1)
    print("moved one flap")


    
def flip_x_flaps(x):
    #There are 4096 rotations for this motor. 4096 / 40 flaps = 102.4 per flap

    k = round(102.4*(x))
    print("rotations = ", k)
    for a in range(k):
        stepper_move(1)
    
    print("moved", x,  "flaps")
    
def rotate_by_step(steps):
    for a in range(steps):
        stepper_move(1)
    
def select_letter(c, current_position):
    location = letter_places[flap_name.index(c)-offset]
    steps_to_move = 0
    #print("Current position = ", current_position)
    if (current_position<location):
        steps_to_move = location - current_position
        #print("Moving to location ", location, " in ", steps_to_move, " steps.")
    elif (current_position > location):
        steps_to_move =  4096 - current_position + location
        #print("Moving to location ", location, " in ", steps_to_move, " steps.")
    elif (current_position == location):
        steps_to_move = 4096
        #print("Moving to location ", location, " in ", steps_to_move, " steps.")

    
    print("Moving to location: ", location)
    rotate_by_step(steps_to_move);
    current_position = location
    return location
    
def show_word(word, current_position):
    for a in range(len(word)):
        current_position = select_letter(word[a], current_position)
        utime.sleep(1.5)
    return current_position

print("Find home...")
current_position = -1
if (current_position!=0):
    current_position = find_home()

print("Found Home - sleeping")
utime.sleep(0.5)

current_position = show_word('ATE', current_position)
#current_position = advance_one_flap(current_position)
#utime.sleep(2)

#current_position = show_word('ABCDEFG', current_position)

