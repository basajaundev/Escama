import cv2
from time import time

import utils


def processSetImages(img_dict, cap_acc):
    global surf

    if utils.DEBUG:
        print('[Info] Usando una precisión de captura de {}'.format(cap_acc))

    try:
        surf = cv2.xfeatures2d.SURF_create(cap_acc)
    except:
        print("[Error] Invalid feature type; should be either 'SURF'")

    keyp_dict = dict()
    des_dict = dict()
    img_dict2g = dict()

    if utils.DEBUG:
        print('[Info] Procesando las cartas para el reconocimiento')

    t0 = time()
    for key in img_dict:  # calculate keypoints for all card images in the set
        img2g = cv2.cvtColor(img_dict[key], cv2.COLOR_BGR2GRAY)
        img_dict2g[key] = img2g
        kp, des = surf.detectAndCompute(img2g, None)
        keyp_dict[key] = kp
        des_dict[key] = des
    # pass along everything including the sift object
    t1 = time()
    t = t1 - t0
    if utils.DEBUG:
        print('[Info] Terminado el procesamiento de cartas en {} segundos...'.format(int(t)))

    return keyp_dict, des_dict, img_dict2g, surf
