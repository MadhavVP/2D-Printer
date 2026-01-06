import RPi.GPIO as GPIO
import sys
import tty
import termios
import time

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
    gpio_map = {'a':17, 'd':27, 'w':22, 's':23}
    dir_map = {'a':'left', 'd':'right', 'w':'up', 's':'down'}

    GPIO.setmode(GPIO.BCM)
    for x in list(gpio_map.values()):
        GPIO.setup(x, GPIO.OUT)

    prev = 'p'
    while True:
        c = getc()
        if prev in gpio_map:
            GPIO.output(gpio_map[prev], GPIO.LOW)
        if c == 'q':
            break
        if c in gpio_map:
            GPIO.output(gpio_map[c], GPIO.HIGH)
            print(f'{dir_map[c]}')
        prev = c

if __name__ == "__main__":
    main()
