# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ConfigForm.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets

class Ui_frmConfig(object):
    def setupUi(self, frmConfig):
        frmConfig.setObjectName("frmConfig")
        frmConfig.resize(370, 206)
        frmConfig.setMinimumSize(QtCore.QSize(370, 206))
        frmConfig.setMaximumSize(QtCore.QSize(370, 206))
        frmConfig.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(frmConfig)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(frmConfig)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.formLayout = QtWidgets.QFormLayout(self.tab)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.tab)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.txtCamera = QtWidgets.QLineEdit(self.tab)
        self.txtCamera.setObjectName("txtCamera")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.txtCamera)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.formLayout_2 = QtWidgets.QFormLayout(self.tab_2)
        self.formLayout_2.setObjectName("formLayout_2")
        self.txtAppToken = QtWidgets.QLineEdit(self.tab_2)
        self.txtAppToken.setObjectName("txtAppToken")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.txtAppToken)
        self.txtAppSecret = QtWidgets.QLineEdit(self.tab_2)
        self.txtAppSecret.setEchoMode(QtWidgets.QLineEdit.Password)
        self.txtAppSecret.setObjectName("txtAppSecret")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.txtAppSecret)
        self.label_4 = QtWidgets.QLabel(self.tab_2)
        self.label_4.setObjectName("label_4")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.txtAccessToken = QtWidgets.QLineEdit(self.tab_2)
        self.txtAccessToken.setObjectName("txtAccessToken")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.txtAccessToken)
        self.label_5 = QtWidgets.QLabel(self.tab_2)
        self.label_5.setObjectName("label_5")
        self.formLayout_2.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.txtAccessSecret = QtWidgets.QLineEdit(self.tab_2)
        self.txtAccessSecret.setEchoMode(QtWidgets.QLineEdit.Password)
        self.txtAccessSecret.setObjectName("txtAccessSecret")
        self.formLayout_2.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.txtAccessSecret)
        self.label_2 = QtWidgets.QLabel(self.tab_2)
        self.label_2.setObjectName("label_2")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.label_3 = QtWidgets.QLabel(self.tab_2)
        self.label_3.setObjectName("label_3")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.tabWidget.addTab(self.tab_2, "")
        self.verticalLayout.addWidget(self.tabWidget)
        self.horizontalWidget = QtWidgets.QWidget(frmConfig)
        self.horizontalWidget.setObjectName("horizontalWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalWidget)
        self.horizontalLayout.setContentsMargins(1, 1, 1, 1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btnSave = QtWidgets.QPushButton(self.horizontalWidget)
        self.btnSave.setObjectName("btnSave")
        self.horizontalLayout.addWidget(self.btnSave)
        self.btnCancel = QtWidgets.QPushButton(self.horizontalWidget)
        self.btnCancel.setObjectName("btnCancel")
        self.horizontalLayout.addWidget(self.btnCancel)
        self.verticalLayout.addWidget(self.horizontalWidget, 0, QtCore.Qt.AlignRight)

        self.retranslateUi(frmConfig)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(frmConfig)

    def retranslateUi(self, frmConfig):
        _translate = QtCore.QCoreApplication.translate
        frmConfig.setWindowTitle(_translate("frmConfig", "Configuración"))
        self.label.setText(_translate("frmConfig", "Camara IP:"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("frmConfig", "Escama"))
        self.label_4.setText(_translate("frmConfig", "Access Token:"))
        self.label_5.setText(_translate("frmConfig", "Access Token Secret:"))
        self.label_2.setText(_translate("frmConfig", "App Token:"))
        self.label_3.setText(_translate("frmConfig", "App Secret:"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("frmConfig", "Cardmarket"))
        self.btnSave.setText(_translate("frmConfig", "Guardar"))
        self.btnCancel.setText(_translate("frmConfig", "Cancelar"))

