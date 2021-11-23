import RPi.GPIO as GPIO
import time

sensors = [37, 36, 33, 32, 31, 29, 18, 16]
led_enable = 22
GPIO.setmode(GPIO.BOARD)

for s in sensors:
    GPIO.setup(s, GPIO.IN)

GPIO.setup(led_enable, GPIO.OUT)
GPIO.output(led_enable, 1)

if __name__ == '__main__':

    counter = 0
    while counter<70:
        print("loop #", counter)
        counter+=1
        for s in sensors:
            if GPIO.input(s):
                print("on: ", s)
        time.sleep(2)
    GPIO.cleanup()

