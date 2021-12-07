import os
from datetime import datetime

from config import API_REQUEST_DATETIME_FORMAT, ROOT_CAPTURES_FOLDER_PATH


def create_capture_folders(num_objects: int = 3):
    curr_session_timestamp = datetime.now()
    curr_session_timestamp_string = curr_session_timestamp.strftime(API_REQUEST_DATETIME_FORMAT)
    for i in range(1, num_objects + 1):
        path = os.path.join(ROOT_CAPTURES_FOLDER_PATH, f'object{i}CaptureSession-{curr_session_timestamp_string}')
        print(f'Creating folder: {path}')
        os.mkdir(path)
    return curr_session_timestamp_string
