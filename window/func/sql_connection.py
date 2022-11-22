import sys, os
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtWidgets import QWidget, QMessageBox


class MySQLite(QWidget):
    def __init__(self):
        super(MySQLite, self).__init__()
        self.query = None
        self.db = None
        self.db_connect()
        # self.query = QSqlQuery()

    def db_connect(self):
        flag = False
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        if not os.path.isfile('./db/data.db'):
            flag = True
        self.db.setDatabaseName('./db/data.db')
        if not self.db.open():
            QMessageBox.critical(self, 'Database Connection', self.db.lastError().text())
        elif flag:
            print('数据库初始化')
            self.db_init()

    def db_init(self):
        q = QSqlQuery()
        q.exec_('CREATE TABLE Vul_list (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,name TEXT NOT NULL,"type" INTEGER DEFAULT 0 NOT NULL,vul_id INTEGER DEFAULT 0,father_id INTEGER DEFAULT 0 NOT NULL,CONSTRAINT Vul_list_FK FOREIGN KEY (vul_id) REFERENCES Vul_detail(vul_id))')
        q.exec_('CREATE TABLE Vul_detail (vul_id INTEGER DEFAULT 0 NOT NULL PRIMARY KEY AUTOINCREMENT,introduction TEXT,header_key TEXT,header_value TEXT,body TEXT,other TEXT NOT NULL)')
        q.exec_('CREATE TABLE Config ("attribute" TEXT NOT NULL,"type" TEXT,value1 TEXT,value2 TEXT,CONSTRAINT Config_PK PRIMARY KEY ("attribute"))')
        # q.exec_()

    # 执行自定义sql语句
    def sql_exec(self, sql_code):
        q = QSqlQuery()
        if q.exec_(sql_code):
            print('Sql executed successfully')

    # 查询最新节点数据
    def sql_query_vul_list(self):
        sql_code = 'SELECT * FROM Vul_list order by id'
        q = QSqlQuery(sql_code)
        node_list = []
        if q.exec_(sql_code):
            index_id = q.record().indexOf('id')
            index_name = q.record().indexOf('name')
            index_type = q.record().indexOf('type')
            index_vul_id = q.record().indexOf('vul_id')
            index_father_id = q.record().indexOf('father_id')
            while q.next():
                node = [q.value(index_id), q.value(index_name), q.value(index_type), q.value(index_vul_id), q.value(index_father_id)]
                node_list.append(node)
            return node_list
        else:
            print(q.lastError().text())
            return None

    # 查询节点最新id
    def sql_query_last_id(self):
        sql_code = 'select id from Vul_list order by id desc limit 0,1'
        self.query = QSqlQuery()
        node_id = []
        if self.query.exec_(sql_code):
            # print(self.query.value(0))
            index = self.query.record().indexOf('id')
            while self.query.next():
                node_id.append(self.query.value(index))
            return node_id
        else:
            return None

    # 通过节点id查询漏洞id
    def sql_query_vul_id(self, node_id: int):
        sql_code = 'select vul_id from Vul_list where id = ' + str(node_id)
        self.query = QSqlQuery()
        vul_id = []
        if self.query.exec_(sql_code):
            index = self.query.record().indexOf('vul_id')
            while self.query.next():
                vul_id.append(self.query.value(index))
            return vul_id
        else:
            return None

    # 查询节点类型
    def sql_query_type(self, node_id: int):
        sql_code = 'select type from Vul_list where id=' + str(node_id)
        self.query = QSqlQuery()
        node_type = []
        if self.query.exec_(sql_code):
            index = self.query.record().indexOf('type')
            while self.query.next():
                node_type.append(self.query.value(index))
            return node_type
        else:
            return None

    # 获取最新vul_id
    def sql_query_last_vul_id(self):
        sql_code = 'select vul_id from Vul_detail order by vul_id desc limit 0,1'
        self.query = QSqlQuery()
        vul_id = []
        if self.query.exec_(sql_code):
            index = self.query.record().indexOf('vul_id')
            while self.query.next():
                vul_id.append(self.query.value(index))
            return vul_id
        else:
            return None

    # 通过vul_id查询漏洞名称
    def sql_query_vul_name(self, vul_id):
        sql_code = 'select name from Vul_list where vul_id=' + str(vul_id)
        self.query = QSqlQuery()
        vul_name = []
        if self.query.exec_(sql_code):
            index = self.query.record().indexOf('name')
            while self.query.next():
                vul_name.append(self.query.value(index))
            return vul_name
        else:
            return None

    # 通过vul_id查询漏洞细节
    def sql_query_vul_detail(self, vul_id):
        try:
            sql_code = 'SELECT introduction, header_key, header_value, body, other FROM Vul_detail WHERE vul_id=' + str(vul_id)
            q = QSqlQuery(sql_code)
            vul_detail = ()
            if q.exec_(sql_code):
                index_introduction = q.record().indexOf('introduction')
                index_header_key = q.record().indexOf('header_key')
                index_header_value = q.record().indexOf('header_value')
                index_body = q.record().indexOf('body')
                index_other = q.record().indexOf('other')
                while q.next():
                    vul_detail = (q.value(index_introduction), q.value(index_header_key), q.value(index_header_value), q.value(index_body), q.value(index_other))
                return vul_detail
            else:
                print(q.lastError().text())
                return None
        except Exception as e:
            print("Exception in MySQLite --> " + "sql_query_vul_detail", e)

    # 插入新的节点
    def sql_insert_node(self, data_list):
        try:
            if len(data_list) == 5:
                q = QSqlQuery()
                q.prepare('INSERT INTO Vul_list (id, name, type, vul_id, father_id) VALUES (?, ?, ?, ?, ?)')
                q.addBindValue(int(data_list[0]))
                q.addBindValue(str(data_list[1]))
                q.addBindValue(int(data_list[2]))
                q.addBindValue(int(data_list[3]))
                q.addBindValue(int(data_list[4]))
                if q.exec_():
                    print('已加入新节点: ', data_list)
                    # print('节点id：', self.sql_query_last_id()[0])
                else:
                    print('节点', data_list[0], '添加失败', q.lastError().text())
        except Exception as e:
            print("Exception in MySQLite --> " + "sql_insert_node", e)

    # 插入新的漏洞
    def sql_insert_vul(self, data_list):
        try:
            if len(data_list) == 6:
                q = QSqlQuery()
                q.prepare('INSERT INTO Vul_detail (vul_id, introduction, header_key, header_value, body, other) VALUES (?, ?, ?, ?, ?, ?)')
                q.addBindValue(int(data_list[0]))
                q.addBindValue(str(data_list[1]))
                q.addBindValue(str(data_list[2]))
                q.addBindValue(str(data_list[3]))
                q.addBindValue(str(data_list[4]))
                q.addBindValue(str(data_list[5]))
                if q.exec_():
                    print('[*]已加入新漏洞: ', data_list)
                    # print('漏洞id：', self.sql_query_last_vul_id()[0])
                else:
                    print('[*]漏洞', data_list[0], '添加失败', q.lastError().text())
        except Exception as e:
            print("Exception in MySQLite --> " + "sql_insert_vul", e)

    # 重命名节点名称
    def sql_modify_node_name(self, node_id: int, new_name: str):
        sql_code = 'UPDATE Vul_list SET name=\'' + new_name.replace('\'', '\'\'') + '\' WHERE id=' + str(node_id)
        q = QSqlQuery()
        if q.exec_(sql_code):
            print('更新节点', node_id, '名称成功')
        else:
            print('更新节点', node_id, '名称失败', q.lastError().text())

    # 更改节点指定列数据
    def sql_modify_vul(self, vul_id: int, col: str, new_data):
        sql_code = 'UPDATE Vul_detail SET ' + col + '=\'' + str(new_data).replace('\'', '\'\'') + '\' WHERE vul_id=' + str(vul_id)
        q = QSqlQuery()
        if q.exec_(sql_code):
            print('[*]更新漏洞', vul_id, '成功 -', col, '->', str(new_data))
        else:
            print('[*]更新漏洞', vul_id, '失败', q.lastError().text())

    # 更改系统配置数据
    def sql_modify_config(self):
        pass

    # 删除节点
    def sql_delete_node(self, node_id: int):
        sql_code = 'DELETE FROM Vul_list WHERE id = ' + str(node_id)
        q = QSqlQuery()
        if q.exec_(sql_code):
            print('节点', node_id, '删除成功')
        else:
            print('节点', node_id, '删除失败', q.lastError().text())

    # 删除漏洞
    def sql_delete_vul(self, vul_id: int):
        sql_code = 'DELETE FROM Vul_detail WHERE vul_id = {}'.format(str(vul_id))
        q = QSqlQuery()
        if q.exec_(sql_code):
            print('[*]漏洞', vul_id, '删除成功')
        else:
            print('[*]漏洞', vul_id, '删除失败', q.lastError().text())

    # 关闭数据库连接
    def closeEvent(self, QCloseEvent):
        self.db.close()

