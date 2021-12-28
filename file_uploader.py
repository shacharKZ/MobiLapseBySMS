from firebase_admin import storage

IMAGE_CONTENT_TYPE = 'image/png'

bucket = storage.bucket()

def upload_image(video_name, video_path):
    blob = bucket.blob(f'robotImages/{video_name}')
    # logger.warning(f'Uploading {video_name} to captures/{video_name} from {video_path}')
    blob.upload_from_filename(video_path, content_type=IMAGE_CONTENT_TYPE)
    print(f'Finished uploading image to robotImages/{video_name} from path {video_path}')