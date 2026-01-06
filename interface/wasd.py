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
    gpio_outs = [17, 27, 22, 23]
    gpio_map = {'a':[17, 27, GPIO.HGIH], 'd':[17, 27, GPIO.LOW], 'w':[22, 23, GPIO.HIGH], 's':[22, 23, GPIO.LOW]}
    dir_map = {'a':'left', 'd':'right', 'w':'up', 's':'down'}

    GPIO.setmode(GPIO.BCM)
    for x in gpio_outs:
        GPIO.setup(x, GPIO.OUT)

    while True:
        c = getc()
        if c == 'q':
            break
        if c in gpio_map:
            GPIO.output(gpio_map[c][1], gpio_map[c][2])
            GPIO.output(gpio_map[c][0], GPIO.HIGH)
            print(f'{dir_map[c]}')
            sleep(0.01)
            GPIO.output(gpio_map[c][0], GPIO.LOW)
            GPIO.output(gpio_map[c][1], GPI.LOW)

if __name__ == "__main__":
    main()
