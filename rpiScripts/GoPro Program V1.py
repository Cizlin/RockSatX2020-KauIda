from gpiozero import LED
from time import sleep
led = LED(13)
led2 = LED(26)
led3 = LED(21)

while True:
    led.on()
    sleep (1)
    led.off()
    sleep (1)
    