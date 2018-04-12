#!/usr/bin/python
# -*- coding:utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        actionSQL.py
#
# Author:      WangKun
#
# Created:     06/18/2017
#
# Copyright:   (c) XLY_WK 2017
#-------------------------------------------------------------------------------

import sys
import sqlite3 # 引用数据库接口

class SQLite3Action(object):
    def __init__(self, sqldb = 'test.db'):
        # 连接数据库
        self.conn = sqlite3.connect(sqldb) # 创建/链接数据库
        self.conn.isolation_level = None #这个就是事务隔离级别，默认是需要自己commit才能修改数据库，置为None则自动每次修改都提交,否则为""
        print ("Opened database successfully")
        self.func = ['create', 'drop', 'insert', 'select', 'update', 'delete']

    def closesql(self):
        # 关闭数据库
        self.conn.close()

    def _run(self, function_name, sql):
        # 执行sql的API
        res = self.conn.execute(sql)
        print ("Table {0} successfully".format(function_name))
        if function_name == 'select':
            return res.fetchall()
        elif function_name == 'insert':
            return res.execute('select last_insert_rowid();').fetchall()
        return None

    def create(self, table, args):
        # 创建数据表
        fname = sys._getframe().f_code.co_name
        sql = 'CREATE TABLE IF NOT EXISTS {0} {1};'.format(table, args)
        return self._run(fname, sql)
        
    def drop(self, table):
        # 如果存在就删除数据表
        fname = sys._getframe().f_code.co_name
        sql = 'DROP TABLE IF EXISTS `{0}`;'.format(table)
        return self._run(fname, sql)
        
    def insert(self, table, kargs):
        # 添加数据
        fname = sys._getframe().f_code.co_name
        keys =  ','.join(['"' + str(key) + '"' for key in kargs.keys()])
        values =  ','.join(['"' + str(value) + '"' for value in kargs.values()])
        sql = "INSERT INTO {0} ({1}) VALUES ({2});".format(table,keys, values)
        return self._run(fname, sql)
        
    def select(self, table, fields='*', contions='1=1'): 
        fname = sys._getframe().f_code.co_name
        if not contions:
            contions = '1=1'
        sql = "SELECT {0} from {1} where {2};".format(fields, table, contions)
        return self._run(fname, sql)
        
    def update(self, table, upkey, upvalue, keyid, keyvalue ):
        # 修改数据
        fname = sys._getframe().f_code.co_name
        sql = "UPDATE {0} set {1} = {2} where {3}={4};".format(table, upkey, upvalue, keyid, keyvalue)
        return self._run(fname, sql)
        
    def delete(self, table, keyid, keyvalue):
        # 删除数据
        fname = sys._getframe().f_code.co_name
        sql = "DELETE from {0} where {1}={2};".format(table, keyid, keyvalue)
        return self._run(fname, sql)

if __name__=='__main__':
    # ID  INTEGER PRIMARY KEY NOT NULL,
    # NAME           TEXT    NOT NULL,
    # AGE            INT     NOT NULL,
    # ADDRESS        CHAR(50),
    # SALARY         REAL
    sqlA = SQLite3Action('URI.DB')
    table = 'WEBSITES'
    args = '''(
	ID  INTEGER PRIMARY KEY NOT NULL,
        NAME           TEXT    NOT NULL,
        langageclass   CHAR(50),
        state          INT     NOT NULL
	)'''
    # sqlA.drop(table)
    print (sqlA.create(table, args))
    table = 'URLS'
    args = '''(
	ID  INTEGER PRIMARY KEY NOT NULL,
        NAME           TEXT    NOT NULL,
        siteid            INT     NOT NULL
	)'''
    print (sqlA.create(table, args))
    # kargs = {'NAME':'Paul','siteid': 1}
    # print (sqlA.insert(table, kargs))
    # kargs = {'NAME':'Paul','AGE': 32,'ADDRESS':'California','SALARY': 20000.00}
    # print (sqlA.insert(table, kargs))
    # print (sqlA.select(table))
    # print (sqlA.update(table, 'SALARY', '25000.00', 'ID', '1'))
    # print (sqlA.delete(table, 'ID', 2))
