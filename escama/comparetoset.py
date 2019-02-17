import numpy as np
import cv2
import math
from time import time

from PyQt5.QtWidgets import QApplication

from fetchSetImages import fetchSetImages
from processSetImages import processSetImages
import utils


class CompareToSet:
    def __init__(self, setcode, cap_acc, cejson, ld):
        # User Provides the SetCode
        # Get name dictionary and image dictionary from fetchSetImages
        self.imgdict, self.namedict = fetchSetImages(setcode, cejson, ld)
        # Get keypoints dictionaries and SIFT object from processSetImages
        self.keypdict, self.desdict, self.imgdict2g, self.sift = processSetImages(self.imgdict, cap_acc)

        ##Matcher Steup
        # create OpenCV keypoint matcher object
        self.bf = cv2.BFMatcher()

        ld.set_desc('Expansión {} lista para usar...'.format(setcode))
        QApplication.processEvents()
        if utils.DEBUG:
            print('[Info] Expansión {} lista para usar...'.format(setcode))

    # Compare an image to the card images and identify one as a match
    def compareimg(self, camimg):
        # accepts the webcam image as input
        t0 = time()
        try:
            height, width, _ = camimg.shape
            while width > 1000:
                new_width = int(width / 2)
                new_height = int(height / 2)
                camimg = cv2.resize(camimg, (new_width, new_height))
                height, width, _ = camimg.shape
            camimg2g = cv2.cvtColor(camimg, cv2.COLOR_BGR2GRAY)
        except:
            raise IOError('Cannot properly process input image')

        # compute keypoints for the webcam image
        kpr, desr = self.sift.detectAndCompute(camimg2g, None)

        printsimages = []
        printsimages2g = []
        printskp = []
        printsdes = []
        printsmatches = []
        printsmatcheslen = []
        printsnames = []

        # Loop through images to compare each one
        for key in self.imgdict:
            printsimages.append(self.imgdict[key])
            printsimages2g.append(self.imgdict2g[key])
            kp = self.keypdict[key]
            des = self.desdict[key]
            printskp.append(kp)
            printsdes.append(des)
            printsnames.append(self.namedict[key])

            rawmatches = self.bf.knnMatch(desr, des, k=2)  # find 2 nearest negihbor keypoint matches
            matches = []
            for m, n in rawmatches:
                if m.distance < 0.75 * n.distance:  # use ratio test to determine if match is successful
                    matches.append([m])
            printsmatches.append(matches)
            printsmatcheslen.append(len(matches))

        ## Find Best Match and Display
        # for x in range(3):
        #     best_match = np.argmax(printsmatcheslen)  # identify correct card by number of successful matches
        #     print("Match", (x + 1), ',', printsnames[best_match], ':', 'with', printsmatcheslen[best_match],
        #           'feature matches')
        #
        #     if x == 0:
        #         best_match_name = printsnames[best_match]
        #         best_match_img = printsimages[best_match]
        #
        #     printsmatcheslen[best_match] = -math.inf

        best_match = np.argmax(printsmatcheslen)  # identify correct card by number of successful matches
        t1 = time()
        t = t1 - t0
        print('[Info] Coincidencia: "{0}" con {1} coincidencias en {2} milisegundos'
              .format(printsnames[best_match], printsmatcheslen[best_match], int(round(t * 1000))))

        best_match_name = printsnames[best_match]
        best_match_img = printsimages[best_match]

        printsmatcheslen[best_match] = -math.inf

        best_match_img = cv2.resize(best_match_img, (223, 311))
        return best_match_name, best_match_img  # return the name and image of the identified card
