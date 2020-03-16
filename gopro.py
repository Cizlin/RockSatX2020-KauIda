#
#!/user/bin/env  python

from gpiozero import LED
from time import sleep
import sys


power = LED(21)
rec = LED(26)
gp_enable = LED(13)

power.off()
rec.off()
gp_enable.off()

gp_enable.on()	#high, closes relay

#This section powers on GoPro
power.on()	#turn on Q3 so GPPower goes to  gnd
sleep(1)
power.off()	#turn off Q3 so GPPower floats
sleep(1)

#This section starts recording and stops recording
#A falling edge starts/stop recording

rec.off()	#turn OFF Q1 so GPRec now floats
sleep(5)	#GoPro seems to need this set up time
rec.on()	#turn ON Q1 so GPRec goes to gnd falling edge starts record
sleep(4)	#record time
rec.off()
sleep(2)	#still recording
rec.on()	#Q1 on, GPRec go low and stops recording
sleep(2)

#this section powers off the GoPor


power.on()
sleep(5)
power.off()
sleep(1)
gp_enable.off()

print("GoPro done")

#sys.exit(0)


