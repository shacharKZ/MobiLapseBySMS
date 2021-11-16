import cv2 # Import the OpenCV library
# import numpy as np # Import Numpy library
import motor
import car_dir as dir
import video_dir as vid
import time

cap = cv2.VideoCapture(0)

def party():
    for t in range(3):
        vid.home_x_y()
        print("start cycle num", t)
        time.sleep(2)
        for i in range(10):
            vid.move_increase_x()
            vid.move_increase_y()
            time.sleep(0.5)
        for i in range(20):
            vid.move_decrease_x()
            vid.move_decrease_y()
            time.sleep(0.5)

def test_everything(p_list):
    print("DEBUG: start testing everything!")
    motor.setup_motor()
    dir.setup_direction()
    vid.setup_vid()
    vid.home_x_y()
    time.sleep(1)
    dir.home()
    motor.forward()

    flag = True
    for i in range(1, 4):
        motor.setSpeed(22*i)
        for p in p_list:
            if flag:
                dir.turn_left()
            else:
                dir.turn_right()
            flag = not flag
            aim_and_take_a_photo(p)
    
    dir.home()
    motor.stop()

def test_showoff():
    print("DEBUG: start testing showoff!\ncount to 10 and run!")
    time.sleep(10)
    p1 = Position(350, 250)
    p2 = Position(350, 300)
    p3 = Position(450, 300)
    p4 = Position(450, 200)
    motor.setup_motor()
    dir.setup_direction()
    vid.setup_vid()
    vid.home_x_y()
    time.sleep(1)
    dir.home()
    motor.forward()

    for i in range(2):
        motor.setSpeed(20)
        motor.forward()
        aim_and_take_a_photo(p1)
        time.sleep(2)
        aim_and_take_a_photo(p2)
        motor.stop()
        motor.setSpeed(15)
        dir.turn_right()
        motor.backward()
        time.sleep(2)
        aim_and_take_a_photo(p3)
        motor.stop()
        dir.home()
        motor.setSpeed(30)
        motor.forward()
        aim_and_take_a_photo(p4)
        motor.stop()



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

if __name__ == '__main__':
    # p1 = Position(330, 20)
    # p2 = Position(250, 400)
    # p3 = Position(350, 250)
    p_list = [Position(350, 250), Position(350, 300), Position(450, 300), Position(450, 200), \
        Position(320, 300), Position(500, 300), Position(500, 200), Position(300, 300)]
    # test_everything(p_list)
    test_showoff()
