import os
import threading
import cv2

from datetime import datetime

from config import ROOT_CAPTURES_FOLDER_PATH, API_REQUEST_DATETIME_FORMAT, CAMERA_PATH
from file_uploader import upload_image

max_img_num = 5+4  # 5 as for actual len and 4 for ".png"


def crop_and_adjust_img_to_img(prev_img_path, target_img_path) -> str:
    margin = 71
    if prev_img_path is None or prev_img_path == '':
        # first img just crop into its center
        ref_img = cv2.imread(target_img_path, cv2.IMREAD_COLOR)
        img_final_color = ref_img[margin: -margin,  margin:-margin]
        tmp_index = target_img_path.index('.png')
        crop_img_name = target_img_path[:tmp_index] + '_crop.png'
        cv2.imwrite(crop_img_name, img_final_color)
        return crop_img_name

    # loading the imgs in gray for the coming matching method
    img_to_crop = cv2.imread(target_img_path, cv2.IMREAD_GRAYSCALE)
    ref_img = cv2.imread(prev_img_path, cv2.IMREAD_GRAYSCALE)

    height, weight = ref_img.shape
    # finding the best location which the imgs are corresponding together
    res_locs = cv2.matchTemplate(img_to_crop, ref_img, cv2.TM_CCOEFF)
    # min_val, max_val, min_loc, top_left = cv2.minMaxLoc(res_locs)
    top_left = cv2.minMaxLoc(res_locs)[-1]

    # save a copy of the img (with color) with crop according to the location we found
    tmp_index = target_img_path.index('.png')
    img_to_crop_color = cv2.imread(target_img_path, cv2.IMREAD_COLOR)
    img_final_color = img_to_crop_color[top_left[1]:top_left[1]+height, top_left[0]: top_left[0]+weight]
    crop_img_name = target_img_path[:tmp_index] + '_crop.png'
    cv2.imwrite(crop_img_name, img_final_color)
    return crop_img_name


def take_a_pic(curr_object_num: int, curr_picture_num: int, session_timestamp_string: str, prev_imgs: list):
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    target_dir = f'object{curr_object_num}CaptureSession-{session_timestamp_string}'
    target_path = os.path.join(ROOT_CAPTURES_FOLDER_PATH, target_dir)
    pic_label = f'{curr_picture_num}.png'
    pic_label = ('0' * (max_img_num - len(pic_label))) + pic_label
    print(
        f"Picture attempt result: {ret}, Resulting picture name: {pic_label}")
    if not ret:
        return False
    img_path = target_path + os.path.sep + pic_label
    generated_res = cv2.imwrite(img_path, frame)

    if len(prev_imgs) == 0:
        crop_img_path = crop_and_adjust_img_to_img(None, img_path)
    else:
        crop_img_path = crop_and_adjust_img_to_img(prev_imgs[-1], img_path)
    prev_imgs.append(crop_img_path)

    x = threading.Thread(target=upload_image, args=(
        target_dir + os.path.sep + pic_label, crop_img_path))
    # x = threading.Thread(target=upload_image, args=(target_dir + pic_label, target_path + '/' + pic_label))
    x.start()
    print('created thread', x.ident)
    # upload_image(target_dir + pic_label, target_path + os.path.sep + pic_label)
    return crop_img_path
