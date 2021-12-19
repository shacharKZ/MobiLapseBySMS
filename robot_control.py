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

wall_speed = 37  # when connected to the power source directly
battery_speed = 80  # when connected to batteries only
battery_slow_speed = 55  # when connected to batteries only


def stop_line(curr_object_num: int, curr_object_angle: str, curr_picture_num: int, session_timestamp: str):
    print("all 8 sensors see the line")
    print(f'Calling take a pic with angle {curr_object_angle}')
    motor.stop()
    vid.set_camera_to_angle(curr_object_angle)
    time.sleep(1.5)
    print('curr obj is:', curr_picture_num)
    take_a_pic(curr_object_num, curr_picture_num, session_timestamp)
    time.sleep(3)
    vid.home_x_y()
    motor.forward()
    time.sleep(0.3)


actions_dir = {
    '00000000': (print, "car don't see the line", 1),
    '00011000': (dir.home, None, 1),
    '00001000': (dir.home, None, 1),
    '00010000': (dir.home, None, 1),
    '00111100': (dir.home, None, 1),
    '10111101': (dir.home, None, 1),
    '10011001': (dir.home, None, 1),
    '10010001': (dir.home, None, 1),
    '10001001': (dir.home, None, 1),
    '11111111': (stop_line, None, 1),

    '00001100': (dir.turn_left, dir.TURN_15, 1),
    '00000100': (dir.turn_left, dir.TURN_15, 1),
    '00000110': (dir.turn_left, dir.TURN_25, 1),
    '00000010': (dir.turn_left, dir.TURN_25, 1),
    '00000111': (dir.turn_left, dir.TURN_35, 1.2),
    '00000011': (dir.turn_left, dir.TURN_35, 1.2),
    '00000001': (dir.turn_left, dir.TURN_45, 1.5),

    '00110000': (dir.turn_right, dir.TURN_15, 1),
    '00100000': (dir.turn_right, dir.TURN_15, 1),
    '01100000': (dir.turn_right, dir.TURN_25, 1),
    '01000000': (dir.turn_right, dir.TURN_25, 1),
    '11100000': (dir.turn_right, dir.TURN_35, 1.2),
    '11000000': (dir.turn_right, dir.TURN_35, 1.2),
    '10000000': (dir.turn_right, dir.TURN_45, 1.5),
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
    speed_power = wall_speed

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
    motor.setSpeed(speed_power)
    time.sleep(1)
    motor.stop()  # TODO
    dir.home()
    prev_state = '00011000'

    time.sleep(4)
    motor.forward()  # TODO
    # while True:
    for itt in range(10000):
        last_status_str = ir.check_above_line()

        same_ir_as_prev = 0
        for ir1, ir2 in zip(prev_state, last_status_str):
            if ir1 == ir2:
                same_ir_as_prev += 1

        if last_status_str in actions_dir:
            action_to_exe, params, speed_factor = actions_dir[last_status_str]
            # if DEBUG:
            print(action_to_exe, params)
            print(ir.last_status_str)
            # if ir.last_status_str == '1111111':
            if action_to_exe == stop_line:
                # We encountered a stop line so we need to take a picture
                # Sending the number of the current picture of the current object to the image capture function
                action_to_exe(curr_object + 1, object_angle_list[curr_object], picture_progress_list[curr_object],
                              session_timestamp)
                # Incrementing the number of images for the current object
                picture_progress_list[curr_object] += 1
                # Updating the index of the next object to take an image for
                curr_object = (curr_object + 1) % num_objects
            elif same_ir_as_prev >= 6:
                print(same_ir_as_prev)
                motor.setSpeed(int(speed_power*speed_factor))
                action_to_exe(params)
                prev_state = last_status_str
        else:
            if DEBUG:
                print("car: ???", last_status_str)
        time.sleep(0.000002)

    motor.stop()


if __name__ == '__main__':
    # p1 = Position(330, 20)
    # p2 = Position(250, 400)
    # p3 = Position(350, 250)
    # p_list = [Position(350, 250), Position(350, 300), Position(450, 300), Position(450, 200), \
    #     Position(320, 300), Position(500, 300), Position(500, 200), Position(300, 300)]
    # # test_everything(p_list)
    # test_showoff()

    # test2()
    # time.sleep(5)
    # test3()
    # test_dir1()

    follow_line()
    # take_a_pic()
