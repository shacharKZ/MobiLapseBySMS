import multiprocessing
import os

from flask import Flask, request
from flask_cors import CORS, cross_origin

from capture_handler import create_capture_folders
from config import STORAGE_BUCKET, ROOT_CAPTURES_FOLDER_PATH
from file_uploader import upload_image
from robot_control import follow_line

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
default_app = firebase_admin.initialize_app(credential=None, options={'storageBucket': STORAGE_BUCKET})

ACTIVE_THREAD = None


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.get('/capture')
@cross_origin()
def get_command_from_app_in_get():
    return {'message': 'all good from get capture!'}, 200


@app.post('/capture')
@cross_origin()
def get_command_from_app():
    global ACTIVE_THREAD
    data = request.get_json()
    print(data)
    num_objects = data.get(['numObjects'], 3)
    session_timestamp = create_capture_folders(num_objects)
    if data['command'] == 'start':
        ACTIVE_THREAD = multiprocessing.Process(target=follow_line, args=(num_objects, session_timestamp))
        ACTIVE_THREAD.start()
    elif data['command'] == 'stop':
        ACTIVE_THREAD.terminate()
        upload_new_captures(session_timestamp)
        send_convert_request_to_server()
    return {'message': 'all good from capture posttt!'}, 200


def upload_new_captures(session_timestamp: str):
    for dirpath, _, files in os.walk(ROOT_CAPTURES_FOLDER_PATH):
        for file in files:
            print(os.path.join(dirpath, file))
            print(file)
            # upload_image(file, os.path.join(dirpath, file))


def send_convert_request_to_server():
    pass


if __name__ == '__main__':
    app.run(debug=True)
