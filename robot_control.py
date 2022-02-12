# TODO what is that?? should we remove it?
# from cv2 import PROJ_SPHERICAL_EQRECT
import requests

import motor
import car_dir as dir
import video_dir as vid
import QTR_8RC as ir
import power_management as power
import time
from datetime import datetime
from capture_handler import take_a_pic
from anomaly_detection import check_anomaly_last_cap

# 0 to suppress, 1 to print debuggin messages
from db_handler import write_robot_error_to_db

DEBUG = 0

wall_speed = 30  # when connected to the power source directly
battery_speed = 50  # when connected to batteries only

# speed_power = wall_speed
speed_power = battery_speed


def stop_line(curr_object_num: int, curr_object_angle: str, curr_picture_num: int, session_timestamp: str,
              prev_imgs: list, num_of_non_anomaly):
    print("all 8 sensors see the line")
    print(f'Calling take a pic with angle {curr_object_angle}')
    motor.stop()
    vid.set_camera_to_angle(curr_object_angle)
    time.sleep(1.5)
    print('curr obj is:', curr_picture_num)
    take_a_pic(curr_object_num, curr_picture_num, session_timestamp, prev_imgs)
    detected_anomaly = check_anomaly_last_cap(
        prev_imgs, num_of_non_anomaly, curr_object_num=curr_object_num)
    # if detected_anomaly:
    #     vid.make_gesture(1)
    time.sleep(3)
    print("!!!!!! check power after stop: ")
    power.check_voltage()  # TODO
    return detected_anomaly


def try_to_refind_the_line(prev_exe_angle) -> bool:
    motor.stop()
    time.sleep(1)
    exe_angle = dir.TURN_45
    if prev_exe_angle < 0:
        exe_angle = -dir.TURN_45
    dir.turn_with_angle(-exe_angle)
    motor.setSpeed(speed_power*0.7)
    motor.backward()
    time.sleep(0.7)
    motor.stop()
    time.sleep(0.7)
    dir.turn_with_angle(prev_exe_angle)
    motor.setSpeed(speed_power)
    motor.forward()
    starting_time_for_searching_line = time.time()
    while time.time() - starting_time_for_searching_line < 5:
        time.sleep(0.005)
        if ir.check_above_line() in actions_dir:
            return True
    return False


actions_dir = {
    '00001000': (0, 1),  # staight forward. bias to the left
    '11111111': (0, 1),  # this is never been use (only for improving codeing)

    '00001100': (-dir.TURN_15, 1),
    '00000100': (-dir.TURN_15, 1),
    '00000110': (-dir.TURN_25, 1),
    '00000010': (-dir.TURN_25, 1),
    # '00000111': (-dir.TURN_35, 1.1),  # this is bias to the left
    # '00000011': (-dir.TURN_35, 1.1),  # this is bias to the left
    # '00000001': (-dir.TURN_45, 1.2),  # this is bias to the left
    '00000111': (-dir.TURN_35, 1.165),
    '00000011': (-dir.TURN_35, 1.165),
    '00000001': (-dir.TURN_45, 1.25),

    '00010000': (dir.TURN_10, 1),  # this is bias to the left
    '00110000': (dir.TURN_15, 1),
    '00100000': (dir.TURN_15, 1),
    '01100000': (dir.TURN_25, 1),
    '01000000': (dir.TURN_25, 1),
    # '11100000': (dir.TURN_35, 1.15),
    # '11100000': (dir.TURN_35, 1.15),
    # '11000000': (dir.TURN_35, 1.15),
    # '10000000': (dir.TURN_45, 1.23)
    '11100000': (dir.TURN_35, 1.2),
    '11100000': (dir.TURN_35, 1.2),
    '11000000': (dir.TURN_35, 1.2),
    '10000000': (dir.TURN_45, 1.35)
}


