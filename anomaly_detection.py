import datetime

import numpy as np
import cv2
# from firebase_admin import db

from db_handler import update_anomaly_for_object_in_db


def pixelate_img(img, window=33, normalize=False):
    n, m = img.shape
    n, m = n - n % window, m - m % window
    pix_img = np.zeros((n, m, 3))
    for x in range(0, n, window):
        for y in range(0, m, window):
            pix_img[x:x + window, y:y + window] = img[x:x +
                                                      window, y:y + window].mean(axis=(0, 1))

    if normalize:
        rng = pix_img.max() - pix_img.min()
        min_pix = pix_img.min()
        pix_img = (pix_img - min_pix) * 255 / rng

    pix_img = pix_img.astype(int)
    return np.asarray(pix_img).flatten()


def diff_pix(flat_pix1, flat_pix2, threshold=80) -> int:
    pix_diff = flat_pix1 - flat_pix2

    curr_diff = 0
    for val in pix_diff:
        if abs(val) > threshold:
            curr_diff += 1
    return max(curr_diff, 1000)


def check_anomaly_last_cap(imgs: list, num_of_non_anomaly, diff_rate=7.7, curr_object_num=0) -> bool:
    number_of_prev_imgs = 5
    if len(imgs) < number_of_prev_imgs or num_of_non_anomaly < number_of_prev_imgs:
        print(f'Anomaly detection: skip this time since comparing last {number_of_prev_imgs} images but only had '
              f'{num_of_non_anomaly} images after starting/last detection')
        return False
    relevant_pixs = [pixelate_img(cv2.imread(c_img, cv2.IMREAD_GRAYSCALE))
                     for c_img in imgs[-number_of_prev_imgs:]]

    sum_diff = 0
    i = 0
    while i < len(relevant_pixs) - 2:
        sum_diff += diff_pix(relevant_pixs[i], relevant_pixs[i + 1])
        i += 1

    avg_diff = sum_diff // (number_of_prev_imgs - 2)
    last_diff = diff_pix(relevant_pixs[-2], relevant_pixs[-1])
    print(
        f'Anomaly detection: avg pixelate diff: {avg_diff}, last pixelate diff: {last_diff}')

    if last_diff > avg_diff * diff_rate:
        update_anomaly_for_object_in_db(curr_object_num)
        return True

    return False
