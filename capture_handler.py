import os

import cv2

from datetime import datetime

from config import ROOT_CAPTURES_FOLDER_PATH, API_REQUEST_DATETIME_FORMAT, CAMERA_PATH


def take_a_pic(curr_object_num: int, curr_picture_num: int, session_timestamp_string: str):
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    target_path = os.path.join(ROOT_CAPTURES_FOLDER_PATH,
                               f'object{curr_object_num}CaptureSession-{session_timestamp_string}')
    pic_label = f'{curr_picture_num}.png'
    print(f"Picture attempt result: {ret}, Resulting picture name: {pic_label}")
    if not ret:
        return False
    return cv2.imwrite(target_path + os.path.sep + pic_label, frame)
