# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'LoadingForm.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_frmLoading(object):
    def setupUi(self, frmLoading):
        frmLoading.setObjectName("frmLoading")
        frmLoading.setWindowModality(QtCore.Qt.ApplicationModal)
        frmLoading.resize(400, 58)
        frmLoading.setMinimumSize(QtCore.QSize(400, 58))
        frmLoading.setMaximumSize(QtCore.QSize(400, 58))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        frmLoading.setFont(font)
        self.vboxlayout = QtWidgets.QVBoxLayout(frmLoading)
        self.vboxlayout.setObjectName("vboxlayout")
        self.progressBar = QtWidgets.QProgressBar(frmLoading)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setAlignment(QtCore.Qt.AlignCenter)
        self.progressBar.setTextVisible(False)
        self.progressBar.setObjectName("progressBar")
        self.vboxlayout.addWidget(self.progressBar)
        self.lblStatus = QtWidgets.QLabel(frmLoading)
        self.lblStatus.setMinimumSize(QtCore.QSize(0, 20))
        self.lblStatus.setMaximumSize(QtCore.QSize(16777215, 20))
        self.lblStatus.setText("")
        self.lblStatus.setAlignment(QtCore.Qt.AlignCenter)
        self.lblStatus.setObjectName("lblStatus")
        self.vboxlayout.addWidget(self.lblStatus)

        self.retranslateUi(frmLoading)
        QtCore.QMetaObject.connectSlotsByName(frmLoading)

    def retranslateUi(self, frmLoading):
        _translate = QtCore.QCoreApplication.translate
        frmLoading.setWindowTitle(_translate("frmLoading", "Espere por favor..."))


