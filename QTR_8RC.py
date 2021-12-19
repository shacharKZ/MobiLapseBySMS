# from _typeshed import Self
import RPi.GPIO as GPIO
import time

led = 16  # TODO currently unsupported
sensors = [37, 36, 33, 32, 31, 29, 22, 18]
min_color = None  # this value is changing a bit from time to time. try adjust it
max_color = None
last_status_arr = [0, 0, 0, 0, 0, 0, 0, 0]
last_status_str = '00000000'


def setup_IR():
    global led, sensors, min_color, max_color, last_status_arr, last_status_str
    led = 16
    sensors = [37, 36, 33, 32, 31, 29, 22, 18]
    min_color = 80  # this value is changing a bit from time to time. try adjust it
    max_color = 150
    # last_status = [0, 0, 0, 0, 0, 0, 0, 0]
    last_status_str = '00000000'
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(led, GPIO.OUT)


# def check_above_line():
#     global led, sensors, min_color, max_color, last_status, last_status_str
#     last_status_str = ""
#     for index, s in enumerate(sensors):
#         GPIO.setup(s, GPIO.OUT)
#         GPIO.output(s, GPIO.HIGH)
#         time.sleep(0.01)
#         GPIO.setup(s, GPIO.IN)
#         counter = 0
#         while GPIO.input(s) and counter < min_color:
#             counter += 1
#             # GPIO.output(led, GPIO.HIGH)
#         GPIO.output(led, GPIO.LOW)
#         # last_status[index] =  int(counter == min_color)
#         last_status_str += '1' if counter == min_color else '0'
#     return last_status_str

def check_above_line():
    global led, sensors, min_color, max_color, last_status_arr, last_status_str
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

    res_str = ""
    for color in res:
        res_str += ('1' if color >= min_color else '0')

    last_status_str = res_str
    return last_status_str


def adjust_thershold():
    global led, sensors, min_color, max_color, last_status_arr, last_status_str
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

    print(color_list)
    if color_list[-1] > color_list[-2] + 23:
        min_color = color_list[-1] - 17
    elif color_list[-2] > color_list[-3] + 30:
        min_color = color_list[-2] - 17
    max_color = min_color + 70

    print(f'new min={min_color}, new max={max_color}')


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


# def all_above_line():
#     global last_status
#     return last_status == [1, 1, 1, 1, 1, 1, 1, 1]


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
    # op1_5()
    # op2()
    # op3()
    # op4()
    op5()
