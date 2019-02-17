from PyQt5.QtWidgets import QDialog, QApplication
import gui.LoadingForm as LoadingUI


class LoadingDialog(QDialog, LoadingUI.Ui_frmLoading):
    def __init__(self):
        super(LoadingDialog, self).__init__()
        self.setupUi(self)
        self.lblStatus.setText('')

    def show_dialog(self, desc):
        self.lblStatus.setText(desc)
        self.show()
        QApplication.processEvents()

    def set_desc(self, desc):
        self.lblStatus.setText(desc)
        QApplication.processEvents()

    def set_range(self, val1, val2):
        self.progressBar.setRange(val1, val2)

    def set_value(self, val):
        self.progressBar.setValue(val)
        QApplication.processEvents()
