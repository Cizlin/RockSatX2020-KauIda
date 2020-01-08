# The following code has been modified from that provided at github.com/piborg/diablo
# by Garrisen Cizmich

# To run this program (or any other program with I2C control), you must perform the following:
# Open Terminal.
# Type "ps aux | grep ManualMotorControl.py" without the quotes and press Enter.
# Find the process owned by root with "sudo" in the command to the right. Note its PID (number in the second column).
# Type "sudo kill -TERM [pid]" without the quotes, replacing [pid] with the PID found above. Press Enter.
# You can now start this program.

# Runs through a simulation of the RockSat-X 2020 mission. The current delay between each step is 10 seconds. Each line in the below summary is a step.
# Initially waits.
# "Turns on" 360 camera and RFID experiment (not currently operational).
# Extends boom for specified length of time (dictated by the variable "motorOnTime").
# Retracts boom for specified length of time (dictated by the variable "motorOnTime").
# "Turns off" 360 camera and RFID experiment (not currently operational).
# To kill the motor, press Ctrl+C at any time. DO NOT USE THE STOP BUTTON!
# If all else fails, pull the jumper off the motor driver board. This action will immediately stop the motor. It cannot be started until the jumper is replaced, however.

# Import library functions we need
from __future__ import print_function
from diablo import *
from time import sleep
from sys import exit
import RPi.GPIO as GPIO # Fetch the GPIO library and initialize the object.
GPIO.setmode(GPIO.BCM)

# This value is the length of time (in seconds) for which the motor will be turned on for boom extension/retraction.
motorOnTime = 10 # CHANGE AS NECESSARY!!!

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
    print('Simulation started. First action will occur in 10 seconds.')
    sleep(10) # Sleep for 10 s, now at t = 10 s.
    print('Turning on 360 camera and RFID experiment... (currently does nothing)')
    # Add code to turn on 360 camera and RFID experiment.
    sleep(10) # Sleep for 10 s, now at t = 20 s.
    print('Extending boom...')
    DIABLO.SetMotor1(-1.0) # Activate the motor in a ccw direction (from back of motor).
    sleep(motorOnTime) # Sleep for the desired motor on time (please configure this delay above).
    DIABLO.SetMotor1(0.0) # Turn off motor.
    print('Boom extended. Holding position...')
    sleep(10) # Sleep for 10 s, now at t = 30 s + motorOnTime/1000.
    print('Retracting boom...')
    DIABLO.SetMotor1(+1.0) # Activate the motor in a cw direction (from back of motor)
    sleep(motorOnTime) # Sleep for the desired motor on time (again, please configure this delay above).
    DIABLO.SetMotor1(0.0)
    print('Boom retracted. Waiting to turn off camera and experiment...')
    sleep(10) # Sleep for 10 s, now at t = 40 s + 2 * motorOntime/1000.
    print('Turning off 360 camera and RFID experiment... (currently does nothing)')
    # Add code to turn off 360 camera and RFID experiment.
    
    DIABLO.MotorsOff() # Turn off motors just in case issues occur.
    print('The program has finished running.')
    
except KeyboardInterrupt:
    # User has pressed CTRL+C
    DIABLO.MotorsOff()              # Turn both motors off
    print ('Done')
