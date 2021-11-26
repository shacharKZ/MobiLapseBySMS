import cv2 # Import the OpenCV library
# import numpy as np # Import Numpy library
import motor
import car_dir as dir
import video_dir as vid
import QTR_8RC as ir
import tests
import time

wall_speed = 40  # when connected to the power source directly
battery_speed = 80  # when connected to batteries only
battery_slow_speed = 55  # when connected to batteries only

cap = cv2.VideoCapture(0) 


class Position():
    def __init__(self, x, y) -> None:
        self._x = x
        self._y = y
        self._counter = 0

    def get_label_and_increase_counter(self) -> str:
        self._counter+=1
        return 'point(x='+str(self._x) + ', y=' + str(self._y)+') #' + str(self._counter)

    def __str__(self) -> str:
        return 'point(x='+str(self._x) + ', y=' + str(self._y)+') #' + str(self._counter)


def take_a_pic(pic_label: str):
    ret, frame = cap.read()
    if not ret:
        return False
    # cv2.imshow("imshow", frame)
    # key=cv2.waitKey(30)
    return cv2.imwrite('./cap_imgs/'+pic_label+'.png', frame)


def aim_and_take_a_photo(p: Position, label: str = ""):
    vid.set_dir(p._x, p._y)
    time.sleep(1)
    if label == "":
        take_a_pic(p.get_label_and_increase_counter())
    else:
        take_a_pic(label)


def follow_line():
    motor.setup_motor()
    dir.setup_direction()
    vid.setup_vid()
    vid.home_x_y()
    motor.setSpeed(wall_speed)
    time.sleep(1)
    motor.stop()  # TODO
    dir.home()
    ir.setup_IR()
    action_needed = {
        '00000000': (print,"car don't see the line"),
        '00011000': (dir.home, None),
        '00111100': (dir.home, None),
        '11111111': (print, "all 8 sensors see the line"),

        '00001000': (dir.turn_right, dir.TURN_15),
        '00011100': (dir.turn_right, dir.TURN_15),
        '00001100': (dir.turn_right, dir.TURN_15),
        '00001110': (dir.turn_right, dir.TURN_25),
        '00000100': (dir.turn_right, dir.TURN_25),
        '00000110': (dir.turn_right, dir.TURN_35),
        '00001111': (dir.turn_right, dir.TURN_35),
        '00000010': (dir.turn_right, dir.TURN_45),
        '00000111': (dir.turn_right, dir.TURN_45),
        '00000011': (dir.turn_right, dir.TURN_60),
        '00000001': (dir.turn_right, dir.TURN_60),

        '00010000': (dir.turn_left, dir.TURN_15),
        '00111000': (dir.turn_left, dir.TURN_15),
        '00110000': (dir.turn_left, dir.TURN_15),
        '01110000': (dir.turn_left, dir.TURN_25),
        '00100000': (dir.turn_left, dir.TURN_25),
        '01100000': (dir.turn_left, dir.TURN_35),
        '11110000': (dir.turn_left, dir.TURN_35),
        '01000000': (dir.turn_left, dir.TURN_45),
        '11100000': (dir.turn_left, dir.TURN_45),
        '11000000': (dir.turn_left, dir.TURN_60),
        '10000000': (dir.turn_left, dir.TURN_60),
    }

    motor.forward()
    while True:
        ir.check_above_line()
        if ir.last_status_str in action_needed:
            action_to_exe, params = action_needed[ir.last_status_str]
            # print(action_to_exe, params)
            action_to_exe(params)
        else:
            print("car: ???", ir.last_status_str)
        time.sleep(0.05)

def test2():
    print("DEBUG: start test2 (func)")
    motor.setup_motor()
    dir.setup_direction()
    vid.setup_vid()
    vid.home_x_y()
    motor.setSpeed(battery_speed)
    time.sleep(1)
    dir.home()

    dir.turn_right()
    time.sleep(2)
    dir.turn_left()
    time.sleep(2)
    dir.turn_right()
    time.sleep(2)
    dir.home()
    time.sleep(2)
    motor.forward()
    time.sleep(2)
    motor.stop()
    time.sleep(1.5)
    motor.backward()
    time.sleep(4)
    motor.stop()
    time.sleep(3)

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
    follow_line()
