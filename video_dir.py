#!/usr/bin/env python
import PCA9685 as servo
import time  # Import necessary modules

MinPulse = 200  # original that was 200. we changed it
MaxPulse = 700  # original that was 700. we changed it

Current_x = 0  # original that was 0. we changed it
Current_y = 0  # original that was 0. we changed it

ANGLE_T0_DIR_DICT = {
    -90: (0, 0),
    -45: (30, 0),
    0: (50, 0),
    45: (70, 0),
    90: (90, 0)
}


def setup_vid(busnum=None):
    global Xmin, Ymin, Xmax, Ymax, home_x, home_y, pwm
    offset_x = 0  # original that was 0. we changed it
    offset_y = 0  # original that was 0. we changed it
    try:
        for line in open('config'):
            if line[0:8] == 'offset_x':
                offset_x = int(line[11:-1])
                # print 'offset_x =', offset_x
            if line[0:8] == 'offset_y':
                offset_y = int(line[11:-1])
                # print 'offset_y =', offset_y
    except:
        pass
    Xmin = MinPulse + offset_x
    Xmax = MaxPulse + offset_x
    Ymin = MinPulse + offset_y
    Ymax = MaxPulse + offset_y
    # print("!!!", (Xmax + Xmin)/2, Ymin+80)
    # print("???x?", offset_x, "???y?", offset_y)
    # print('max are: Xmax', Xmax, ', Ymax', Ymax)
    # print('min are: Xmin', Xmin, ', Ymin', Ymin)
    # print('max are: Xmax', Xmax, ', Ymax', Ymax)
    home_x = (Xmax + Xmin) / 2
    home_y = Ymin + 80
    if busnum == None:
        pwm = servo.PWM()  # Initialize the servo controller.
    else:
        pwm = servo.PWM(bus_number=busnum)  # Initialize the servo controller.
    pwm.frequency = 60


# ==========================================================================================
# Control the servo connected to channel 14 of the servo control board to make the camera
# turning towards the positive direction of the x axis.
# ==========================================================================================


def move_decrease_x():
    global Current_x
    Current_x += 25
    if Current_x > Xmax:
        Current_x = Xmax
    pwm.write(14, 0, Current_x)
    # ==========================================================================================


# Control the servo connected to channel 14 of the servo control board to make the camera
# turning towards the negative direction of the x axis.
# ==========================================================================================


def move_increase_x():
    global Current_x
    Current_x -= 25
    if Current_x <= Xmin:
        Current_x = Xmin
    pwm.write(14, 0, Current_x)


# ==========================================================================================
# Control the servo connected to channel 15 of the servo control board to make the camera
# turning towards the positive direction of the y axis.
# ==========================================================================================


def move_increase_y():
    global Current_y
    Current_y += 25
    if Current_y > Ymax:
        Current_y = Ymax
    pwm.write(15, 0, Current_y)  # CH15 <---> Y axis


# ==========================================================================================
# Control the servo connected to channel 15 of the servo control board to make the camera
# turning towards the negative direction of the y axis.
# ==========================================================================================


def move_decrease_y():
    global Current_y
    Current_y -= 25
    if Current_y <= Ymin:
        Current_y = Ymin
    pwm.write(15, 0, Current_y)


# ==========================================================================================
# Control the servos connected with channel 14 and 15 at the same time to make the camera
# move forward.
# ==========================================================================================


def home_x_y():
    global Current_y
    global Current_x
    Current_y = home_y
    Current_x = home_x
    pwm.write(14, 0, Current_x)
    pwm.write(15, 0, Current_y)


def calibrate(x, y):
    pwm.write(14, 0, (MaxPulse + MinPulse) / 2 + x)
    pwm.write(15, 0, (MaxPulse + MinPulse) / 2 + y)


def set_camera_to_angle(angle: int):
    x, y = ANGLE_T0_DIR_DICT.get(angle, (0, 0))
    set_dir(x, y)


def test():
    while True:
        home_x_y()
        time.sleep(0.5)
        for i in range(0, 9):
            move_increase_x()
            move_increase_y()
            time.sleep(0.5)
        for i in range(0, 9):
            move_decrease_x()
            move_decrease_y()
            time.sleep(0.5)

def set_dir(x, y=home_y):
    # print("(x,y): ", '(', x, ',', y, ')')
    global Current_y
    Current_y = y
    if Current_y < Ymin:
        Current_y = Ymin
    elif Current_y > Ymax:
        Current_y = Ymax
    pwm.write(15, 0, Current_y)

    global Current_x
    Current_x = x
    if Current_x < Xmin:
        Current_x = Xmin
    elif Current_x > Xmax:
        Current_x = Xmax
    pwm.write(14, 0, Current_x)


def set_dir_according_to_home(x, y=0):
    global home_y
    y = home_y + y
    global home_x
    x = home_x + x
    set_dir(x, y)


def get_dir():
    global Current_x
    global Current_y
    return Current_x, Current_y


if __name__ == '__main__':
    setup_vid()
    home_x_y()
