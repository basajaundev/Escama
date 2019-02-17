import os
import bz2
from time import time
import _pickle as pickle
import numpy as np
import cv2
from urllib import request as urlreq

import utils


def fetchSetImages(expcode, exp, ld):

    if not os.path.exists('./cache'):
        os.makedirs('./cache')

    files = os.listdir('./cache')

    name_dict = dict()

    if (expcode + '.imgs') not in files:  # if .images file doesnt exist
        exp.load_imgs(expcode)  # call card_set_json to get image URLs
        ld.set_desc('Descargando {0} cartas de {1}, puede tardar varios minutos.'.format(len(exp.uids), expcode))
        img_dict = create_image_dict(exp)
        dump_file_dict(expcode, '.imgs', img_dict)

    if (expcode + '.nms') not in files:
        exp.load_imgs(expcode)
        for i in range(len(exp.uids)):
            url = exp.imgurls[i]
            if url is not None:
                name_dict[exp.uids[i]] = exp.names[i]

        dump_file_dict(expcode, '.nms', name_dict)

    imgdictret = load_img_dict(expcode)
    namedictret = load_name_dict(expcode)

    return imgdictret, namedictret


def dump_file_dict(setcode, ext, _dict):
    with bz2.BZ2File(('cache/' + setcode + ext), 'wb') as wfile:
        pickle.dump(_dict, wfile, -1)
    wfile.close()


def create_image_dict(exp):
    img_dict = dict()
    cnt = 0
    t0 = time()
    for i in range(len(exp.uids)):  # fetch all card images from URLs
        url = exp.imgurls[i]
        if url is not None:
            request = urlreq.urlopen(url)
            img_array = np.asarray(bytearray(request.read()), dtype=np.uint8)
            img = cv2.imdecode(img_array, -1)   # CV_LOAD_IMAGE_UNCHANGED
            img_dict[exp.uids[i]] = img
            cnt += 1
    t1 = time()
    t = t1 - t0
    if utils.DEBUG:
        print('[Info] {0} cartas cargadas en {1:.1f} minutos...'.format(cnt, t / 60))

    return img_dict


def load_img_dict(setcode):
    if utils.DEBUG:
        print('[Info] {}.imgs archivo encontrado...'.format(setcode))

    with bz2.BZ2File(('cache/' + setcode + '.imgs'), 'rb') as rfile:  # read .images file from local disk
        imgdictret = pickle.load(rfile)
    rfile.close()
    return imgdictret


def load_name_dict(setcode):
    if utils.DEBUG:
        print('[Info] {}.nms archivo encontrado...'.format(setcode))

    with bz2.BZ2File(('cache/' + setcode + '.nms'), 'rb') as rfile:  # read .names file from local disk
        namedictret = pickle.load(rfile)
    rfile.close()
    return namedictret
