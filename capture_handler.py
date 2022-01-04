import os
import threading

import cv2

from datetime import datetime

from config import ROOT_CAPTURES_FOLDER_PATH, API_REQUEST_DATETIME_FORMAT, CAMERA_PATH
from file_uploader import upload_image


def take_a_pic(curr_object_num: int, curr_picture_num: int, session_timestamp_string: str):
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    target_dir = f'object{curr_object_num}CaptureSession-{session_timestamp_string}'
    target_path = os.path.join(ROOT_CAPTURES_FOLDER_PATH, target_dir)
    pic_label = f'{curr_picture_num}.png'
    print(f"Picture attempt result: {ret}, Resulting picture name: {pic_label}")
    if not ret:
        return False
    generated_image = cv2.imwrite(target_path + os.path.sep + pic_label, frame)
    x = threading.Thread(target=upload_image, args=(target_dir + os.path.sep + pic_label, target_path + os.path.sep + pic_label))
    # x = threading.Thread(target=upload_image, args=(target_dir + pic_label, target_path + '/' + pic_label))
    x.start()
    print('created thread', x.ident)
    # upload_image(target_dir + pic_label, target_path + os.path.sep + pic_label)
    return generated_image
