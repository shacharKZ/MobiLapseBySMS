import os
import firebase_admin

API_REQUEST_DATETIME_FORMAT = '%d-%m-%YT%H-%M-%S'
STORAGE_BUCKET = 'mobilapse.appspot.com'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = f'{os.sep}home{os.sep}pi{os.sep}mobilapse-firebase-adminsdk.json'

ROOT_CAPTURES_FOLDER_PATH = f'{os.sep}home{os.sep}pi{os.sep}cap_images{os.sep}'

default_app = firebase_admin.initialize_app(credential=None, options={'storageBucket': STORAGE_BUCKET})