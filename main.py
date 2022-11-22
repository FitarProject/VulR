import ctypes
import re
import sys
import json

from PyQt5.Qt import *

from window.func.sql_connection import MySQLite
from window.import_package import Import_package
from window.ui.main_window import Ui_Form

ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")


class Window(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        # 编辑状态记录指针
        self.writable_item = None
        # 当前装载漏洞信息
        self.curr_vul = None
        # 右键选中指针
        self.curr_item = None
        self.icon_save = None
        self.icon_edit = None
        self.icon_delete = None
        self.icon_vul = None
        self.icon_folder = None
        # 初始化header字典
        self.header_labels_dict = {}
        self.header_lineEdits_dict = {}
        self.header_buttons_dict = {}
        # 子窗口状态记录值
        self.childwindow_import_package = False
        # 获取显示器分辨率
        self.desktop = QApplication.desktop()
        self.screenRect = self.desktop.screenGeometry()
        self.screenheight = self.screenRect.height()
        self.screenwidth = self.screenRect.width()
        self.height = int(self.screenheight * 0.7)
        self.width = int(self.screenwidth * 0.55)
        # print("Screen height {}".format(self.screenheight))
        # print("Screen width {}".format(self.screenwidth))
        # 连接数据库
        self.sqlite = MySQLite()
        self.setupUi(self)

    def setupUi(self, main_widget):
        super().setupUi(main_widget)
        self.set_icon()
        self.set_qss()
        # 适应屏幕分辨率重设大小
        self.resize(self.width, self.height)
        # 设置初始界面比例
        self.splitter_list_and_detail.setStretchFactor(0, 20)
        self.splitter_list_and_detail.setStretchFactor(1, 80)
        self.splitter_header_and_request.setStretchFactor(0, 45)
        self.splitter_header_and_request.setStretchFactor(1, 55)
        self.splitter_header_and_body.setStretchFactor(0, 50)
        self.splitter_header_and_body.setStretchFactor(1, 50)
        self.splitter_request_input.setStretchFactor(0, 30)
        self.splitter_request_input.setStretchFactor(1, 70)
        self.splitter_target.setStretchFactor(0, 90)
        self.splitter_target.setStretchFactor(1, 10)
        self.splitter_request.setStretchFactor(0, 90)
        self.splitter_request.setStretchFactor(1, 10)
        # 初始化漏洞列表
        self.vul_list_init()
        # 设置右键菜单
        self.select_vul.setContextMenuPolicy(Qt.CustomContextMenu)
        self.select_vul.customContextMenuRequested[QPoint].connect(self.tree_right_menu)
        # 连接信号和槽函数
        self.pushButton_introduction.clicked.connect(self.pushButton_introduction_event)
        self.pushButton_modify_vul.clicked.connect(self.pushButton_modify_vul_event)
        # header事件
        self.pushButton_add_header.clicked.connect(self.pushButton_add_header_event)
        self.pushButton_edit_header.clicked.connect(self.pushButton_edit_header_event)
        self.toolButton_req_path.clicked.connect(self.toolButton_req_path_event)
        # body事件
        self.pushButton_edit_body.clicked.connect(self.pushButton_edit_body_event)
        # 处理目标、攻击和结果事件
        self.pushButton_target_deal.clicked.connect(self.pushButton_target_deal_event)
        # self.pushButton_attack.clicked.connect(self.pushButton_attack_event)
        # self.pushButton_export_result.clicked.connect(self.pushButton_export_result_event)
        # 其他事件
        self.select_vul.itemSelectionChanged.connect(self.change_item_writable_event)

    # 重写close事件，关闭一切子窗口
    def closeEvent(self, event):
        try:
            # 子窗口全部关闭标识
            flag_close = True
            # 关闭所有未关闭的子窗口
            if self.childwindow_import_package:
                # 确认子窗口是否退出
                if not self.import_package_window.main_close():
                    flag_close = False
            if flag_close:
                # 记录文件夹节点打开状态
                self.open_folder_record()
                # 关闭数据库连接
                self.sqlite.close()
                super().closeEvent(event)
            else:
                event.ignore()
        except Exception as e:
            print("Exception in main --> " + "closeEvent", e)

    # 设置qss
    def set_qss(self):
        pass

    # 设置图标
    def set_icon(self):
        self.icon_delete = QIcon("resource/image/delete.png")
        self.icon_edit = QIcon("resource/image/edit.png")
        self.icon_save = QIcon("resource/image/save.png")
        self.icon_folder = QIcon("resource/image/folder.png")
        self.icon_vul = QIcon("resource/image/vul.png")
        # 设置图标
        self.toolButton_req_path.setIcon(self.icon_edit)

    # 功能函数
    # 读取数据库绘制漏洞列表
    def vul_list_init(self):
        try:
            node_list = self.sqlite.sql_query_vul_list()
            for node in node_list[1:]:
                if node[4] == 0:
                    item = QTreeWidgetItem(self.select_vul)
                    item.setData(0, Qt.UserRole, node[0])
                    item.setText(0, node[1])
                    if node[2] == 0:
                        item.setIcon(0, self.icon_folder)
                    else:
                        item.setData(0, Qt.UserRole + 1, node[3])
                        item.setIcon(0, self.icon_vul)
                    self.select_vul.addTopLevelItem(item)
                else:
                    # 遍历节点
                    item_tree = QTreeWidgetItemIterator(self.select_vul)
                    father_item = None
                    while item_tree.value():
                        if item_tree.value().data(0, Qt.UserRole) == node[4]:
                            father_item = item_tree.value()
                        item_tree.__iadd__(1)
                    if father_item:
                        item = QTreeWidgetItem(father_item)
                        item.setData(0, Qt.UserRole, node[0])
                        item.setText(0, node[1])
                        if node[2] == 0:
                            item.setIcon(0, self.icon_folder)
                        else:
                            item.setData(0, Qt.UserRole + 1, node[3])
                            item.setIcon(0, self.icon_vul)
            # 恢复节点状态
            self.open_folder_recover()
            # self.select_vul.expandAll()
        except Exception as e:
            print("Exception in main --> " + "vul_list_init", e)

    # 任务列表右键菜单
    def tree_right_menu(self, point):
        try:
            self.curr_item = self.select_vul.itemAt(point)
            if self.curr_item:
                # print(self.curr_item.data(0, Qt.UserRole))
                vul_name = self.curr_item.text(0)
                popMenu = QMenu()
                # print('当前节点为：', self.curr_item, vul_name, 'id = ', self.curr_item.data(0, Qt.UserRole))
                item_type = self.sqlite.sql_query_type(self.curr_item.data(0, Qt.UserRole))
                if item_type:
                    if item_type[0] == 0:
                        for i in range(self.curr_item.childCount()):
                            print('  |__子节点为：', self.curr_item.child(i))
                        addVulAct = QAction(u'添加漏洞', self)
                        popMenu.addAction(addVulAct)
                        addVulAct.triggered.connect(self.addVulAct_event)
                        addChildDirAct = QAction(u'添加子目录', self)
                        popMenu.addAction(addChildDirAct)
                        addChildDirAct.triggered.connect(self.addChildDirAct_event)
                        renameDirAct = QAction(u'重命名目录', self)
                        popMenu.addAction(renameDirAct)
                        renameDirAct.triggered.connect(self.renameAct_event)
                        delDirAct = QAction(u'删除目录', self)
                        popMenu.addAction(delDirAct)
                        delDirAct.triggered.connect(self.delDirAct_event)
                        exportVulAct = QAction(u'导出', self)
                        popMenu.addAction(exportVulAct)
                        exportVulAct.triggered.connect(self.exportVulAct_event)
                    elif item_type[0] == 1:
                        # print('当前无子节点')
                        loadVulAct = QAction(u'装载', self)
                        popMenu.addAction(loadVulAct)
                        loadVulAct.triggered.connect(self.loadVulAct_event)
                        editVulAct = QAction(u'编辑', self)
                        popMenu.addAction(editVulAct)
                        editVulAct.triggered.connect(self.editVulAct_event)
                        renameVulAct = QAction(u'重命名', self)
                        popMenu.addAction(renameVulAct)
                        renameVulAct.triggered.connect(self.renameAct_event)
                        delVulAct = QAction(u'删除', self)
                        popMenu.addAction(delVulAct)
                        delVulAct.triggered.connect(self.delVulAct_event)
                        exportVulAct = QAction(u'导出', self)
                        popMenu.addAction(exportVulAct)
                        exportVulAct.triggered.connect(self.exportVulAct_event)
                    popMenu.exec_(QCursor.pos())
                else:
                    print('类型出错！')
            else:
                popMenu = QMenu()
                print('未选中节点')
                addRootDirAct = QAction(u'添加根目录', self)
                popMenu.addAction(addRootDirAct)
                addRootDirAct.triggered.connect(self.addRootDirAct_event)
                addVulAct = QAction(u'添加漏洞', self)
                popMenu.addAction(addVulAct)
                addVulAct.triggered.connect(self.addRootVulAct_event)
                importVulAct = QAction(u'导入', self)
                popMenu.addAction(importVulAct)
                importVulAct.triggered.connect(self.importVulAct_event)
                popMenu.exec_(QCursor.pos())
        except Exception as e:
            print("Exception in main --> " + "tree_right_menu", e)

    # 递归删除目录函数
    def delete_dir_vul(self, select_item):
        try:
            for i in range(select_item.childCount()):       # 遍历子节点
                child_id = select_item.child(0).data(0, Qt.UserRole)
                item_type = self.sqlite.sql_query_type(child_id)
                if item_type:
                    if item_type[0] == 0:           # 递归条件，若为目录则继续递归
                        self.delete_dir_vul(select_item.child(0))
                    elif item_type[0] == 1:         # 退出条件，若为漏洞则删除
                        # print('remove', select_item.child(0), select_item.childCount())
                        select_item.removeChild(select_item.child(0))
                        # 删除数据库数据
                        vul_id = self.sqlite.sql_query_vul_id(child_id)
                        self.sqlite.sql_delete_node(child_id)
                        self.sqlite.sql_delete_vul(vul_id[0])
                else:
                    print('类型出错！')
            if select_item.parent():        # 子节点删除完毕，删除当前节点
                # print('remove', select_item, select_item.childCount())
                select_item.parent().removeChild(select_item)
            else:
                # print('remove', select_item, select_item.childCount())
                self.select_vul.takeTopLevelItem(self.select_vul.indexOfTopLevelItem(select_item))
            self.sqlite.sql_delete_node(select_item.data(0, Qt.UserRole))
            return
        except Exception as e:
            print("Exception in main --> " + "delete_dir_vul", e)

    # 记录文件夹节点状态
    def open_folder_record(self):
        pass

    # 恢复文件夹节点状态
    def open_folder_recover(self):
        pass
        # # 遍历节点
        # item_tree = QTreeWidgetItemIterator(self.select_vul)
        # while item_tree.value():
        #     item_tree.value().setExpanded(False)
        #     item_tree.__iadd__(1)

    # 手动添加一个header
    def add_header(self, label_text):
        try:
            label_pos = self.gridLayout_3.rowCount()
            self.header_labels_dict['label_' + label_text] = QLabel(self.scrollAreaWidgetContents_header)
            self.header_lineEdits_dict['lineEdit_' + label_text] = QLineEdit(self.scrollAreaWidgetContents_header)
            self.header_buttons_dict['toolButton_' + label_text] = QToolButton(self.scrollAreaWidgetContents_header)
            self.header_labels_dict['label_' + label_text].setObjectName('label_' + label_text)
            self.header_lineEdits_dict['lineEdit_' + label_text].setObjectName('lineEdit_' + label_text)
            self.header_buttons_dict['toolButton_' + label_text].setObjectName('toolButton_' + label_text)
            self.header_labels_dict['label_' + label_text].setText(label_text)
            self.header_labels_dict['label_' + label_text].setToolTip(label_text)
            self.header_labels_dict['label_' + label_text].setAlignment(Qt.AlignCenter)
            self.header_labels_dict['label_' + label_text].setMaximumSize(QSize(80, 16777215))
            if self.pushButton_edit_header.text() == '编辑':
                self.header_lineEdits_dict['lineEdit_' + label_text].setReadOnly(True)
            self.header_lineEdits_dict['lineEdit_' + label_text].setFrame(False)
            self.header_buttons_dict['toolButton_' + label_text].setIcon(self.icon_delete)
            self.header_buttons_dict['toolButton_' + label_text].setAutoRaise(True)
            self.header_buttons_dict['toolButton_' + label_text].clicked.connect(self.header_button_delete_event)
            self.gridLayout_3.addWidget(self.header_labels_dict['label_' + label_text], label_pos, 0, 1, 1)
            self.gridLayout_3.addWidget(self.header_lineEdits_dict['lineEdit_' + label_text], label_pos, 1, 1, 1)
            self.gridLayout_3.addWidget(self.header_buttons_dict['toolButton_' + label_text], label_pos, 2, 1, 1)
        except Exception as e:
            print("Exception in main --> " + "add_header", e)

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
            print("Exception in main --> " + "del_header", e)

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
            print("Exception in main --> " + "clear_header", e)

    # 槽函数
    def pushButton_target_deal_event(self):
        try:
            target_list = []
            target_dealed = ''
            target_dealed_list = []
            if self.plainTextEdit_target.toPlainText():
                targets = self.plainTextEdit_target.toPlainText().replace(',', '\n').split('\n')
                for target in targets:                              # 删除行尾的换行符
                    target_list.append(target.rstrip('\n'))
                pattern1 = '(?:http(?:s?)://)?[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}(:[0-9]{1,5})?'
                pattern2 = '(?:http(?:s?)://)?(?:[\w|-]+\.)+[a-zA-Z]+(?::\d{1,5})?'
                black_suffix = ['html', 'php', 'jsp', 'jspx', 'rar', 'zip', 'exe', 'pdf', 'doc', 'docx', 'avi', 'tmp',
                                'db', 'json', 'xls', 'xlsx', 'jpg', 'png', 'ico', 'img']
                for line in target_list:
                    ip = re.search(pattern1, line)
                    domain = re.search(pattern2, line)
                    if domain:
                        if domain.group(0).split('.')[-1] not in black_suffix:      # 由于/xxx/a.txt也会被匹配，加一层过滤
                            if domain.group(0).startswith('http://') or domain.group(0).startswith('https://'):
                                target_dealed_list.append(domain.group(0) + '\n')
                            else:
                                target_dealed_list.append('http://' + domain.group(0) + '\n')
                    elif ip:
                        if ip.group(0).startswith('http://') or ip.group(0).startswith('https://'):
                            target_dealed_list.append(ip.group(0) + '\n')
                        else:
                            target_dealed_list.append('http://' + ip.group(0) + '\n')
                target_dealed_list = {}.fromkeys(target_dealed_list).keys()
            for i in target_dealed_list:
                target_dealed += i
            self.plainTextEdit_target.setPlainText(target_dealed)
        except Exception as e:
            print("Exception in main --> " + "pushButton_target_deal_event", e)

    def addRootDirAct_event(self):
        try:
            item_id = self.sqlite.sql_query_last_id()
            if item_id:
                item = QTreeWidgetItem(self.select_vul)
                self.change_item_writable_event()
                self.writable_item = item
                item.setData(0, Qt.UserRole, item_id[0] + 1)
                item.setText(0, '<未命名分组>')
                item.setIcon(0, self.icon_folder)
                self.select_vul.addTopLevelItem(item)
                item.setFlags(item.flags() | Qt.ItemIsEditable)
                self.select_vul.editItem(item)
                # 插入数据
                new_data = [item_id[0] + 1, '<未命名分组>', 0, 0, 0]
                self.sqlite.sql_insert_node(new_data)
        except Exception as e:
            print("Exception in main --> " + "addRootDirAct_event", e)

    def addChildDirAct_event(self):
        try:
            select_item = self.curr_item
            item_id = self.sqlite.sql_query_last_id()
            if item_id:
                item = QTreeWidgetItem(select_item)
                self.change_item_writable_event()
                self.writable_item = item
                item.setData(0, Qt.UserRole, item_id[0] + 1)
                item.setText(0, '<未命名分组>')
                item.setIcon(0, self.icon_folder)
                item.setFlags(item.flags() | Qt.ItemIsEditable)
                self.select_vul.editItem(item)
                # 插入数据
                new_data = [item_id[0] + 1, '<未命名分组>', 0, 0, select_item.data(0, Qt.UserRole)]
                self.sqlite.sql_insert_node(new_data)
        except Exception as e:
            print("Exception in main --> " + "addChildDirAct_event", e)

    def addRootVulAct_event(self):
        try:
            item_id = self.sqlite.sql_query_last_id()
            vul_id = self.sqlite.sql_query_last_vul_id()
            if item_id and vul_id:
                item = QTreeWidgetItem(self.select_vul)
                self.change_item_writable_event()
                self.writable_item = item
                item.setData(0, Qt.UserRole, item_id[0] + 1)
                item.setData(0, Qt.UserRole + 1, vul_id[0] + 1)
                item.setText(0, '<未命名漏洞>')
                item.setIcon(0, self.icon_vul)
                self.select_vul.addTopLevelItem(item)
                item.setFlags(item.flags() | Qt.ItemIsEditable)
                self.select_vul.editItem(item)
                # 插入数据
                new_vul_data = [vul_id[0] + 1, '', '', '', '', '']
                self.sqlite.sql_insert_vul(new_vul_data)
                new_data = [item_id[0] + 1, '<未命名漏洞>', 1, vul_id[0] + 1, 0]
                self.sqlite.sql_insert_node(new_data)
        except Exception as e:
            print("Exception in main --> " + "addVulAct_event", e)

    def addVulAct_event(self):
        try:
            select_item = self.curr_item
            item_id = self.sqlite.sql_query_last_id()
            vul_id = self.sqlite.sql_query_last_vul_id()
            if item_id:
                item = QTreeWidgetItem(select_item)
                self.change_item_writable_event()
                self.writable_item = item
                item.setData(0, Qt.UserRole, item_id[0] + 1)
                item.setData(0, Qt.UserRole + 1, vul_id[0] + 1)
                item.setText(0, '<未命名漏洞>')
                item.setIcon(0, self.icon_vul)
                item.setFlags(item.flags() | Qt.ItemIsEditable)
                self.select_vul.editItem(item)
                # 插入数据
                new_vul_data = [vul_id[0] + 1, '', '', '', '', '']
                self.sqlite.sql_insert_vul(new_vul_data)
                new_data = [item_id[0] + 1, '<未命名漏洞>', 1, vul_id[0] + 1, select_item.data(0, Qt.UserRole)]
                self.sqlite.sql_insert_node(new_data)
        except Exception as e:
            print("Exception in main --> " + "addVulAct_event", e)

    def delDirAct_event(self):
        try:
            select_item = self.curr_item
            if select_item.childCount():
                if QMessageBox.warning(self, "操作确认", '是否删除当前目录及其所有漏洞？',
                                       QMessageBox.Ok | QMessageBox.Cancel) == QMessageBox.Ok:
                    self.delete_dir_vul(select_item)
            else:
                if select_item.parent():
                    # print('remove', select_item, select_item.childCount())
                    select_item.parent().removeChild(select_item)
                else:
                    # print('remove', select_item, select_item.childCount())
                    self.select_vul.takeTopLevelItem(self.select_vul.indexOfTopLevelItem(select_item))
                # 删除数据库数据
                self.sqlite.sql_delete_node(select_item.data(0, Qt.UserRole))
        except Exception as e:
            print("Exception in main --> " + "delDirAct_event", e)

    def loadVulAct_event(self):
        try:
            flag_init = True
            if self.curr_vul:
                if QMessageBox.warning(self, "操作确认", '当前已装载漏洞，是否覆盖？', QMessageBox.Ok | QMessageBox.Cancel) == QMessageBox.Ok:
                    del self.curr_vul
                else:
                    flag_init = False
            if flag_init:
                select_item = self.curr_item
                node_id = select_item.data(0, Qt.UserRole)
                vul_id = self.sqlite.sql_query_vul_id(node_id)[0]
                vul_name = self.sqlite.sql_query_vul_name(vul_id)[0]
                introduction, header_key_tmp, header_value_tmp, body, other = self.sqlite.sql_query_vul_detail(vul_id)
                self.pushButton_introduction.setToolTip(introduction)
                header_key = header_key_tmp.split('+++++')
                header_value = header_value_tmp.split('+++++')
                other = json.loads(other)
                # 初始化漏洞字典
                self.curr_vul = {
                    'select_item': select_item,
                    'node_id': node_id,
                    'vul_id': vul_id,
                    'vul_name': vul_name,
                    'introduction': introduction,
                    'header_key': header_key,
                    'header_value': header_value,
                    'body': body,
                    'other': other
                }
                # 判断是否需要完全初始化
                if len(self.header_labels_dict) == 0:
                    self.lineEdit_req_path.setText(self.curr_vul['header_value'][0])
                    self.lineEdit_req_path.setCursorPosition(0)
                    # 遍历header头，添加相应行
                    for header_label, header_content in zip(self.curr_vul['header_key'][1:], self.curr_vul['header_value'][1:]):
                        self.add_header(header_label)
                        self.header_lineEdits_dict['lineEdit_' + header_label].setText(header_content)
                        self.header_lineEdits_dict['lineEdit_' + header_label].setCursorPosition(0)
                else:
                    self.clear_header()
                    self.lineEdit_req_path.setText(self.curr_vul['header_value'][0])
                    self.lineEdit_req_path.setCursorPosition(0)
                    for header_label, header_content in zip(self.curr_vul['header_key'][1:], self.curr_vul['header_value'][1:]):
                        self.add_header(header_label)
                        self.header_lineEdits_dict['lineEdit_' + header_label].setText(header_content)
                        self.header_lineEdits_dict['lineEdit_' + header_label].setCursorPosition(0)
                if other['fixed_host']:
                    pass
                if other['judge_post']:
                    self.plainTextEdit_body.setPlainText(self.curr_vul['body'])
                if other['judge_upload']:
                    pass
                    print(other['upload_file'])
        except Exception as e:
            print("Exception in main --> " + "loadVulAct_event", e)

    def editVulAct_event(self):
        try:
            flag = True
            if self.childwindow_import_package:
                if QMessageBox.warning(self, "操作确认", '已有正在编辑的漏洞，是否覆盖？', QMessageBox.Ok | QMessageBox.Cancel) == QMessageBox.Cancel:
                    flag = False
            if flag:
                select_item = self.curr_item
                node_id = select_item.data(0, Qt.UserRole)
                # print(node_id)
                vul_id = self.sqlite.sql_query_vul_id(node_id)[0]
                # print(vul_id)
                vul_name = self.sqlite.sql_query_vul_name(vul_id)[0]
                # print(vul_name)
                introduction, header_key_tmp, header_value_tmp, body, other = self.sqlite.sql_query_vul_detail(vul_id)
                if not introduction.strip():
                    introduction = ''
                header_key = header_key_tmp.split('+++++')
                header_value = header_value_tmp.split('+++++')
                other = json.loads(other)
                # print((introduction, header_key, header_value, body, other))
                # vul_id = 0
                # vul_name = '测试漏洞'
                # introduction = ''
                # header_key = ['__request_path__']
                # header_value = ['/']
                # body = ' '
                # other = {"fixed_host": false, "judge_post": false, "judge_upload": false, "upload_file": ""}
                self.import_package_window = Import_package(vul_id, vul_name, introduction, header_key, header_value, body, other)
                self.import_package_window.signal_close.connect(self.import_package_window_close_event)
                self.import_package_window.signal_change.connect(self.import_package_window_change_event)
                self.import_package_window.show()
                self.childwindow_import_package = True
        except Exception as e:
            print("Exception in main --> " + "editVulAct_event", e)

    def renameAct_event(self):
        try:
            self.writable_item = self.curr_item
            self.writable_item.setFlags(self.writable_item.flags() | Qt.ItemIsEditable)
            self.select_vul.editItem(self.writable_item)
        except Exception as e:
            print("Exception in main --> " + "renameAct_event", e)

    def delVulAct_event(self):
        try:
            select_item = self.curr_item
            if QMessageBox.warning(self, "操作确认", '是否删除当前漏洞？', QMessageBox.Ok | QMessageBox.Cancel) == QMessageBox.Ok:
                if select_item.parent():
                    select_item.parent().removeChild(select_item)
                else:
                    self.select_vul.takeTopLevelItem(self.select_vul.indexOfTopLevelItem(select_item))
                # 删除数据库数据
                vul_id = self.sqlite.sql_query_vul_id(select_item.data(0, Qt.UserRole))
                self.sqlite.sql_delete_node(select_item.data(0, Qt.UserRole))
                self.sqlite.sql_delete_vul(vul_id[0])
        except Exception as e:
            print("Exception in main --> " + "delVulAct_event", e)

    def importVulAct_event(self):
        try:
            pass
        except Exception as e:
            print("Exception in main --> " + "importVulAct_event", e)

    def exportVulAct_event(self):
        try:
            pass
        except Exception as e:
            print("Exception in main --> " + "exportVulAct_event", e)

    # 查看漏洞介绍按钮
    def pushButton_introduction_event(self):
        try:
            if self.curr_vul:
                QMessageBox.about(self, "漏洞介绍", self.curr_vul['introduction'])
            else:
                QMessageBox.warning(self, "提示", '请先装载漏洞！', QMessageBox.Ok)
        except Exception as e:
            print("Exception in main --> " + "pushButton_introduction_event", e)

    # 编辑漏洞
    def pushButton_modify_vul_event(self):
        try:
            if self.curr_vul:
                flag = True
                if self.childwindow_import_package:
                    if QMessageBox.warning(self, "操作确认", '已有正在编辑的漏洞，是否覆盖？', QMessageBox.Ok | QMessageBox.Cancel) == QMessageBox.Cancel:
                        flag = False
                if flag:
                    select_item = self.curr_vul['select_item']
                    node_id = select_item.data(0, Qt.UserRole)
                    vul_id = self.sqlite.sql_query_vul_id(node_id)[0]
                    vul_name = self.sqlite.sql_query_vul_name(vul_id)[0]
                    introduction, header_key_tmp, header_value_tmp, body, other = self.sqlite.sql_query_vul_detail(vul_id)
                    if not introduction.strip():
                        introduction = ''
                    header_key = header_key_tmp.split('+++++')
                    header_value = header_value_tmp.split('+++++')
                    other = json.loads(other)
                    # self.import_package_window = Import_package(self.curr_vul['vul_id'], self.curr_vul['vul_name'], self.curr_vul['introduction'], self.curr_vul['header_key'], self.curr_vul['header_value'], self.curr_vul['body'], self.curr_vul['other'])
                    self.import_package_window = Import_package(vul_id, vul_name, introduction, header_key, header_value, body, other)
                    self.import_package_window.signal_close.connect(self.import_package_window_close_event)
                    self.import_package_window.signal_change.connect(self.import_package_window_change_event)
                    self.import_package_window.show()
                    self.childwindow_import_package = True
            else:
                QMessageBox.warning(self, "提示", '请先装载漏洞！', QMessageBox.Ok)
        except Exception as e:
            print("Exception in main --> " + "pushButton_modify_vul_event", e)

    # 添加header按钮
    def pushButton_add_header_event(self):
        try:
            if self.curr_vul:
                label_text, ok = QInputDialog.getText(self, "输入提示", "请输入header标签名:", QLineEdit.Normal)
                if label_text and ok and label_text not in self.header_labels_dict.keys():
                    self.add_header(label_text)
                    self.curr_vul['header_key'].append(label_text)
            else:
                QMessageBox.warning(self, "提示", '请先装载漏洞！', QMessageBox.Ok)
        except Exception as e:
            print("Exception in main --> " + "pushButton_add_header_event", e)

    # 编辑所有header
    def pushButton_edit_header_event(self):
        try:
            if self.curr_vul:
                if self.pushButton_edit_header.text() == '编辑':
                    for header_label in self.curr_vul['header_key'][1:]:
                        print(self.header_lineEdits_dict['lineEdit_' + header_label].isReadOnly())
                        self.header_lineEdits_dict['lineEdit_' + header_label].setReadOnly(False)
                    self.pushButton_edit_header.setText('确定')
                else:
                    for header_label in self.curr_vul['header_key'][1:]:
                        print(self.header_lineEdits_dict['lineEdit_' + header_label].isReadOnly())
                        self.header_lineEdits_dict['lineEdit_' + header_label].setReadOnly(True)
                    self.pushButton_edit_header.setText('编辑')
            else:
                QMessageBox.warning(self, "提示", '请先装载漏洞！', QMessageBox.Ok)
        except Exception as e:
            print("Exception in main --> " + "pushButton_edit_header_event", e)

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
            print("Exception in main --> " + "toolButton_req_path_event", e)

    # header对应删除按钮
    def header_button_delete_event(self):
        try:
            label_text = self.sender().objectName().split('_', 1)[-1]
            self.del_header(label_text)
        except Exception as e:
            print("Exception in main --> " + "header_button_delete_event", e)

    # 编辑body数据包
    def pushButton_edit_body_event(self):
        try:
            if self.plainTextEdit_body.isReadOnly():
                self.plainTextEdit_body.setReadOnly(False)
                self.pushButton_edit_body.setText('确定')
            else:
                self.plainTextEdit_body.setReadOnly(True)
                self.pushButton_edit_body.setText('编辑')
        except Exception as e:
            print("Exception in main --> " + "pushButton_edit_body_event", e)

    # 信号接受事件槽函数
    def import_package_window_close_event(self):
        self.childwindow_import_package = False

    # 漏洞变动保存配置进数据库
    def import_package_window_change_event(self, vul_id, introduction, header_key, header_value, body, other):
        try:

            self.sqlite.sql_modify_vul(vul_id, 'introduction', introduction)
            self.sqlite.sql_modify_vul(vul_id, 'header_key', '+++++'.join(header_key))
            self.sqlite.sql_modify_vul(vul_id, 'header_value', '+++++'.join(header_value))
            self.sqlite.sql_modify_vul(vul_id, 'body', body)
            self.sqlite.sql_modify_vul(vul_id, 'other', json.dumps(other))
        except Exception as e:
            print("Exception in main --> " + "change_item_writable_event", e)

    # item可编辑状态还原槽函数，当选中的item改变时还原状态并置空记录指针
    def change_item_writable_event(self):
        try:
            if self.writable_item:
                self.writable_item.setFlags(self.writable_item.flags() & ~Qt.ItemIsEditable)
                new_name = self.writable_item.text(0)
                item_id = self.writable_item.data(0, Qt.UserRole)
                self.writable_item = None
                # 修改数据库数据
                self.sqlite.sql_modify_node_name(item_id, new_name)
        except Exception as e:
            print("Exception in main --> " + "change_item_writable_event", e)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # 创建启动界面，支持png透明图片
    splash = QSplashScreen(QPixmap('resource/image/urchin.png'))
    splash.show()

    window = Window()
    window.setWindowIcon(QIcon('resource/image/urchin.png'))
    window.show()

    splash.finish(window)
    sys.exit(app.exec_())
