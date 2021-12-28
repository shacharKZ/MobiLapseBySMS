import datetime
import multiprocessing
import os
import socket
import time

from firebase_admin import db
import requests
from flask import Flask, request
from flask_cors import CORS, cross_origin

from config import STORAGE_BUCKET, ROOT_CAPTURES_FOLDER_PATH, API_REQUEST_DATETIME_FORMAT, FIREBASE_RT_DB_URL
from filesystem_handler import create_capture_folders
from robot_control import follow_line

from stop import stop_all_robot_actions

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

ACTIVE_THREAD = None
tstamp = datetime.datetime(2021, 12, 7, 12, 19, 37)
# CURR_SESSION_TIMESTAMP = tstamp.strftime(API_REQUEST_DATETIME_FORMAT)
CURR_SESSION_TIMESTAMP = None


@app.route('/')
def hello_world():  # put application's code here
    print('RECEIVED REQ')
    return {'message': 'Hello World!'}, 200


@app.get('/capture')
@cross_origin()
def get_command_from_app_in_get():
    print('RECEIVED CAPTURE GET REQ')
    return {'message': 'all good from get capture!'}, 200


# TODO: upload each photo when it is captured, not when getting the order to finish capture
@app.post('/capture')
@cross_origin()
def get_command_from_app():
    global ACTIVE_THREAD, CURR_SESSION_TIMESTAMP
    data = request.get_json()
    print(data)
    num_objects = data.get('numObjects', None)
    object_angle_list: list[str] = data.get('objectAngleList', ['HARD_RIGHT', 'HARD_RIGHT', 'HARD_RIGHT'])
    if num_objects == None:
        num_objects = len(object_angle_list)
    if data['command'] == 'start':
        CURR_SESSION_TIMESTAMP = create_capture_folders(num_objects)
        ACTIVE_THREAD = multiprocessing.Process(target=follow_line,
                                                args=(num_objects, object_angle_list, CURR_SESSION_TIMESTAMP))
        ACTIVE_THREAD.start()
    elif data['command'] == 'stop':
        ACTIVE_THREAD.terminate()
        stop_all_robot_actions()
        # upload_new_captures(num_objects, CURR_SESSION_TIMESTAMP)
        send_convert_request_to_server(num_objects, CURR_SESSION_TIMESTAMP)
    message = "Finished processing " + data['command'] + " action"
    return {'message': message}, 200


def upload_new_captures(num_objects: int, session_timestamp: str):
    curr_upload_dir_name = ''
    for i in range(1, num_objects + 1):
        capture_dir_path = os.path.join(ROOT_CAPTURES_FOLDER_PATH, f'object{i}CaptureSession-{session_timestamp}')
        curr_upload_dir_name = f'object{i}CaptureSession-{session_timestamp}/'
        for file in os.listdir(capture_dir_path):
            full_path = os.path.join(ROOT_CAPTURES_FOLDER_PATH, f'object{i}CaptureSession-{session_timestamp}', file)
            print(f'Uploading file {file} from path {full_path}')
            print(f'Uploading to path robotImages/{curr_upload_dir_name}{file}')
            # upload_image(curr_upload_dir_name + file, full_path)


def send_convert_request_to_server(num_objects: int, session_timestamp: str):
    # Waiting for final upload to finish
    time.sleep(3)
    body = {
        "objects": num_objects,
        "datetime": session_timestamp
    }
    res = requests.post('https://mobiapicr-4hioxusaea-ew.a.run.app:443/convert', json=body)
    if res.status_code == 200:
        print('Conversion finished successfully!')
    else:
        print(f'An error has occurred, status code is {res.status_code}')


def write_api_address_to_db():
    print('getting DB reference')
    ref = db.reference('/')
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    local_ip = s.getsockname()[0]
    s.close()
    ref.set({"ROBOT_IP": local_ip,
             "lastUpdated": str(datetime.datetime.now())})
    print(f'added IP {local_ip} to firebase DB')


if __name__ == '__main__':
    print('API NOW RUNNING')
    write_api_address_to_db()
    app.run(debug=True, host='0.0.0.0')
    # get_command_from_app({'command': 'start', 'num_objects': 3})
