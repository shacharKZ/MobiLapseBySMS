# from cv2 import PROJ_SPHERICAL_EQRECT  # TODO what is that??
import motor
import car_dir as dir
import video_dir as vid
import QTR_8RC as ir
import time
from datetime import datetime
from capture_handler import take_a_pic
from anomaly_detection import check_anomaly_last_cap

# 0 to suppress, 1 to print debuggin messages
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
    detected_anomaly = check_anomaly_last_cap(prev_imgs, num_of_non_anomaly)
    if detected_anomaly:
        vid.make_gesture(1)  # TODO replace with REST CALL
    time.sleep(3)
    return detected_anomaly


actions_dir = {
    '00001000': (0, 1),  # staight forward. bias to the left
    '11111111': (0, 1),  # this is never been use (only for improving codeing)

    '00001100': (-dir.TURN_15, 1),
    '00000100': (-dir.TURN_15, 1),
    '00000110': (-dir.TURN_25, 1),
    '00000010': (-dir.TURN_25, 1),
    '00000111': (-dir.TURN_35, 1.165),  # this is bias to the left
    '00000011': (-dir.TURN_35, 1.165),  # this is bias to the left
    '00000001': (-dir.TURN_45, 1.25),  # this is bias to the left

    '00010000': (dir.TURN_10, 1),  # this is bias to the left
    '00110000': (dir.TURN_15, 1),
    '00100000': (dir.TURN_15, 1),
    '01100000': (dir.TURN_25, 1),
    '01000000': (dir.TURN_25, 1),
    '11100000': (dir.TURN_35, 1.2),
    '11000000': (dir.TURN_35, 1.2),
    '10000000': (dir.TURN_45, 1.35)
}


def test_dir1():  # TODO for debugging only
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
    img_dic = {}
    anomaly_dic = {}
    for obj_n in range(1, num_objects+1):
        img_dic[obj_n] = []
        anomaly_dic[obj_n] = 0
    curr_object = 0
    picture_progress_list = [1] * num_objects
    ir.setup_IR()
    motor.setup_motor()
    dir.setup_direction()
    vid.setup_vid()
    vid.home_x_y()
    motor.setSpeed(speed_power, print_flag=True)
    time.sleep(1)
    motor.stop()
    dir.home()
    prev_exe_angle = 0  # last angle the car dir aim to. helps with "softer" directions change
    count_const_not_on_line = 0  # if more then few sec the car out of track: stop the car

    time.sleep(4)
    motor.forward()

    while True:
        ir_status_str = ir.check_above_line()

        if ir_status_str in actions_dir:
            exe_angle, speed_factor = actions_dir[ir_status_str]
            if ir_status_str == '11111111':
                # We encountered a stop line so we need to take a picture
                # Sending the number of the current picture of the current object to the image capture function
                prev_exe_angle = 0
                stop_res = stop_line(curr_object + 1, object_angle_list[curr_object], picture_progress_list[curr_object],
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
                time.sleep(0.17)
                # adjust the sensativity of the ir sensor according to the current light
                ir.adjust_thershold()

                # Incrementing the number of images for the current object
                picture_progress_list[curr_object] += 1
                # Updating the index of the next object to take an image for
                curr_object = (curr_object + 1) % num_objects
            elif (prev_exe_angle < 0 and exe_angle > 0) or (prev_exe_angle > 0 and exe_angle < 0):
                # in this case the turn was to "hard". might be a flake
                if DEBUG:
                    print('DID NOT TURN NOW!')
                    print(
                        f'curr angle={exe_angle}, prev angle={prev_exe_angle}')
                count_const_not_on_line += 1
                continue
            else:
                motor.setSpeed(int(speed_power*speed_factor))
                dir.turn_with_angle(exe_angle)
                prev_exe_angle = exe_angle
                count_const_not_on_line = 0
        else:
            if DEBUG:
                print("DEBUG DIR EXE: ???", ir_status_str)
            count_const_not_on_line += 1
            # if the car more then few seconds out of the track: stop on goes into zombie mode
            if count_const_not_on_line > 432:
                motor.stop()
                dir.home()
                vid.make_gesture(4)
                break  # TODO !!!! Zombie mode  !!!!
        time.sleep(0.000002)

    motor.stop()
    while True:  # TODO !!!! Zombie mode  !!!!
        time.sleep(5)


if __name__ == '__main__':
    follow_line()
