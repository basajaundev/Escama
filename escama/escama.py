from __init__ import __version__
import sys
import cv2
import json

import qdarkstyle
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox

import utils
import gui.MainWindow as EscamaUI
from QWebcamThread import QWebcamThread
from cardexpjson import CardExpJson
from comparetoset import CompareToSet
from loadingWidget import LoadingDialog
from configWidget import ConfigDialog
from tableWidget import tableCards
from cardmarket import CardMarket


class EscamaApp(QMainWindow, EscamaUI.Ui_MainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.cmarket = CardMarket()

        self.table_Cards = tableCards(self, self.cmarket)

        self.setupUi(self)

        self.ld = LoadingDialog()

        self.cejson = CardExpJson(self.ld)
        self.cejson.load_json()

        self.load_escama()

        self.cd = None
        self.camera_src = None
        self.appToken = None
        self.appSecret = None
        self.accessToken = None
        self.accessSecret = None

        self.time_refresh = int(self.sboxSegs.value())
        self.timer = QTimer(self)
        self.isTimerOn = False

        # self.old_set = ''
        self.compare_set = ''

        self.blank = None

        self.lyTableCards.addWidget(self.table_Cards)

        self.card_back = cv2.imread('Cardback.png')
        self.blank = self.cvimg2qpixmap(self.card_back)
        self.lblCapCard.setPixmap(self.blank)

        self.cd = ConfigDialog(self)
        self.camera_src = self.cd.getCameraSrc()
        self.appToken = self.cd.getAppToken()
        self.appSecret = self.cd.getAppSecret()
        self.accessToken = self.cd.getAccessToken()
        self.accessSecret = self.cd.getAccessSecret()

        self.captured = QWebcamThread(self.lblCapCam, self.camera_src, self)

        self.cmbSets.activated[str].connect(self.switch_set)
        self.btnInit.clicked.connect(self.start_timer)
        self.timer.timeout.connect(lambda: self.read_match(self.compare_set, self.captured.getFrame()))
        self.btnConfig.clicked.connect(self.config_dialog)
        self.btnExit.clicked.connect(self.close)
        self.btnDelAllCards.clicked.connect(self.table_Cards.del_all_rows)
        self.btnDelSelectedRows.clicked.connect(self.table_Cards.del_sel_row)
        self.btnSendToCardmarket.clicked.connect(self.sellAllCards)

        self.captured.sig.connect(self.WebCamMissingDialog)
        self.captured.start()

        # self.gpbox_Cardmarket.setTitle('Cardmarket [{}]'.format(self.cmarket.get_username()))
        QApplication.processEvents()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Escama',
                                     'Realmente quieres salir de Escama?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def load_escama(self):
        self.cmbSets.addItem('Ninguno')
        self.ld.show()
        self.ld.set_desc('Cargando la GUI de Escama...')
        exps, utils.dict_exp = self.cejson.get_exps()
        self.ld.set_range(1, len(exps) - 1)
        i = 0
        for exp in exps:
            i += 1
            self.ld.set_value(((i + 1) / 100) * 100)
            self.cmbSets.addItem(exp)

        self.ld.close()

    def config_dialog(self):
        self.cd.show()

    def update_timer(self):
        self.lcdTimer.display(self.time_refresh % 60)

    def start_timer(self):
        if not self.isTimerOn:
            self.btnInit.setText('DETENER')
            self.time_refresh = int(self.sboxSegs.value())
            self.update_timer()
            self.timer.start(1000)
            self.isTimerOn = True
        else:
            self.timer.stop()
            self.lcdTimer.display(0)
            self.btnInit.setText('INICIAR')
            self.lblCapCard.setPixmap(self.blank)
            self.isTimerOn = False

    def read_match(self, c2s, cv_img):
        self.time_refresh -= 1
        self.update_timer()
        if self.time_refresh <= 0:
            self.time_refresh = int(self.sboxSegs.value())
            self.lblCapCard.setPixmap(self.blank)
            QApplication.processEvents()

            match_name, match_cvimage = c2s.compareimg(cv_img)
            match_image = self.cvimg2qpixmap(match_cvimage)
            self.lblCapCard.setPixmap(match_image)
            QApplication.processEvents()

            expname = utils.search_name_set(self.cmbSets.currentText())
            id_prod = self.cmarket.get_idproduct(match_name, expname)

            stock = self.cmarket.get_productstock(id_prod)
            if stock is None:
                stock = 0

            price = self.cmarket.get_productprice(id_prod)

            row_position = self.table_Cards.rowCount()
            self.table_Cards.insertRow(row_position)

            self.table_Cards.insert_card(row_position, match_name, expname, stock, price)

            self.table_Cards.resizeColumnsToContents()
            QApplication.processEvents()

    def switch_set(self, text):
        if text != 'Ninguno':
            self.ld.show_dialog('Cargando la expansion {}'.format(text))
            self.ld.set_range(0, 0)
            self.lblCapCard.setPixmap(self.blank)
            QApplication.processEvents()
            self.compare_set = CompareToSet(text, self.sboxCapAcc.value(), self.cejson, self.ld)
        # if not text == self.old_set:
        #     self.ld.show_dialog('Cargando la expansion {}'.format(text))
        #     self.lblCapCard.setPixmap(self.blank)
        #     QApplication.processEvents()
        #     start = self.cmbSets.findText('Ninguno', Qt.MatchFixedString)
        #     if start != -1:
        #         self.cmbSets.removeItem(start)
        #     self.compare_set = CompareToSet(text, self.sboxCapAcc.value(), self.cejson, self.ld)
        #     QApplication.processEvents()
        # self.old_set = text
        self.ld.close()
        QApplication.processEvents()

    @staticmethod
    def cvimg2qpixmap(cvimg):
        cvimg_rgb = cv2.cvtColor(cvimg, cv2.COLOR_BGR2RGB)
        qpix_img = QPixmap(
            QImage(cvimg_rgb, cvimg_rgb.shape[1], cvimg_rgb.shape[0], cvimg_rgb.strides[0], QImage.Format_RGB888))
        return qpix_img

    def WebCamMissingDialog(self):
        QMessageBox.question(self, 'Webcam Error',
                             u'Revisa que la camara esté conectada y reinicia la aplicación.',
                             QMessageBox.Ok, QMessageBox.Ok)

    def sellAllCards(self):
        cards = self.table_Cards.read_all_cards()
        for card in cards:
            idprod = self.cmarket.get_idproduct(card[1], card[2])
            data = json.dumps({
                'article': [{
                    'idProduct': idprod,
                    'idLanguage': card[3],
                    'comments': 'Added card with Escama {}'.format(__version__),
                    'count': card[10],
                    'price': card[9],
                    'condition': card[4],
                    'isFoil': card[5],
                    'isSigned': card[6],
                    'isAltered': card[7],
                    'isPlayset': 'false'
                }]})
            card_data = json.loads(data)
            self.cmarket.sell_card(card_data, card[8])
            print('[Info] Carta en venta -> {0}'.format(data))


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    form = EscamaApp()
    form.setWindowTitle(form.windowTitle() + ' {0} - [Cardmarket User: {1}]'
                        .format(__version__, form.cmarket.get_username()))
    form.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
