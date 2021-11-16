import cv2 # Import the OpenCV library
# import numpy as np # Import Numpy library
import motor
import car_dir as dir
import video_dir as vid
import time

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


class Position():
    # self._x = 0
    # self._y = 0

    def __init__(self, x, y) -> None:
        self._x = x
        self._y = y
        self._counter = 0

    def get_label_and_increase_counter(self) -> str:
        self._counter+=1
        return 'point(x='+str(self._x) + ', y=' + str(self._y)+') #' + str(self._counter)

    def __str__(self) -> str:
        return 'point(x='+str(self._x) + ', y=' + str(self._y)+') #' + str(self._counter)

p1 = Position(330, 20)
p2 = Position(250, 400)
p3 = Position(350, 250)

def take_a_pic(pic_label: str):
    ret, frame = cap.read()
    if not ret:
        return False
    # cv2.imshow("imshow", frame)
    # key=cv2.waitKey(30)
    print("##", pic_label)
    return cv2.imwrite('./cap_imgs/'+pic_label+'.png', frame)

def aim_and_take_a_photo(p: Position, label: str = ""):
    vid.set_dir(p._x, p._y)
    time.sleep(1)
    print(str(p))
    if label == "":
        take_a_pic(p.get_label_and_increase_counter())
    else:
        take_a_pic(label)


cap = cv2.VideoCapture(0)

if __name__ == '__main__':
    # test_cam()
    # motor.setup_motor()
    # dir.setup_direction()
    
    # grey_img = cv2.imread('~/img_home.pn', cv2.IMREAD_GRAYSCALE)

    # save image
    # status = cv2.imwrite('/home/img/python_grey.png',grey_img)
    
    vid.setup_vid()
    vid.home_x_y()
    time.sleep(1)
    # vid.set_dir(p1._x, p1._y)
    # take_a_pic("t1")
    aim_and_take_a_photo(p1)
    aim_and_take_a_photo(p1, 'f1')
    aim_and_take_a_photo(p2, 'f2')
    aim_and_take_a_photo(p3, 'f3')
    aim_and_take_a_photo(p1, 's1')
    aim_and_take_a_photo(p2, 's2')
    aim_and_take_a_photo(p3, 's3')

    # time.sleep(2)
    # vid.set_dir(p2._x, p2._y)
    # time.sleep(2)
    # vid.set_dir(p3._x, p3._y)
    # time.sleep(2)
    # vid.set_dir(p1._x, p1._y)

    # party()
    # vid.move_increase_y()
    vid.setup_vid()

    # motor.setSpeed(30)
    # vid.move_increase_y()
