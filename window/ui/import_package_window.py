# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'import_package_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_import_package_window(object):
    def setupUi(self, import_package_window):
        import_package_window.setObjectName("import_package_window")
        import_package_window.resize(750, 659)
        self.gridLayout = QtWidgets.QGridLayout(import_package_window)
        self.gridLayout.setObjectName("gridLayout")
        self.toolBox = QtWidgets.QToolBox(import_package_window)
        self.toolBox.setObjectName("toolBox")
        self.toolBoxPage_get = QtWidgets.QWidget()
        self.toolBoxPage_get.setGeometry(QtCore.QRect(0, 0, 732, 551))
        self.toolBoxPage_get.setObjectName("toolBoxPage_get")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.toolBoxPage_get)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.pushButton_get_change = QtWidgets.QPushButton(self.toolBoxPage_get)
        self.pushButton_get_change.setObjectName("pushButton_get_change")
        self.gridLayout_4.addWidget(self.pushButton_get_change, 0, 4, 1, 1)
        self.label_header = QtWidgets.QLabel(self.toolBoxPage_get)
        self.label_header.setObjectName("label_header")
        self.gridLayout_4.addWidget(self.label_header, 0, 0, 1, 1)
        self.scrollArea_header = QtWidgets.QScrollArea(self.toolBoxPage_get)
        self.scrollArea_header.setWidgetResizable(True)
        self.scrollArea_header.setObjectName("scrollArea_header")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 712, 246))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.toolButton_req_path = QtWidgets.QToolButton(self.scrollAreaWidgetContents)
        self.toolButton_req_path.setObjectName("toolButton_req_path")
        self.gridLayout_3.addWidget(self.toolButton_req_path, 0, 2, 1, 1)
        self.lineEdit_req_path = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_req_path.setReadOnly(True)
        self.lineEdit_req_path.setObjectName("lineEdit_req_path")
        self.gridLayout_3.addWidget(self.lineEdit_req_path, 0, 1, 1, 1)
        self.label_req_path = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_req_path.setObjectName("label_req_path")
        self.gridLayout_3.addWidget(self.label_req_path, 0, 0, 1, 1)
        self.scrollArea_header.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout_4.addWidget(self.scrollArea_header, 2, 0, 1, 5)
        self.pushButton_header_add = QtWidgets.QPushButton(self.toolBoxPage_get)
        self.pushButton_header_add.setObjectName("pushButton_header_add")
        self.gridLayout_4.addWidget(self.pushButton_header_add, 0, 3, 1, 1)
        self.plainTextEdit_imput_get = QtWidgets.QPlainTextEdit(self.toolBoxPage_get)
        self.plainTextEdit_imput_get.setObjectName("plainTextEdit_imput_get")
        self.gridLayout_4.addWidget(self.plainTextEdit_imput_get, 1, 0, 1, 5)
        self.checkBox_fixed_host = QtWidgets.QCheckBox(self.toolBoxPage_get)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkBox_fixed_host.sizePolicy().hasHeightForWidth())
        self.checkBox_fixed_host.setSizePolicy(sizePolicy)
        self.checkBox_fixed_host.setObjectName("checkBox_fixed_host")
        self.gridLayout_4.addWidget(self.checkBox_fixed_host, 0, 1, 1, 1)
        self.checkBox_judge_post = QtWidgets.QCheckBox(self.toolBoxPage_get)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkBox_judge_post.sizePolicy().hasHeightForWidth())
        self.checkBox_judge_post.setSizePolicy(sizePolicy)
        self.checkBox_judge_post.setObjectName("checkBox_judge_post")
        self.gridLayout_4.addWidget(self.checkBox_judge_post, 0, 2, 1, 1)
        self.toolBox.addItem(self.toolBoxPage_get, "")
        self.toolBoxPage_post = QtWidgets.QWidget()
        self.toolBoxPage_post.setGeometry(QtCore.QRect(0, 0, 732, 551))
        self.toolBoxPage_post.setObjectName("toolBoxPage_post")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.toolBoxPage_post)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.scrollArea_body = QtWidgets.QScrollArea(self.toolBoxPage_post)
        self.scrollArea_body.setStyleSheet("background-color: rgb(85, 85, 255);")
        self.scrollArea_body.setWidgetResizable(True)
        self.scrollArea_body.setObjectName("scrollArea_body")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 712, 246))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.plainTextEdit_2 = QtWidgets.QPlainTextEdit(self.scrollAreaWidgetContents_2)
        self.plainTextEdit_2.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.plainTextEdit_2.setObjectName("plainTextEdit_2")
        self.gridLayout_2.addWidget(self.plainTextEdit_2, 0, 0, 1, 1)
        self.scrollArea_body.setWidget(self.scrollAreaWidgetContents_2)
        self.gridLayout_5.addWidget(self.scrollArea_body, 2, 0, 1, 5)
        self.checkBox_judge_upload = QtWidgets.QCheckBox(self.toolBoxPage_post)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkBox_judge_upload.sizePolicy().hasHeightForWidth())
        self.checkBox_judge_upload.setSizePolicy(sizePolicy)
        self.checkBox_judge_upload.setObjectName("checkBox_judge_upload")
        self.gridLayout_5.addWidget(self.checkBox_judge_upload, 0, 3, 1, 1)
        self.pushButton_post_change = QtWidgets.QPushButton(self.toolBoxPage_post)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_post_change.sizePolicy().hasHeightForWidth())
        self.pushButton_post_change.setSizePolicy(sizePolicy)
        self.pushButton_post_change.setObjectName("pushButton_post_change")
        self.gridLayout_5.addWidget(self.pushButton_post_change, 0, 4, 1, 1)
        self.toolButton_select_file = QtWidgets.QToolButton(self.toolBoxPage_post)
        self.toolButton_select_file.setObjectName("toolButton_select_file")
        self.gridLayout_5.addWidget(self.toolButton_select_file, 0, 2, 1, 1)
        self.plainTextEdit_input_post = QtWidgets.QPlainTextEdit(self.toolBoxPage_post)
        self.plainTextEdit_input_post.setObjectName("plainTextEdit_input_post")
        self.gridLayout_5.addWidget(self.plainTextEdit_input_post, 1, 0, 1, 5)
        self.label_body = QtWidgets.QLabel(self.toolBoxPage_post)
        self.label_body.setObjectName("label_body")
        self.gridLayout_5.addWidget(self.label_body, 0, 0, 1, 1)
        self.lineEdit_upload_file = QtWidgets.QLineEdit(self.toolBoxPage_post)
        self.lineEdit_upload_file.setAutoFillBackground(True)
        self.lineEdit_upload_file.setStyleSheet("background-color: rgb(240, 240, 240);")
        self.lineEdit_upload_file.setText("")
        self.lineEdit_upload_file.setFrame(False)
        self.lineEdit_upload_file.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineEdit_upload_file.setReadOnly(True)
        self.lineEdit_upload_file.setObjectName("lineEdit_upload_file")
        self.gridLayout_5.addWidget(self.lineEdit_upload_file, 0, 1, 1, 1)
        self.toolBox.addItem(self.toolBoxPage_post, "")
        self.gridLayout.addWidget(self.toolBox, 2, 0, 1, 4)
        self.pushButton_introduction = QtWidgets.QPushButton(import_package_window)
        self.pushButton_introduction.setObjectName("pushButton_introduction")
        self.gridLayout.addWidget(self.pushButton_introduction, 1, 1, 1, 1)
        self.pushButton_save = QtWidgets.QPushButton(import_package_window)
        self.pushButton_save.setObjectName("pushButton_save")
        self.gridLayout.addWidget(self.pushButton_save, 1, 3, 1, 1)
        self.label_vul_name = QtWidgets.QLabel(import_package_window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_vul_name.sizePolicy().hasHeightForWidth())
        self.label_vul_name.setSizePolicy(sizePolicy)
        self.label_vul_name.setObjectName("label_vul_name")
        self.gridLayout.addWidget(self.label_vul_name, 1, 0, 1, 1)
        self.pushButton_import_burp = QtWidgets.QPushButton(import_package_window)
        self.pushButton_import_burp.setObjectName("pushButton_import_burp")
        self.gridLayout.addWidget(self.pushButton_import_burp, 1, 2, 1, 1)

        self.retranslateUi(import_package_window)
        QtCore.QMetaObject.connectSlotsByName(import_package_window)

    def retranslateUi(self, import_package_window):
        _translate = QtCore.QCoreApplication.translate
        import_package_window.setWindowTitle(_translate("import_package_window", "Form"))
        self.pushButton_get_change.setText(_translate("import_package_window", "智能识别"))
        self.label_header.setText(_translate("import_package_window", "header"))
        self.toolButton_req_path.setText(_translate("import_package_window", "编辑"))
        self.lineEdit_req_path.setText(_translate("import_package_window", "/"))
        self.label_req_path.setText(_translate("import_package_window", "请求路径"))
        self.pushButton_header_add.setText(_translate("import_package_window", "添加header"))
        self.plainTextEdit_imput_get.setPlaceholderText(_translate("import_package_window", "智能识别区，请粘贴请求头到此处"))
        self.checkBox_fixed_host.setText(_translate("import_package_window", "锁定host"))
        self.checkBox_judge_post.setText(_translate("import_package_window", "是否POST"))
        self.checkBox_judge_upload.setText(_translate("import_package_window", "是否文件上传"))
        self.pushButton_post_change.setText(_translate("import_package_window", "智能识别"))
        self.toolButton_select_file.setText(_translate("import_package_window", "选择上传文件"))
        self.plainTextEdit_input_post.setPlaceholderText(_translate("import_package_window", "智能识别区，请粘贴请求体到此处，勾选文件上传后需选择本地文件进行上传"))
        self.label_body.setText(_translate("import_package_window", "body"))
        self.pushButton_introduction.setText(_translate("import_package_window", "添加说明"))
        self.pushButton_save.setText(_translate("import_package_window", "保存"))
        self.label_vul_name.setText(_translate("import_package_window", "漏洞名"))
        self.pushButton_import_burp.setText(_translate("import_package_window", "burp数据包识别"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    import_package_window = QtWidgets.QWidget()
    ui = Ui_import_package_window()
    ui.setupUi(import_package_window)
    import_package_window.show()
    sys.exit(app.exec_())