def follow_line(num_objects: int = 4, object_angle_list=None, session_timestamp: str = 'tmpRun', speed: int = 50):
    speed_power = speed
    print(f'Robot speed will now be: {speed_power}')
    if object_angle_list is None:
        object_angle_list = ['HARD_RIGHT',
                             'HARD_RIGHT', 'HARD_RIGHT', 'HARD_RIGHT']
    print('Starting follow line')
    img_dic = {}
    anomaly_dic = {}
    for obj_n in range(1, num_objects + 1):
        img_dic[obj_n] = []
        anomaly_dic[obj_n] = 0
    curr_object = 0
    picture_progress_list = [1] * num_objects
    ir.setup_IR()
    motor.setup_motor()
    dir.setup_direction()
    vid.setup_vid()
    power.setup_power_management()
    vid.home_x_y()
    motor.setSpeed(speed_power, print_flag=True)
    time.sleep(0.5)
    motor.stop()
    dir.home()
    prev_exe_angle = 0  # last angle the car dir aim to. helps with "softer" directions change
    # if more then few sec the car out of track: stop the car/try to find it
    last_time_saw_line = time.time()
    possible_hard_turn = 0

    time.sleep(2)
    motor.forward()

    while True:
        ir_status_str = ir.check_above_line()

        if ir_status_str in actions_dir:
            exe_angle, speed_factor = actions_dir[ir_status_str]
            if ir_status_str == '11111111':
                # We encountered a stop line so we need to take a picture
                # Sending the number of the current picture of the current object to the image capture function
                prev_exe_angle = 0
                stop_res = stop_line(curr_object + 1, object_angle_list[curr_object],
                                     picture_progress_list[curr_object],
                                     session_timestamp, img_dic[curr_object + 1], anomaly_dic[curr_object + 1])
                if stop_res:
                    anomaly_dic[curr_object + 1] = 0
                else:
                    anomaly_dic[curr_object + 1] += 1
                vid.home_x_y()  # back from taking a picture we want to continue staight for a few seconds
                dir.home()
                motor.setSpeed(speed_power)
                motor.forward()
                # sleep for a few seconds so we won't stop again on the stopping line
                # this size may be change according to the road we build
                time.sleep(0.27)
                # adjust the sensativity of the ir sensor according to the current light

                # Incrementing the number of images for the current object
                picture_progress_list[curr_object] += 1
                # Updating the index of the next object to take an image for
                curr_object = (curr_object + 1) % num_objects
                last_time_saw_line = time.time()
                possible_hard_turn = 0
            elif (prev_exe_angle < 0 and exe_angle > 0) or (prev_exe_angle > 0 and exe_angle < 0):
                # in this case the turn was to "hard". might be a flake
                if DEBUG:
                    print(
                        f'DID NOT TURN NOW: curr angle={exe_angle}, prev angle={prev_exe_angle}')
                continue
            else:
                motor.setSpeed(int(speed_power * speed_factor))
                dir.turn_with_angle(exe_angle)
                if abs(exe_angle) >= dir.TURN_45:
                    possible_hard_turn += 1
                else:
                    possible_hard_turn = 0

                prev_exe_angle = exe_angle
                last_time_saw_line = time.time()
        elif 0 < possible_hard_turn < 5 and time.time() - last_time_saw_line > 0.5:
            # that looks like we are on a hard turn at the moment. we will try to adjust the car to the line
            if try_to_refind_the_line(prev_exe_angle):
                last_time_saw_line = time.time()
            possible_hard_turn = 0

        elif time.time() - last_time_saw_line > 3:
            # if the car more then few seconds out of the track: stop the car and go into zombie mode
            # but, before going into zombie mode, we try to find again the line by going back and forth
            if possible_hard_turn > 4 and try_to_refind_the_line(prev_exe_angle):
                last_time_saw_line = time.time()
                possible_hard_turn = 0
            else:
                motor.stop()
                dir.home()
                break  # go to zombie mode

        time.sleep(0.0000015)
        power.check_voltage()

    motor.stop()
    while True:  # TODO !!!! Zombie mode  !!!!
        vid.head_down()
        body = {
            "numObjects": num_objects,
            "command": 'stop',
            "error": "Robot can't find the line"
        }
        print('Asking API to kill robot_control thread')
        print(f'Sending request with data {body}')
        res = requests.post('http://localhost:5000/capture', json=body)
        time.sleep(5)


if __name__ == '__main__':
    follow_line()
