import RPi.GPIO as GPIO
from time import sleep
from home import home
from constants import gpio_outs, gpio_map, allms, stepspeed, penoffset, mstepsperstep

class Head():
    def __init__(self):
        home()
        self.curx = 0
        self.cury = 0
        self.pendown = False

        GPIO.setmode(GPIO.BCM)
        for x in gpio_outs:
            GPIO.setup(x, GPIO.OUT)

        GPIO.output(allms, GPIO.HIGH)

    def move(self, xnext, ynext):
        dx = xnext - self.curx
        dirx = 'a'
        if dx < 0:
            dirx = 'd'
        self.step(dirx, abs(dx) * mstepsperstep)

        self.curx = xnext
        
        diry = 'w'
        dy = ynext - self.cury
        if dy < 0:
            diry = 's'
        self.step(diry, abs(dy) * mstepsperstep)

        self.cury = ynext

    def step(self, direction, numsteps):
        for i in range(numsteps):
            GPIO.output(gpio_map[direction][1], gpio_map[direction][2])
            GPIO.output(gpio_map[direction][0], GPIO.HIGH)
            sleep(stepspeed)
            GPIO.output(gpio_map[direction][0], GPIO.LOW)
            GPIO.output(gpio_map[direction][1], GPIO.LOW)

    def activate(self):
        if not self.pendown:
                self.step('p', penoffset)
        self.pendown = True

    def release(self):
        if self.pendown:
                self.step('u', penoffset)
        self.pendown = False

    def close(self):
        home()
        self.curx = 0
        self.cury = 0
