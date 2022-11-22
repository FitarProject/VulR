from window.ui.import_burp_window import Ui_import_burp_window

from PyQt5.Qt import *


class Import_burp(QWidget, Ui_import_burp_window):
    # signal_dialog_close = pyqtSignal()
    signal_yes = pyqtSignal(str, str, str)

    def __init__(self):
        super().__init__()
        self.header = ''
        self.body = ''
        self.data_type = ''
        self.setupUi(self)

    def setupUi(self, import_burp_window):
        try:
            super().setupUi(import_burp_window)
            # self.setWindowIcon(QIcon('resource/image/urchin.png'))
            self.pushButton_yes.clicked.connect(self.pushButton_yes_event)
        except Exception as e:
            print("Exception in Import_burp --> " + "setupUi")

    # def closeEvent(self, event):
    #     super().closeEvent(event)
    #     self.signal_dialog_close.emit()

    def pushButton_yes_event(self):
        try:
            deal_status = self.deal_burp_data()
            if deal_status == 'success':
                self.signal_yes.emit(self.header, self.body, self.data_type)
                self.close()
            elif deal_status == 'empty':
                QMessageBox.warning(self, "提示", '识别区不能为空！', QMessageBox.Ok)
            elif deal_status == 'failed':
                QMessageBox.warning(self, "提示", '数据包格式有误！\n识别失败！', QMessageBox.Ok)
            elif deal_status == 'unknown':
                QMessageBox.warning(self, "提示", '暂不支持该请求方式！\n识别失败！', QMessageBox.Ok)
        except Exception as e:
            print("Exception in Import_burp --> " + "pushButton_yes_event")

    def deal_burp_data(self):
        try:
            burp_data_tmp = self.plainTextEdit_burp.toPlainText().split('\n')
            burp_data = []
            for data_tmp in burp_data_tmp:                              # 删除行尾的换行符
                burp_data.append(data_tmp.rstrip('\n'))
            if burp_data[0].startswith('GET'):                          # 判断是否为GET请求
                self.header = self.plainTextEdit_burp.toPlainText()
                self.data_type = 'GET'
                return 'success'
            elif burp_data[0].startswith('POST'):                       # 判断是否为POST请求
                self.data_type = 'POST'
                flag = -1
                for index, value in enumerate(burp_data[1:]):
                    if value.find(':', 1, 30) == -1:                    # 因为几乎所有header头部字段长度都不超过30，所以判断前30个字符中是否包含'：'
                        flag = index + 1
                        break
                for i in burp_data_tmp[:flag]:
                    self.header += i + '\n'
                for i in burp_data_tmp[flag:]:
                    if i.strip():
                        self.body += i + '\n'
                return 'success'
            elif burp_data[0].startswith('HEAD'):                       # 判断是否为其他请求方式
                return 'unknown'
            elif burp_data[0].startswith('PUT'):
                return 'unknown'
            elif burp_data[0].startswith('DELETE'):
                return 'unknown'
            elif burp_data[0].startswith('OPTIONS'):
                return 'unknown'
            elif burp_data[0].startswith('TRACE'):
                return 'unknown'
            elif burp_data[0].startswith('CONNECT'):
                return 'unknown'
            elif burp_data[0].startswith('PATCH'):
                return 'unknown'
            else:                                                       # 请求方式识别失败
                return 'failed'
        except Exception as e:
            print("Exception in Import_burp --> " + "deal_buurp_data", e)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    import_burp_window = QWidget()
    ui = Import_burp()
    ui.setupUi(import_burp_window)
    import_burp_window.show()
    sys.exit(app.exec_())

