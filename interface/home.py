import RPi.GPIO as GPIO
from time import sleep

def home():
    gpio_outs = [17, 27, 22, 23, 2, 3, 4]
    gpio_map = {'a':[17, 27, GPIO.HIGH], 'd':[17, 27, GPIO.LOW], 'w':[22, 23, GPIO.HIGH], 's':[22, 23, GPIO.LOW]}
    dir_map = {'a':'left', 'd':'right', 'w':'up', 's':'down'}
    ms1 = 4
    ms2 = 3
    ms3 = 2
    xstop = 21
    ystop = 20

    offsetsteps = 800

    GPIO.setmode(GPIO.BCM)
    for x in gpio_outs:
        GPIO.setup(x, GPIO.OUT)

    GPIO.output(ms1, GPIO.HIGH)
    GPIO.output(ms2, GPIO.HIGH)
    GPIO.output(ms3, GPIO.HIGH)

    GPIO.setup(xstop, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(ystop, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    while GPIO.input(xstop):
        GPIO.output(gpio_map['d'][1], gpio_map['d'][2])
        GPIO.output(gpio_map['d'][0], GPIO.HIGH)
        sleep(0.0001)
        GPIO.output(gpio_map['d'][0], GPIO.LOW)
        GPIO.output(gpio_map['d'][1], GPIO.LOW)

    for x in range(offsetsteps):
        GPIO.output(gpio_map['a'][1], gpio_map['a'][2])
        GPIO.output(gpio_map['a'][0], GPIO.HIGH)
        sleep(0.0005)
        GPIO.output(gpio_map['a'][0], GPIO.LOW)
        GPIO.output(gpio_map['a'][1], GPIO.LOW)

    while GPIO.input(ystop):
        GPIO.output(gpio_map['s'][1], gpio_map['s'][2])
        GPIO.output(gpio_map['s'][0], GPIO.HIGH)
        sleep(0.0001)
        GPIO.output(gpio_map['s'][0], GPIO.LOW)
        GPIO.output(gpio_map['s'][1], GPIO.LOW)

    for x in range(offsetsteps):
        GPIO.output(gpio_map['w'][1], gpio_map['w'][2])
        GPIO.output(gpio_map['w'][0], GPIO.HIGH)
        sleep(0.0005)
        GPIO.output(gpio_map['w'][0], GPIO.LOW)
        GPIO.output(gpio_map['w'][1], GPIO.LOW)
        
    print("HOMING FINISHED")
