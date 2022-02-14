# from _typeshed import Self
from doctest import debug_script
import RPi.GPIO as GPIO
import time

debug_flag = 1  # 1 to print debug. 0 to slient

# led = 16  # currently unsupported led pin
sensors = [37, 36, 33, 32, 31, 29, 22, 18]
last_status_arr = [0, 0, 0, 0, 0, 0, 0, 0]
last_status_str = '00000000'
min_color = 75
max_color = 200
last_time_did_not_see_the_line = 0


def setup_IR():
    global led, sensors, min_color, max_color, last_status_arr, last_status_str, last_time_did_not_see_the_line
    led = 16
    sensors = [37, 36, 33, 32, 31, 29, 22, 18]
    # this value is changing a bit from time to time. try adjust it
    min_color = 70
    max_color = 200
    # last_status = [0, 0, 0, 0, 0, 0, 0, 0]
    last_status_str = '00000000'
    last_time_did_not_see_the_line = 0
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(led, GPIO.OUT)


def check_above_line():
    global led, sensors, min_color, max_color, last_status_arr, last_status_str, last_time_did_not_see_the_line
    last_status_str = ""
    for s in sensors:
        GPIO.setup(s, GPIO.OUT)
        GPIO.output(s, GPIO.HIGH)

    time.sleep(0.01)

    for s in sensors:
        GPIO.setup(s, GPIO.IN)

    res = [0, 0, 0, 0, 0, 0, 0, 0]
    for _ in range(max_color):
        for index, s in enumerate(sensors):
            res[index] += GPIO.input(s)

    last_status_arr = res

    # min_color = init_min_color
    if max(res) > 2*min(res):
        min_color = max(res)*0.83
    elif 75 > max(res) > min(res) + 15:
        min_color = max(res) - 5
    elif min(res) > min_color and time.time() - last_time_did_not_see_the_line > 0.7:
        res_str = "11111111"
        if debug_flag:
            print(
                f'all ir sensors sees the line with possible_stop_line {min_color}')
            print(res)
        return res_str

    # elif max(res) < 77:
    #     if max(res) > 2*min(res) and max(res) > 40:
    #         if max(res) > 60:
    #             min_color = max(res)*0.91
    #         else:
    #             min_color = max(res)*0.95
    #     elif time.time() - last_time_did_not_see_the_line < 0.7 and max(res) > min(res) + 10 > 55:
    #         min_color = max(res)*0.93
    # elif max(res) > 2*min(res):
    #     min_color = max(res)*0.83
    # elif time.time() - last_time_did_not_see_the_line < 0.7 and max(res) > min(res) + 10 > 55:
    #     min_color = max(res)*0.93

    res_str = ""
    for color in res:
        res_str += ('1' if color >= min_color else '0')

    if res_str == "00000000":
        last_time_did_not_see_the_line = time.time()

    if debug_flag:
        print(res, "<-------->", res_str, f'--> curr min_color is {min_color}')
    last_status_str = res_str
    return last_status_str


def check_color():
    global led, sensors, min_color, max_color, last_status_arr
    res = []
    for s in sensors:
        GPIO.setup(s, GPIO.OUT)
        GPIO.output(s, GPIO.HIGH)
        time.sleep(0.01)
        GPIO.setup(s, GPIO.IN)
        counter = 0
        while GPIO.input(s) and counter < max_color:
            counter += 1
            GPIO.output(led, GPIO.HIGH)
        GPIO.output(led, GPIO.LOW)
        res.append(counter)
    return res


def read_color(pin_sensor, pin_led):
    GPIO.setup(pin_sensor, GPIO.OUT)
    GPIO.setup(pin_led, GPIO.OUT)
    GPIO.output(pin_sensor, 1)
    time.sleep(0.01)
    GPIO.setup(pin_sensor, GPIO.IN)
    counter = 0
    while GPIO.input(pin_sensor) and counter < 1000000:
        counter += 1
        GPIO.output(pin_led, GPIO.HIGH)
    GPIO.output(pin_led, 0)
    return counter


def op5():
    setup_IR()
    while True:
        print(check_above_line())
        print(last_status_arr)
        time.sleep(1)


if __name__ == '__main__':
    op5()
