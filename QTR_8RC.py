# from _typeshed import Self
import RPi.GPIO as GPIO
import time

# led = 16  # currently unsupported led pin
sensors = [37, 36, 33, 32, 31, 29, 22, 18]
last_status_arr = [0, 0, 0, 0, 0, 0, 0, 0]
last_status_str = '00000000'
init_min_color = 75
init_max_color = 200
# this value is changing a bit from time to time. try adjust it
min_color = init_min_color
max_color = init_max_color
possible_stop_line = init_min_color


def setup_IR():
    global led, sensors, min_color, max_color, init_min_color, init_max_color, last_status_arr, last_status_str, possible_stop_line
    led = 16
    sensors = [37, 36, 33, 32, 31, 29, 22, 18]
    # this value is changing a bit from time to time. try adjust it
    min_color = init_min_color
    max_color = init_max_color
    # last_status = [0, 0, 0, 0, 0, 0, 0, 0]
    last_status_str = '00000000'
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(led, GPIO.OUT)


# def check_above_line():
#     global led, sensors, min_color, max_color, last_status_arr, last_status_str
#     last_status_str = ""
#     for s in sensors:
#         GPIO.setup(s, GPIO.OUT)
#         GPIO.output(s, GPIO.HIGH)

#     time.sleep(0.01)

#     for s in sensors:
#         GPIO.setup(s, GPIO.IN)

#     res = [0, 0, 0, 0, 0, 0, 0, 0]
#     for _ in range(max_color):
#         for index, s in enumerate(sensors):
#             res[index] += GPIO.input(s)

#     last_status_arr = res

#     res_str = ""
#     for color in res:
#         res_str += ('1' if color >= min_color else '0')

#     last_status_str = res_str
#     return last_status_str


def check_above_line():
    global led, sensors, min_color, max_color, last_status_arr, last_status_str, possible_stop_line
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

    # # min_color = init_min_color  # TODO
    # min_color = possible_stop_line
    # # if min(res) > min(init_min_color, possible_stop_line):
    # if min(res) > possible_stop_line:  # TODO
    #     res_str = "11111111"
    # print(
    #     f'all ir sensors sees the line with possible_stop_line {possible_stop_line}')
    #     return res_str
    # elif max(res) < 70:
    #     if max(res) >= 2.6*min(res):
    #         min_color = max(res)*0.9
    #         possible_stop_line = max(res)*0.8
    # elif max(res) > 2*min(res):
    #     min_color = max(res)*0.9
    #     possible_stop_line = max(res)*0.85

    # min_color = init_min_color
    if min(res) > min_color:
        res_str = "11111111"
        print(
            f'all ir sensors sees the line with possible_stop_line {possible_stop_line}')
        return res_str
    elif max(res) < 70:
        if max(res) >= 2.6*min(res):
            min_color = max(res)*0.9
            possible_stop_line = max(res)*0.8
    elif max(res) > 2*min(res):
        min_color = max(res)*0.8

    res_str = ""
    for color in res:
        res_str += ('1' if color >= min_color else '0')

    last_status_str = res_str
    # TODO for debug only
    print(res, "<-------->", res_str, f'--> min is {min_color}')
    return last_status_str


def adjust_thershold():
    return  # TODO
    global led, sensors, min_color, max_color, init_max_color, init_max_color, last_status_arr, last_status_str
    for s in sensors:
        GPIO.setup(s, GPIO.OUT)
        GPIO.output(s, GPIO.HIGH)

    time.sleep(0.01)

    for s in sensors:
        GPIO.setup(s, GPIO.IN)

    color_list = [0, 0, 0, 0, 0, 0, 0, 0]
    for _ in range(max_color):
        for index, s in enumerate(sensors):
            color_list[index] += GPIO.input(s)

    color_list.sort()
    debug_code = 0
    if color_list[-1] > color_list[-2] + 30:
        min_color = min(init_min_color, color_list[-1] - 7)
        debug_code = 1
    elif color_list[-1] < color_list[-2] + 15 and color_list[-2] > color_list[-3] + 30:
        min_color = min(init_min_color, color_list[-2] - 7)
        debug_code = 2

    print(
        f'Adjust IR sensor threshold: new min={min_color}, new max={max_color}. color_list was:{color_list} (code={debug_code})')


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


class IR_array_sensor:
    def __init__(self):
        self._led = 16
        self._sensors = [37, 36, 33, 32, 31, 29, 22, 18]
        self._min = 1122
        self._max = 3000
        self._last_status = [0, 0, 0, 0, 0, 0, 0, 0]
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self._led, GPIO.OUT)

    def check_above_line(self):
        for index, s in enumerate(self._sensors):
            GPIO.setup(s, GPIO.OUT)
            GPIO.output(s, GPIO.HIGH)
            time.sleep(0.01)
            GPIO.setup(s, GPIO.IN)
            counter = 0
            while GPIO.input(s) and counter < self._max:
                counter += 1
                GPIO.output(self._led, GPIO.HIGH)
            GPIO.output(self._led, GPIO.LOW)
            self._last_status[index] = int(counter > self._min)
        return self._last_status

    def check_color(self):
        res = []
        for s in self._sensors:
            GPIO.setup(s, GPIO.OUT)
            GPIO.output(s, GPIO.HIGH)
            time.sleep(0.01)
            GPIO.setup(s, GPIO.IN)
            counter = 0
            while GPIO.input(s) and counter < 100000:
                counter += 1
                GPIO.output(self._led, GPIO.HIGH)
            GPIO.output(self._led, GPIO.LOW)
            res.append(counter)
        return res

    def print_status(self):
        return self._last_status


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


def op4():
    ir = IR_array_sensor()
    while True:
        print(ir.check_above_line())
        # print(ir.check_color())


def op5():
    setup_IR()
    while True:
        print(check_above_line())
        print(last_status_arr)
        time.sleep(1)


if __name__ == '__main__':
    # op4()
    op5()
