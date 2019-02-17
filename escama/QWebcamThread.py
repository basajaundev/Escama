from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QThread, pyqtSignal, Qt
import cv2


class QWebcamThread(QThread):
    sig = pyqtSignal()

    def WebCamMissing(self):
        # emitir señal al trigger del mensaje de error en escama.py
        self.sig.emit()

    def __del__(self):
        self.cap.release()
        self.wait()

    def __init__(self, imgwindow, cam_src, parent=None):
        super(QWebcamThread, self).__init__(parent=parent)
        self.imgwindow = imgwindow
        self.cam_src = cam_src
        self.done = False
        # on initialization, start reading from the webcam using OpenCV
        try:
            self.cap = cv2.VideoCapture(self.cam_src)
            self.ret, self.cvframe = self.cap.read()
        except:
            self.WebCamMissing()

    def getFrame(self):
        return self.cvframe

    def run(self):
        try:
            while not self.done:  # update Webcam image every loop
                cvimg = self.cvframe
                height, width, _ = cvimg.shape
                while width > 1000:  # resize webcam images that are far too high resolution for the UI to handle
                    new_width = int(width / 2)
                    new_height = int(height / 2)
                    cvimg = cv2.resize(cvimg, (new_width, new_height))  # , fx=1, fy=1)
                    height, width, _ = cvimg.shape
                cvimg_rgb = cv2.cvtColor(cvimg, cv2.COLOR_BGR2RGB)
                qpiximg = QPixmap(
                    QImage(cvimg_rgb, cvimg_rgb.shape[1], cvimg_rgb.shape[0], cvimg_rgb.strides[0], QImage.Format_RGB888))
                scale_img = qpiximg.scaled(self.imgwindow.size(), Qt.KeepAspectRatio, Qt.FastTransformation)
                self.imgwindow.setPixmap(scale_img)
                self.imgwindow.update()
                self.ret, self.cvframe = self.cap.read()
        except:
            # if exception, signal for error message
            self.WebCamMissing()
        # QApplication.processEvents()
