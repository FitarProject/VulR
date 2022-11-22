from PyQt5.Qt import *

from window.ui.import_package_window import Ui_import_package_window
from window.func.request_convert_header import header_convert
from window.dialog.import_burp import Import_burp
from window.dialog.vul_introduction import Vul_introduction


class Import_package(QWidget, Ui_import_package_window):
    signal_close = pyqtSignal()
    signal_change = pyqtSignal(int, str, list, list, str, dict)

    def __init__(self, vul_id: int = 0, vul_name: str = '', introduction: str = '', header_key: list = ['__request_path__'], header_value: list = ['/'], body: str = '', other: dict = {'fixed_host': False,'judge_post': False,'judge_upload': False,'upload_file': ''}):
        super().__init__()
        # 配置改动标识
        self.flag_is_changed = False
        # 子窗口状态记录值
        self.childwindow_vul_introduction = False
        # 初始化header字典
        self.header_labels_dict = {}
        self.header_lineEdits_dict = {}
        self.header_buttons_dict = {}
        self.vul_introduction = introduction
        # 接收数据库数据
        self.vul_id = vul_id
        self.vul_name = vul_name
        self.introduction = introduction
        self.header_key = header_key
        self.header_value = header_value
        self.body = body
        self.other = other
        # 界面初始化
        self.setupUi(self)

    def setupUi(self, import_package_window):
        try:
            super().setupUi(import_package_window)
            self.set_icon()
            # 设置分类标题
            self.toolBox.setItemText(0, '请求头')
            self.toolBox.setItemText(1, '请求体')
            # 读取配置字典进行初始化
            self.init_content()
            # 窗口顶部按钮
            self.pushButton_introduction.clicked.connect(self.pushButton_introduction_event)
            self.pushButton_import_burp.clicked.connect(self.pushButton_import_burp_event)
            self.pushButton_save.clicked.connect(self.pushButton_save_event)
            # header事件
            self.checkBox_fixed_host.clicked.connect(self.checkBox_fixed_host_event)
            self.checkBox_judge_post.clicked.connect(self.checkBox_judge_post_event)
            self.pushButton_header_add.clicked.connect(self.pushButton_header_add_event)
            self.pushButton_get_change.clicked.connect(self.pushButton_get_change_event)
            self.toolButton_req_path.clicked.connect(self.toolButton_req_path_event)
            # body事件
            # self.toolButton_select_file.clicked.connect(self.toolButton_select_file_event)
            self.pushButton_post_change.clicked.connect(self.pushButton_post_change_event)
        except Exception as e:
            print("Exception in Import_package --> " + "setupUi")

    def set_icon(self):
        self.icon_edit = QIcon("resource/image/edit.png")
        self.icon_save = QIcon("resource/image/save.png")
        self.icon_delete = QIcon("resource/image/delete.png")
        # 设置图标
        self.toolButton_req_path.setIcon(self.icon_edit)

    def closeEvent(self, event):
        # 直接关闭所有未关闭的子窗口
        if self.childwindow_vul_introduction:
            self.vul_introduction_window.close()
            self.childwindow_vul_introduction = False
        # 判断是否有配置变动
        if self.convert_to_data() != (self.introduction, self.header_key, self.header_value, self.body, self.other):
            self.flag_is_changed = True
            # print(self.convert_to_data())
            # print((self.introduction, self.header_key, self.header_value, self.body, self.other))
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

    # 主窗口程序关闭调用接口
    def main_close(self):
        self.close()
        if self.flag_is_changed:
            return False
        else:
            # 子窗口成功关闭
            return True

    # 功能函数
    # 初始化界面内容
    def init_content(self):
        try:
            self.label_vul_name.setText(self.vul_name)
            headers = {}
            for key, value in zip(self.header_key[1:], self.header_value[1:]):
                headers[key] = value
            # print(1)
            self.lineEdit_req_path.setText(self.header_value[0])
            self.lineEdit_req_path.setCursorPosition(0)
            # print(2)
            for header_label, header_content in headers.items():
                self.add_header(header_label)
                self.header_lineEdits_dict['lineEdit_' + header_label].setText(header_content)
                self.header_lineEdits_dict['lineEdit_' + header_label].setCursorPosition(0)
            # print(self.other)
            self.checkBox_fixed_host.setChecked(self.other['fixed_host'])
            self.checkBox_judge_post.setChecked(self.other['judge_post'])
            self.checkBox_judge_upload.setChecked(self.other['judge_upload'])
            self.lineEdit_upload_file.setText(self.other['upload_file'])
            # print(4)
        except Exception as e:
            print("Exception in Import_package --> " + "init_content", e)

    # 读取当前界面所有配置并解析为相应数据库格式
    def convert_to_data(self):
        try:
            introduction = self.vul_introduction
            header_key = ['__request_path__']
            header_value = ['/']
            body = self.plainTextEdit_2.toPlainText()
            other = {
                'fixed_host': self.checkBox_fixed_host.isChecked(),
                'judge_post': self.checkBox_judge_post.isChecked(),
                'judge_upload': self.checkBox_judge_upload.isChecked(),
                'upload_file': self.lineEdit_upload_file.text()
            }
            for header_name in self.header_labels_dict.keys():
                header_name = header_name.split('_', 1)[-1]
                header_key.append(header_name)
                header_value.append(self.header_lineEdits_dict['lineEdit_' + header_name].text())
            return introduction, header_key, header_value, body, other
        except Exception as e:
            print("Exception in Import_package --> " + "convert_to_data", e)

    # 手动添加一个header
    def add_header(self, label_text):
        try:
            label_pos = self.gridLayout_3.rowCount()
            self.header_labels_dict['label_' + label_text] = QLabel(self.scrollAreaWidgetContents)
            self.header_lineEdits_dict['lineEdit_' + label_text] = QLineEdit(self.scrollAreaWidgetContents)
            self.header_buttons_dict['toolButton_' + label_text] = QToolButton(self.scrollAreaWidgetContents)
            self.header_labels_dict['label_' + label_text].setObjectName('label_' + label_text)
            self.header_lineEdits_dict['lineEdit_' + label_text].setObjectName('lineEdit_' + label_text)
            self.header_buttons_dict['toolButton_' + label_text].setObjectName('toolButton_' + label_text)
            self.header_labels_dict['label_' + label_text].setText(label_text)
            self.header_labels_dict['label_' + label_text].setToolTip(label_text)
            self.header_labels_dict['label_' + label_text].setAlignment(Qt.AlignCenter)
            self.header_labels_dict['label_' + label_text].setMaximumSize(QSize(80, 16777215))
            self.header_lineEdits_dict['lineEdit_' + label_text].setFrame(False)
            self.header_buttons_dict['toolButton_' + label_text].setIcon(self.icon_delete)
            self.header_buttons_dict['toolButton_' + label_text].setAutoRaise(True)
            self.header_buttons_dict['toolButton_' + label_text].clicked.connect(self.header_button_delete_event)
            self.gridLayout_3.addWidget(self.header_labels_dict['label_' + label_text], label_pos, 0, 1, 1)
            self.gridLayout_3.addWidget(self.header_lineEdits_dict['lineEdit_' + label_text], label_pos, 1, 1, 1)
            self.gridLayout_3.addWidget(self.header_buttons_dict['toolButton_' + label_text], label_pos, 2, 1, 1)
        except Exception as e:
            print("Exception in Import_package --> " + "add_header", e)

    # 手动删除一个header
    def del_header(self, label_text):
        try:
            self.header_labels_dict['label_' + label_text].deleteLater()
            self.header_lineEdits_dict['lineEdit_' + label_text].deleteLater()
            self.header_buttons_dict['toolButton_' + label_text].deleteLater()
            self.header_labels_dict.pop('label_' + label_text)
            self.header_lineEdits_dict.pop('lineEdit_' + label_text)
            self.header_buttons_dict.pop('toolButton_' + label_text)
        except Exception as e:
            print("Exception in Import_package --> " + "del_header", e)

    # 清空header，只剩一个请求路径
    def clear_header(self):
        try:
            for key in self.header_labels_dict.keys():
                self.header_labels_dict[key].deleteLater()
            for key in self.header_lineEdits_dict.keys():
                self.header_lineEdits_dict[key].deleteLater()
            for key in self.header_buttons_dict.keys():
                self.header_buttons_dict[key].deleteLater()
            self.header_labels_dict.clear()
            self.header_lineEdits_dict.clear()
            self.header_buttons_dict.clear()
        except Exception as e:
            print("Exception in Import_package --> " + "clear_header", e)

    # 槽函数
    # 勾选锁定host
    def checkBox_fixed_host_event(self):
        try:
            if self.checkBox_fixed_host.isChecked():
                if 'label_Host' in self.header_labels_dict.keys():
                    self.header_lineEdits_dict['lineEdit_Host'].setReadOnly(True)
                else:
                    QMessageBox.warning(self, "提示", '找不到 Host 请求头！', QMessageBox.Ok)
                    self.checkBox_fixed_host.setChecked(False)
            else:
                if 'label_Host' in self.header_labels_dict.keys():
                    self.header_lineEdits_dict['lineEdit_Host'].setReadOnly(False)
                else:
                    QMessageBox.warning(self, "提示", '找不到 Host 请求头！', QMessageBox.Ok)
                    self.checkBox_fixed_host.setChecked(False)
        except Exception as e:
            print("Exception in Import_package --> " + "checkBox_fixed_host_event", e)

    # 勾选是否POST
    def checkBox_judge_post_event(self):
        try:
            if self.checkBox_judge_post.isChecked():
                print(1111)
                # self.toolBoxPage_post.setAcceptDrops(False)
            else:
                print(2222)
                # self.toolBoxPage_post.setAcceptDrops(True)
        except Exception as e:
            print("Exception in Import_package --> " + "checkBox_judge_post_event", e)

    # 介绍按钮
    def pushButton_introduction_event(self):
        try:
            self.vul_introduction_window = Vul_introduction(self.vul_introduction)
            self.vul_introduction_window.signal_close.connect(self.vul_introduction_window_close_event)
            self.vul_introduction_window.signal_yes.connect(self.vul_introduction_window_yes_event)
            self.vul_introduction_window.show()
            self.childwindow_vul_introduction = False
        except Exception as e:
            print("Exception in Import_package --> " + "pushButton_introduction_event", e)

    # burp数据包识别按钮
    def pushButton_import_burp_event(self):
        try:
            self.import_burp_dialog = Import_burp()
            self.import_burp_dialog.signal_yes.connect(self.import_burp_dialog_yes_event)
            self.import_burp_dialog.show()
        except Exception as e:
            print("Exception in Import_package --> " + "pushButton_get_change_event", e)

    # 保存配置
    def pushButton_save_event(self):
        try:
            introduction, header_key, header_value, body, other = self.convert_to_data()
            self.introduction = introduction
            self.header_key = header_key
            self.header_value = header_value
            self.body = body
            self.other = other
            self.signal_change.emit(self.vul_id, introduction, header_key, header_value, body, other)
        except Exception as e:
            print("Exception in Import_package --> " + "pushButton_save_event", e)

    # 添加header按钮
    def pushButton_header_add_event(self):
        try:
            label_text, ok = QInputDialog.getText(self, "输入提示", "请输入header标签名:", QLineEdit.Normal)
            if label_text and ok and label_text not in self.header_labels_dict.keys():
                self.add_header(label_text)
        except Exception as e:
            print("Exception in Import_package --> " + "pushButton_header_add_event", e)

    # 智能识别按钮
    def pushButton_get_change_event(self):
        try:
            headers_tmp = self.plainTextEdit_imput_get.toPlainText()
            if headers_tmp:
                headers = header_convert(headers_tmp.split('\n'))
                # 判断是否需要完全初始化
                if len(self.header_labels_dict) == 0:
                    # 读取burp包，设置请求路径
                    if 'HTTP' in headers_tmp.split('\n')[0]:
                        self.lineEdit_req_path.setText(headers_tmp.split('\n')[0].split(' ')[1])
                        self.lineEdit_req_path.setCursorPosition(0)
                    # 遍历header头，添加相应行
                    for header_label, header_content in headers.items():
                        self.add_header(header_label)
                        self.header_lineEdits_dict['lineEdit_' + header_label].setText(header_content)
                        self.header_lineEdits_dict['lineEdit_' + header_label].setCursorPosition(0)
                else:
                    self.clear_header()
                    if 'HTTP' in headers_tmp.split('\n')[0]:
                        self.lineEdit_req_path.setText(headers_tmp.split('\n')[0].split(' ')[1])
                        self.lineEdit_req_path.setCursorPosition(0)
                    for header_label, header_content in headers.items():
                        self.add_header(header_label)
                        self.header_lineEdits_dict['lineEdit_' + header_label].setText(header_content)
                        self.header_lineEdits_dict['lineEdit_' + header_label].setCursorPosition(0)
                if headers_tmp.startswith('POST'):
                    self.checkBox_judge_post.setChecked(True)
                self.checkBox_fixed_host.setChecked(False)
            else:
                QMessageBox.warning(self, "提示", '识别区不能为空！', QMessageBox.Ok)
            pass
        except Exception as e:
            print("Exception in Import_package --> " + "pushButton_get_change_event", e)

    # 请求路径编辑按钮
    def toolButton_req_path_event(self):
        try:
            if self.lineEdit_req_path.isReadOnly():
                self.lineEdit_req_path.setReadOnly(False)
                self.toolButton_req_path.setIcon(self.icon_save)
            else:
                self.lineEdit_req_path.setReadOnly(True)
                self.toolButton_req_path.setIcon(self.icon_edit)
        except Exception as e:
            print("Exception in Import_package --> " + "toolButton_req_path_event", e)

    # header对应删除按钮
    def header_button_delete_event(self):
        try:
            label_text = self.sender().objectName().split('_', 1)[-1]
            self.del_header(label_text)
        except Exception as e:
            print("Exception in Import_package --> " + "header_button_delete_event", e)

    # POST模式智能识别按钮
    def pushButton_post_change_event(self):
        try:
            body_tmp = self.plainTextEdit_input_post.toPlainText()
            if body_tmp:
                pass
                self.checkBox_judge_post.setChecked(True)
            else:
                QMessageBox.warning(self, "提示", '识别区不能为空！', QMessageBox.Ok)
        except Exception as e:
            print("Exception in Import_package --> " + "pushButton_post_change_event", e)

    # 信号接受事件槽函数
    def import_burp_dialog_yes_event(self, header_tmp, body_tmp, data_type):
        try:
            if data_type == 'GET':
                self.plainTextEdit_imput_get.setPlainText(header_tmp)
            elif data_type == 'POST':
                self.plainTextEdit_imput_get.setPlainText(header_tmp)
                self.plainTextEdit_input_post.setPlainText(body_tmp)
            else:
                pass
        except Exception as e:
            print("Exception in Import_package --> " + "import_burp_dialog_yes_event", e)

    def vul_introduction_window_close_event(self):
        self.childwindow_vul_introduction = False

    def vul_introduction_window_yes_event(self, introduction):
        try:
            self.vul_introduction = introduction
        except Exception as e:
            print("Exception in Import_package --> " + "vul_introduction_window_yes_event", e)

    def set_qss(self):
        pass


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    import_package_window = QWidget()
    ui = Import_package(0)
    # ui.setupUi(import_package_window)
    import_package_window.show()
    sys.exit(app.exec_())
