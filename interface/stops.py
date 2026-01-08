import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
ystop = 20
xstop = 21  
GPIO.setup(ystop, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(xstop, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    if GPIO.input(ystop):
        print("Y not pressed")
    else:
        print("Y pressed")
    if GPIO.input(xstop):
        print("X not pressed")
    else:
        print("X pressed")
    sleep(1)
