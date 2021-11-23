import cv2 # Import the OpenCV library
# import numpy as np # Import Numpy library
import motor
import car_dir as dir
import video_dir as vid
import time

wall_speed = 40  # when connected to the power source directly
battery_speed = 80  # when connected to batteries only
battery_slow_speed = 55  # when connected to batteries only

# cap = cv2.VideoCapture(0)  # TODO

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

    vid.set_dir(400, 400)
    time.sleep(1)
    vid.set_dir(370, 300)
    time.sleep(1)
    for (x,y) in [(350, 250), (500, 200), (270, 300), (370, 300), (370, 250), (320, 380), (330, 500), (400, 400), (255, 350), (330, 330)]:
        vid.set_dir(x, y)
        time.sleep(1)

    time.sleep(2)
    vid.set_dir(400, 400)
    time.sleep(1)
    vid.set_dir(370, 300)
    time.sleep(1)
    dir.turn_left()
    motor.forward()
    for x in range(250, 550, 10):
        vid.set_dir(x, 220)
        time.sleep(0.5)

    dir.turn_right()
    for x in range(550, 250, -10):
        vid.set_dir(x, 260)
        time.sleep(0.5)

    motor.stop()
    vid.home_x_y()
    time.sleep(2)
    motor.setSpeed(battery_slow_speed)
    counter = 0
    for _ in range(2):
        for (x,y) in [(350, 250), (500, 200), (270, 300), (370, 250), (320, 380), (330, 500), (330, 450), (400, 400), (255, 350), (330, 330)]:
            vid.set_dir(x, y)
            time.sleep(0.5)
            counter+=1
            if counter%4 == 1:
                motor.forward()
            elif counter%4 == 3:
                motor.backward()
            
            # time.sleep(0.5)
            if counter%5 == 1:
                dir.turn_right()
            elif counter%5 == 2:
                dir.turn_left()
            elif counter%3 == 1:
                dir.home()
            time.sleep(0.7)
            motor.stop()
    
    motor.stop()
    time.sleep(1)
    dir.home()
    vid.home_x_y()

def test3():
    vid.setup_vid()
    vid.home_x_y()
    for y in range(200, 400, 40):
        for x in range(250, 550, 10):
            vid.set_dir(x, y)
            time.sleep(0.5)
        for x in range(550, 250, -10):
            vid.set_dir(x, y+20)
            time.sleep(0.5)
    
    for y in range(400, 200, -40):
        for x in range(250, 550, 10):
            vid.set_dir(x, y)
            time.sleep(0.5)
        for x in range(550, 250, -10):
            vid.set_dir(x, y-20)
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
        motor.setSpeed(50)
        motor.forward()
        aim_and_take_a_photo(p1)
        time.sleep(2)
        aim_and_take_a_photo(p2)
        motor.stop()
        motor.setSpeed(65)
        dir.turn_right()
        motor.backward()
        time.sleep(2)
        aim_and_take_a_photo(p3)
        motor.stop()
        dir.home()
        motor.setSpeed(50)
        motor.forward()
        aim_and_take_a_photo(p4)
        motor.stop()


if __name__ == '__main__':
    # p1 = Position(330, 20)
    # p2 = Position(250, 400)
    # p3 = Position(350, 250)
    # p_list = [Position(350, 250), Position(350, 300), Position(450, 300), Position(450, 200), \
    #     Position(320, 300), Position(500, 300), Position(500, 200), Position(300, 300)]
    # # test_everything(p_list)
    # test_showoff()

    test2()
    time.sleep(5)
    test3()
