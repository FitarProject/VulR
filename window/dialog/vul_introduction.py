from window.ui.vul_introduction_window import Ui_vul_introduction_window

from PyQt5.Qt import *


class Vul_introduction(QWidget, Ui_vul_introduction_window):
    signal_close = pyqtSignal()
    signal_yes = pyqtSignal(str)

    def __init__(self, introduction: str):
        super().__init__()
        self.flag_is_changed = False
        self.introduction = introduction
        self.setupUi(self)

    def setupUi(self, vul_introduction_window):
        try:
            super().setupUi(vul_introduction_window)
            self.plainTextEdit_introduction.setPlainText(self.introduction)
            # self.setWindowIcon(QIcon('resource/image/urchin.png'))
            self.pushButton_yes.clicked.connect(self.pushButton_yes_event)
            self.pushButton_no.clicked.connect(self.pushButton_no_event)
        except Exception as e:
            print("Exception in Vul_introduction --> " + "setupUi")

    def closeEvent(self, event):
        if self.introduction != self.plainTextEdit_introduction.toPlainText():
            self.flag_is_changed = True
        if self.flag_is_changed:
            if QMessageBox.warning(self, "操作确认", '有未保存的修改，是否继续退出？', QMessageBox.Ok | QMessageBox.Cancel) == QMessageBox.Ok:
                self.flag_is_changed = False
                super().closeEvent(event)
                self.signal_close.emit()
            else:
                event.ignore()
        else:
            super().closeEvent(event)
            self.signal_close.emit()

    def pushButton_yes_event(self):
        try:
            self.introduction = self.plainTextEdit_introduction.toPlainText()
            self.signal_yes.emit(self.plainTextEdit_introduction.toPlainText())
            self.close()
        except Exception as e:
            print("Exception in Vul_introduction --> " + "pushButton_yes_event", e)

    def pushButton_no_event(self):
        try:
            self.close()
        except Exception as e:
            print("Exception in Vul_introduction --> " + "pushButton_no_event", e)


