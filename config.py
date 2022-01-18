import os
import firebase_admin

API_REQUEST_DATETIME_FORMAT = '%d-%m-%YT%H-%M-%S'
STORAGE_BUCKET = 'mobilapse.appspot.com'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = f'{os.sep}home{os.sep}pi{os.sep}mobilapse-firebase-adminsdk.json'
# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'C:\\Users\\1912m\\mobilapse-firebase-key.json'

ROOT_CAPTURES_FOLDER_PATH = f'{os.sep}home{os.sep}pi{os.sep}cap_images{os.sep}'

FIREBASE_RT_DB_URL = 'https://mobilapse-default-rtdb.europe-west1.firebasedatabase.app/'

print('initializing FIREBASE')
default_app = firebase_admin.initialize_app(credential=None, options={'storageBucket': STORAGE_BUCKET,
                                                                      'databaseURL': FIREBASE_RT_DB_URL})
print('FIREBASE ready!')

CAMERA_PATH = f'{os.sep}dev{os.sep}v4l{os.sep}by-id{os.sep}usb-USB2.0_UVC_VGA_USB2.0_UVC_VGA-video-index'

DB_UPDATES = False