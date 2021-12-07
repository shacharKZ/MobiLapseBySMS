import os

from datetime import datetime

from config import ROOT_CAPTURES_FOLDER_PATH, API_REQUEST_DATETIME_FORMAT, CAMERA_PATH


def create_capture_folders(num_objects: int = 3):
    curr_session_timestamp = datetime.now()
    curr_session_timestamp_string = curr_session_timestamp.strftime(API_REQUEST_DATETIME_FORMAT)
    for i in range(1, num_objects + 1):
        os.mkdir(os.path.join(ROOT_CAPTURES_FOLDER_PATH, f'object{i}CaptureSession-{curr_session_timestamp_string}'))
    for dirpath, dirs, _ in os.walk(ROOT_CAPTURES_FOLDER_PATH):
        print(dirs)
    return curr_session_timestamp_string


def take_a_pic(curr_object_num: int, curr_picture_num: int, session_timestamp_string: str):
    pass

# def take_a_pic(curr_object_num: int, curr_picture_num: int, session_timestamp_string: str):
#     import cv2
#     cap = cv2.VideoCapture(0)
#     ret, frame = cap.read()
#     target_path = os.path.join(ROOT_CAPTURES_FOLDER_PATH,
#                                f'object{curr_object_num}CaptureSession-{session_timestamp_string}')
#     pic_label = f'{curr_picture_num}.png'
#     print(f"Picture attempt result: {ret}, Resulting picture name: {pic_label}")
#     if not ret:
#         return False
#     return cv2.imwrite(target_path + pic_label, frame)
