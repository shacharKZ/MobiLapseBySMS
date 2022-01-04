from cv2 import PROJ_SPHERICAL_EQRECT  # TODO what is that??
import motor
import car_dir as dir
import video_dir as vid
import QTR_8RC as ir
# The tests import causes an issue, we probably don't need it anyway so it's commented out
# import tests
import time
from datetime import datetime

# 0 to suppress, 1 to print
from capture_handler import take_a_pic

DEBUG = 0

wall_speed = 33  # when connected to the power source directly
battery_speed = 80  # when connected to batteries only
battery_slow_speed = 55  # when connected to batteries only

speed_power = wall_speed


def stop_line(curr_object_num: int, curr_object_angle: str, curr_picture_num: int, session_timestamp: str):
    print("all 8 sensors see the line")
    print(f'Calling take a pic with angle {curr_object_angle}')
    motor.stop()
    vid.set_camera_to_angle(curr_object_angle)
    time.sleep(1.5)
    print('curr obj is:', curr_picture_num)
    take_a_pic(curr_object_num, curr_picture_num, session_timestamp)
    time.sleep(3)
    

actions_dir = {
    # '00000000': (print, "car don't see the line", 1),
    '00011000': (0, 1),
    '00001000': (0, 1),
    '00010000': (0, 1),
    '00111100': (0, 1),
    # '10111101': (0, 1),
    # '10011001': (0, 1),
    # '10010001': (0, 1),
    # '10001001': (0, 1),
    '11111111': (0, 1),

    '00001100': (-dir.TURN_15, 1),
    '00000100': (-dir.TURN_15, 1),
    '00000110': (-dir.TURN_25, 1),
    '00000010': (-dir.TURN_25, 1),
    '00000111': (-dir.TURN_35, 1.2),
    '00000011': (-dir.TURN_35, 1.2),
    '00000001': (-dir.TURN_45, 1.35),

    '00110000': (dir.TURN_15, 1),
    '00100000': (dir.TURN_15, 1),
    '01100000': (dir.TURN_25, 1),
    '01000000': (dir.TURN_25, 1),
    '11100000': (dir.TURN_35, 1.2),
    '11000000': (dir.TURN_35, 1.2),
    '10000000': (dir.TURN_45, 1.35),
}


def test_dir1():
    ir.setup_IR()
    dir.setup_direction()
    dir.home()

    # while True:
    for itt in range(3000):
        ir.check_above_line()
        print(f"{itt}:\t {ir.last_status_str}  ---> ", end="")
        if ir.last_status_str in actions_dir:
            print(f"{actions_dir[ir.last_status_str]}")
            action_to_exe, params = actions_dir[ir.last_status_str]
        else:
            print("action not set", ir.last_status_str)
        time.sleep(1)


def follow_line(num_objects: int = 4, object_angle_list=None, session_timestamp: str = 'tmpRun'):
    if object_angle_list is None:
        object_angle_list = ['HARD_RIGHT',
                             'HARD_RIGHT', 'HARD_RIGHT', 'HARD_RIGHT']
    print('Starting follow line')
    curr_object = 0
    picture_progress_list = [1] * num_objects
    ir.setup_IR()
    motor.setup_motor()
    dir.setup_direction()
    vid.setup_vid()
    vid.home_x_y()
    motor.setSpeed(speed_power, print_flag=True)
    time.sleep(1)
    motor.stop()  # TODO
    dir.home()
    prev_exe_angle = 0  # last angle the take aim to. helps with "softer" directions change

    time.sleep(4)
    motor.forward()  # TODO
    # while True:
    for itt in range(10000):
        ir_status_str = ir.check_above_line()

        # same_ir_as_prev = 0
        # for ir1, ir2 in zip(prev_state, last_status_str):
        #     if ir1 == ir2 == '1':
        #         same_ir_as_prev += 1

        if ir_status_str in actions_dir:
            exe_angle, speed_factor = actions_dir[ir_status_str]
            # if DEBUG:
            # print(ir.last_status_str)
            # if ir.last_status_str == '1111111':
            if ir_status_str == '11111111':
                # We encountered a stop line so we need to take a picture
                # Sending the number of the current picture of the current object to the image capture function
                prev_exe_angle = 0
                stop_line(curr_object + 1, object_angle_list[curr_object], picture_progress_list[curr_object],
                          session_timestamp)
                vid.home_x_y()
                dir.home()
                motor.setSpeed(speed_power)
                motor.forward()
                # sleep for a few seconds so we won't stop again on the stopping line
                time.sleep(0.5)
                # adjust the sensativity of the ir sensor according to the current light
                ir.adjust_thershold()

                # Incrementing the number of images for the current object
                picture_progress_list[curr_object] += 1
                # Updating the index of the next object to take an image for
                curr_object = (curr_object + 1) % num_objects
            elif (prev_exe_angle < 0 and exe_angle > 0) or (prev_exe_angle > 0 and exe_angle < 0):
                # in this case the turn was to "hard". might be a flake
                print('DID NOT TURN NOW!')
                print(f'curr angle={exe_angle}, prev angle={prev_exe_angle}')
                continue
            else:
                motor.setSpeed(int(speed_power*speed_factor))
                dir.turn_with_angle(exe_angle)
                prev_exe_angle = exe_angle
        else:
            if DEBUG:
                print("DEBUG DIR EXE: ???", ir_status_str)
        time.sleep(0.000002)

    motor.stop()


if __name__ == '__main__':
    follow_line()
