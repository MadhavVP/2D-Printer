import RPi.GPIO as GPIO
import sys
import tty
import termios
from time import sleep
from constants import gpio_map, gpio_outs, dir_map, allms, penoffset, xstop, ystop

def getc():
    fd = sys.stdin.fileno()
    cooked = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, cooked)
    return ch

def main():

    GPIO.setmode(GPIO.BCM)
    for x in gpio_outs:
        GPIO.setup(x, GPIO.OUT)

    GPIO.output(allms, GPIO.HIGH)

    GPIO.setup(xstop, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(ystop, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    while True:
        c = getc()
        if c == 'q':
            for x in gpio_outs:
                GPIO.output(x, GPIO.LOW)
            break
        if c in gpio_map:
            GPIO.output(gpio_map[c][1], gpio_map[c][2])
            steps = 1000
            slptime = 0.0005
            if c == 'u' or c == 'p':
                steps = penoffset
                slptime = 0.005
            for i in range(steps):
                if GPIO.input(ystop) and GPIO.input(xstop):
                    GPIO.output(gpio_map[c][0], GPIO.HIGH)
                    sleep(slptime)
                    GPIO.output(gpio_map[c][0], GPIO.LOW)
                if not GPIO.input(xstop):
                    GPIO.output(gpio_map['a'][1], gpio_map['a'][2])
                    while not GPIO.input(xstop):
                        GPIO.output(gpio_map['a'][0], GPIO.HIGH)
                        sleep(slptime)
                        GPIO.output(gpio_map['a'][0], GPIO.LOW)
                if not GPIO.input(ystop):
                    GPIO.output(gpio_map['w'][1], gpio_map['w'][2])
                    while not GPIO.input(ystop):
                        GPIO.output(gpio_map['w'][0], GPIO.HIGH)
                        sleep(slptime)
                        GPIO.output(gpio_map['w'][0], GPIO.LOW)
                

            GPIO.output(gpio_map[c][1], GPIO.LOW)
            print(f'{dir_map[c]}')

if __name__ == "__main__":
    main()
