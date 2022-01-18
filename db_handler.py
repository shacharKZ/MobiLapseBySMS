import socket
import datetime

from firebase_admin import db


def reset_db_state_before_robot_start():
    """
    Resets the DB before the robot begins running
    The function will write the new robot IP to the DB
    The function will clear errors from the previous runs
    The function will reset the robot state so the app can control it
    The app will clear previous anomalies
    """
    write_api_address_to_db()
    update_robot_state_in_db(0)
    clear_robot_error_in_db()
    reset_anomalies()


def reset_anomalies():
    print('getting DB reference')
    ref = db.reference('/AnomalyData')
    snapshot = ref.order_by_key().get()
    for index, value in enumerate(snapshot):
        if value is None:
            continue
        print(f'index: {index}, value: {value}')
        ref.update({f'{index}/Detected': False,
                    f'{index}/lastUpdated': str(datetime.datetime.now())})


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


def clear_robot_error_in_db():
    print('getting DB reference')
    ref = db.reference(f'/RobotError')
    data = {"Detected": False,
            "Error": '',
            "lastUpdated": str(datetime.datetime.now())}
    ref.set(data)
    print(f'Update error data: {data}')
