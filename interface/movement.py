import RPi.GPIO as GPIO
from time import sleep
from home import home
from constants import gpio_outs, gpio_map, ms1, ms2, ms3, stepspeed

class Head():
    def __init__(self):
        home()
        self.curx = 0
        self.cury = 0
        self.pendown = False

        GPIO.setmode(GPIO.BCM)
        for x in gpio_outs:
            GPIO.setup(x, GPIO.OUT)

        GPIO.output(ms1, GPIO.HIGH)
        GPIO.output(ms2, GPIO.HIGH)
        GPIO.output(ms3, GPIO.HIGH)

    def move(self, xnext, ynext):
        dx = xnext - self.curx
        dirx = 'a'
        if dx < 0:
            dirx = 'd'
        for i in range(abs(dx)):
            self.step(dirx)

        self.curx = xnext
        
        diry = 'w'
        dy = ynext - self.cury
        if dy < 0:
            diry = 's'
        for i in range(abs(dy)):
            self.step(diry)

        self.cury = ynext

    def step(self, direction):
        GPIO.output(gpio_map[direction][1], gpio_map[direction][2])
        GPIO.output(gpio_map[direction][0], GPIO.HIGH)
        sleep(stepspeed)
        GPIO.output(gpio_map[direction][0], GPIO.LOW)
        GPIO.output(gpio_map[direction][1], GPIO.LOW)

    def activate(self):
        if not self.pendown:
            for i in range(penoffset):
                self.step('p')
        self.pendown = True

    def release(self):
        if self.pendown:
            for i in range(penoffset):
                self.step('u')
        self.pendown = False

    def close(self):
        home()
        self.curx = 0
        self.cury = 0
