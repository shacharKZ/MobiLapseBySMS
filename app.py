import datetime
import multiprocessing
import os
import firebase_admin
from flask import Flask, request
from flask_cors import CORS, cross_origin

from config import STORAGE_BUCKET, ROOT_CAPTURES_FOLDER_PATH, API_REQUEST_DATETIME_FORMAT
from file_uploader import upload_image
from filesystem_handler import create_capture_folders
from robot_control import follow_line

# TODO: something in the more complex features is blocking API requests, need to figure out what

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

ACTIVE_THREAD = None
# tstamp = datetime.datetime(2021, 12, 7, 12, 19, 37)
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


@app.post('/capture')
@cross_origin()
def get_command_from_app():
    global ACTIVE_THREAD, CURR_SESSION_TIMESTAMP
    data = request.get_json()
    print(data)
    num_objects = data.get('numObjects', 3)
    # num_objects = args.get(['numObjects'], 3)
    if data['command'] == 'start':
        CURR_SESSION_TIMESTAMP = create_capture_folders(num_objects)
        # if args['command'] == 'start':
        ACTIVE_THREAD = multiprocessing.Process(target=follow_line, args=(num_objects, session_timestamp))
        ACTIVE_THREAD.start()
        follow_line(num_objects, CURR_SESSION_TIMESTAMP)
    elif data['command'] == 'stop':
        # elif args['command'] == 'stop':
        ACTIVE_THREAD.terminate()
        upload_new_captures(CURR_SESSION_TIMESTAMP)
        send_convert_request_to_server()
    return {'message': 'all good from capture posttt!'}, 200


def upload_new_captures(session_timestamp: str):
    curr_upload_dir_name = ''
    for dirpath, _, files in os.walk(ROOT_CAPTURES_FOLDER_PATH):
        curr_file_path = ''
        for file in files:
            print(os.path.join(dirpath, file))
            for i in range(1, 4):
                print(
                    f'Checking if object{i}CaptureSession-{session_timestamp} is in {str(os.path.join(dirpath, file))}')
                if f'object{i}CaptureSession-{session_timestamp}' in os.path.join(dirpath, file):
                    curr_upload_dir_name = f'object{i}CaptureSession-{session_timestamp}/'
                    break

            # print(os.path.join(dirpath, file))
            # print(file)
            upload_image(curr_upload_dir_name + file, os.path.join(dirpath, file))


def send_convert_request_to_server():
    pass


if __name__ == '__main__':
    print('API NOW RUNNING')
    app.run(debug=True, host='0.0.0.0')
    # get_command_from_app({'command': 'start', 'num_objects': 3})
