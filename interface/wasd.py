import RPi.GPIO as GPIO
import sys
import tty
import termios
from time import sleep

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
    gpio_outs = [17, 27, 22, 23, 2, 3, 4]
    gpio_map = {'a':[17, 27, GPIO.HIGH], 'd':[17, 27, GPIO.LOW], 'w':[22, 23, GPIO.HIGH], 's':[22, 23, GPIO.LOW]}
    dir_map = {'a':'left', 'd':'right', 'w':'up', 's':'down'}
    ms1 = 4
    ms2 = 3
    ms3 = 2

    GPIO.setmode(GPIO.BCM)
    for x in gpio_outs:
        GPIO.setup(x, GPIO.OUT)

    GPIO.output(ms1, GPIO.HIGH)
    GPIO.output(ms2, GPIO.HIGH)
    GPIO.output(ms3, GPIO.HIGH)

    while True:
        c = getc()
        if c == 'q':
            for x in gpio_outs:
                GPIO.output(x, GPIO.LOW)
            break
        if c in gpio_map:
            GPIO.output(gpio_map[c][1], gpio_map[c][2])
            for i in range(800):
                GPIO.output(gpio_map[c][0], GPIO.HIGH)
                #print(f'{dir_map[c]}')
                sleep(0.0005)
                GPIO.output(gpio_map[c][0], GPIO.LOW)
            GPIO.output(gpio_map[c][1], GPIO.LOW)

if __name__ == "__main__":
    main()
