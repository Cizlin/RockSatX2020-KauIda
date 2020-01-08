# The following code has been modified from that provided at github.com/piborg/diablo
# by Garrisen Cizmich

#!/usr/bin/env python

###
#
# diabloSequence.py: A script for controlling motors with the Diablo in a sequence.
#
# 2019-04-26
#
###
# Import library functions we need
from __future__ import print_function
from diablo import *
from time import sleep
from sys import exit
import RPi.GPIO as GPIO # Fetch the GPIO library and initialize the object.
GPIO.setmode(GPIO.BCM)

# Set up pins 9 and 10 for input.
GPIO.setup(24, GPIO.IN) 
GPIO.setup(23, GPIO.IN)

# Set up the Diablo
DIABLO = Diablo()        # Create a new Diablo object
DIABLO.Init()                       # Set the board up (checks the board is connected)
if not DIABLO.foundChip:
    boards = ScanForDiablo()
    if len(boards) == 0:
        print('No Diablo found, check you are attached :)')
    else:
        print('No Diablo at address %02X, but we did find boards:' % (DIABLO.i2cAddress))
        for board in boards:
            print('    %02X (%d)' % (board, board))
        print('If you need to change the I2C address change the set-up line so it is correct, e.g.')
        print('DIABLO.i2cAddress = 0x%02X' % (boards[0]))
    exit()
#DIABLO.SetEpoIgnore(True)          # Uncomment to disable EPO latch, needed if you do not have a switch / jumper
DIABLO.ResetEpo()                   # Reset the stop switch (EPO) state
                                    # if you do not have a switch across the two pin header then fit the jumper

# Loop over the sequence until the user presses CTRL+C
print ('Press CTRL+C to cancel manual motor control.')
try:
    while True:
        if (not(GPIO.input(23))):
            DIABLO.SetMotor1(0.0) # If the motor on/off switch is set to off, do not operate the motor.
        else:
            if (GPIO.input(24)):
                DIABLO.SetMotor1(+1.0) # Set the motor to go "forward" if switch is on.
            else:
                DIABLO.SetMotor1(-1.0) # Set the motor to go "backward" if switch is off.
except KeyboardInterrupt:
    # User has pressed CTRL+C
    DIABLO.MotorsOff()              # Turn both motors off
    print ('Done')
