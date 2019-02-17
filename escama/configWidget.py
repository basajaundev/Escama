import configparser

from PyQt5.QtWidgets import QDialog, QMessageBox
import gui.ConfigForm as ConfigUI


class ConfigDialog(QDialog, ConfigUI.Ui_frmConfig):

    def __init__(self, parent=None):
        super(ConfigDialog, self).__init__(parent)
        self.setupUi(self)

        self._camera_src = None
        self._appToken = None
        self._appSecret = None
        self._accessToken = None
        self._accessSecret = None

        self.loadConf()
        self.txtCamera.setText(self._camera_src)
        self.txtAppToken.setText(self._appToken)
        self.txtAppSecret.setText(self._appSecret)
        self.txtAccessToken.setText(self._accessToken)
        self.txtAccessSecret.setText(self._accessSecret)

        self.btnSave.clicked.connect(self.saveConf)
        self.btnCancel.clicked.connect(self.close)

    def showDialog(self):
        self.show()

    def loadConf(self):
        escama_conf = configparser.ConfigParser()
        escama_conf.read('escama.conf')
        self._camera_src = escama_conf.get('EscamaConf', 'camera')
        self._appToken = escama_conf.get('MKMConf', 'appToken')
        self._appSecret = escama_conf.get('MKMConf', 'appSecret')
        self._accessToken = escama_conf.get('MKMConf', 'accessToken')
        self._accessSecret = escama_conf.get('MKMConf', 'accessSecret')

    def saveConf(self):
        escama_conf = configparser.ConfigParser()
        escama_conf.read('escama.conf')
        escama_conf['EscamaConf']['camera'] = self.txtCamera.text()
        escama_conf['MKMConf']['appToken'] = self.txtAppToken.text()
        escama_conf['MKMConf']['appSecret'] = self.txtAppSecret.text()
        escama_conf['MKMConf']['accessToken'] = self.txtAccessToken.text()
        escama_conf['MKMConf']['accessSecret'] = self.txtAccessSecret.text()
        with open('escama.conf', 'w') as f:
            escama_conf.write(f)
        f.close()
        QMessageBox.warning(self, 'Configuración Escama',
                            'Tienes que reiniciar la aplicación para aplicar los nuevos valores.',
                            QMessageBox.Ok, QMessageBox.Ok)
        self.close()

    def getCameraSrc(self):
        return self._camera_src

    def setCameraSrc(self, val):
        self._camera_src = val

    def getAppToken(self):
        return self._appToken

    def setAppToken(self, val):
        self._appToken = val

    def getAppSecret(self):
        return self._appSecret

    def setAppSecret(self, val):
        self._appSecret = val

    def getAccessToken(self):
        return self._accessToken

    def setAccessToken(self, val):
        self._accessToken = val

    def getAccessSecret(self):
        return self._accessSecret

    def setAccessSecret(self, val):
        self._accessSecret = val
