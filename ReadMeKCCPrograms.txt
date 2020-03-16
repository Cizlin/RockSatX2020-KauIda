3/15/2020 Project KauIda
-------------------------------------------
file: config.txt
This is a copy of the config.txt file on the RPi.
GPIO 13, 19, 21, and 26 need to be configured at boot up.
Drives the latch circuit for battery backup and the GoPro camers.
This code addition in the config.txt accomplishes the setup:

#set GPIO19 to be an output set to 1
#set GPIO 26,21,13 to be an output set low
gpio=19=op,dh
gpio=26=op,dl
gpio=21=op,dl
gpio=13=op,dl

Optionally, we may want to disable undervoltage errors. KCC is still chasing this.

----------------------------------------------------------------------------------
file: gopro.py
This Python program is called in the thetaVscript file.
gopro.py turns on the GoPro, records, then turns off.
The program was written using the LED module.
It may be equally accomplished with the GPIO module 
(and probably should be re written).
Please be mindful of what falling edges and dwell times are needed. 

----------------------------------------------------------------------
file: TE2detect.py
This program has not yet been placee in the overall mission timeline because
it waits for TE2 to occur.
After TE2 occurs, circuit is latche and battery backup is enabled.
KCC thinks TE2 needs to occur shortly after launch. 

-----------------------------------

file: thetaVscript
This script is run by a service at Rpi boot up.
It is the master mission script