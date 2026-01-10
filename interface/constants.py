import RPi.GPIO as GPIO

gpio_outs = [17, 27, 22, 23, 2, 3, 4]
gpio_map = {'a':[17, 27, GPIO.HIGH], 'd':[17, 27, GPIO.LOW], 'w':[22, 23, GPIO.HIGH], 's':[22, 23, GPIO.LOW],
            'p':[3, 2, GPIO.LOW], 'u':[3, 2, GPIO.HIGH]}
dir_map = {'a':'left', 'd':'right', 'w':'up', 's':'down', 'p':'pencil down', 'u':'pencil up'}
allms = 4
#ms2 = 3
#ms3 = 2
xstop = 21
ystop = 20
stepspeed = 0.00005
penoffset = 96
