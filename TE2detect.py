#!user/bin/env  python

#This python program looks for TE2 to turn on
#by detecting a rising edge.
#Then the RPi sends a low on GPIO 19 to turn on the 
#mosfet latch

#file config.txt must have GPIO19 set to an output  
#and driving high upon RPi bootup.
#Add this command to config.txt:
#gpio=19=op,dh

import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)	#use the GPIO names, not actual pin numbers

TE2 = 16		#input
latch = 19		#output a low when TE2 has occurred to set latch


GPIO.setup(TE2,GPIO.IN,pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(latch,GPIO.OUT)

time.sleep(2)

print("Waiting for TE2 to occur")
GPIO.wait_for_edge(TE2,GPIO.RISING)
print("Edge detected!")
GPIO.output(latch,GPIO.LOW)
time.sleep(5)




