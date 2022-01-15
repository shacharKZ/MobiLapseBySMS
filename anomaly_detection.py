import os
import numpy as np
import cv2


def pixelate_rgb(img, window=32, normalize=False):
    n, m = img.shape
    n, m = n - n % window, m - m % window
    pix_img = np.zeros((n, m, 3))
    for x in range(0, n, window):
        for y in range(0, m, window):
            pix_img[x:x+window, y:y+window] = img[x:x+window, y:y+window].mean(axis=(0, 1))

    if normalize:
        rng = pix_img.max()-pix_img.min()
        min_pix = pix_img.min()
        pix_img = (pix_img-min_pix)*255/rng

    pix_img = pix_img.astype(int)
    return np.asarray(pix_img).flatten()


def diff_pix(flat_pix1, flat_pix2, threshold=100) -> int:
    pix_diff = flat_pix1 - flat_pix2

    curr_diff = 0
    for val in pix_diff:
        if val > threshold:
            curr_diff += 1
    return max(curr_diff, 100)


def check_anomaly_last_cap(imgs: [str], diff_rate=1.3) -> bool:
    number_of_prev_imgs = 4
    if len(imgs) < number_of_prev_imgs:
        return False
    relevant_pixs = [pixelate_rgb(cv2.imread(c_img, cv2.IMREAD_GRAYSCALE)) for c_img in imgs[-number_of_prev_imgs:]]

    sum_diff = 0
    prev_img = relevant_pixs[0]
    for curr_img in relevant_pixs[1:-1]:
        sum_diff += diff_pix(prev_img, curr_img)
        prev_img = curr_img

    avg_diff = sum_diff/(number_of_prev_imgs-1)
    print(f'&&&&&&&&&&&&&&& AVG DIFF IS: {avg_diff}')
    last_diff = diff_pix(prev_img, relevant_pixs[-1])
    print(f'&&&&&&&&&&&&&&& LAST DIFF IS: {last_diff}')

    if last_diff > avg_diff*diff_rate or last_diff < avg_diff/diff_rate:  # TODO
        return True

    return False

