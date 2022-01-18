import socket
import datetime

from firebase_admin import db


def write_api_address_to_db():
    print('getting DB reference')
    ref = db.reference('/RobotData')
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    local_ip = s.getsockname()[0]
    s.close()
    ref.set({"ROBOT_IP": local_ip,
             "lastUpdated": str(datetime.datetime.now())})
    print(f'added IP {local_ip} to firebase DB')


def update_robot_state_in_db(state: int):
    print('getting DB reference')
    ref = db.reference('/ROBOT_STATE')
    ref.set(state)
    print(f'Set robot state as {state} in DB')


def update_anomaly_for_object_in_db(curr_object_num: int):
    print('getting DB reference')
    ref = db.reference(f'/AnomalyData/{curr_object_num + 1}')
    data = {"Detected": True,
            "lastUpdated": str(datetime.datetime.now())}
    ref.set(data)
    print(f'Update anomaly data: {data}')


def write_robot_error_to_db(error_message: str):
    print('getting DB reference')
    ref = db.reference(f'/RobotError')
    data = {"Detected": True,
            "Error": error_message,
            "lastUpdated": str(datetime.datetime.now())}
    ref.set(data)
    print(f'Update error data: {data}')
