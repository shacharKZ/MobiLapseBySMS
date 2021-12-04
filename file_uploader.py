from firebase_admin import storage

bucket = storage.bucket()

def upload_image(video_name, video_path):
    blob = bucket.blob(f'robotImages/{video_name}')
    # logger.warning(f'Uploading {video_name} to captures/{video_name} from {video_path}')
    blob.upload_from_filename(video_path, content_type=VIDEO_CONTENT_TYPE)