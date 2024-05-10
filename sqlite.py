# -*- coding:utf-8 -*-

import sys
import os
import sqlite3
import threading

class SqliteTool():
    """
       简单sqlite数据库工具类
       编写这个类主要是为了封装sqlite，继承此类复用方法
       """
    def __init__(self, dbName="sunoapi.db"):
        """
        初始化连接——使用完需关闭连接
        :param dbName: 连接库的名字，注意，以'.db'结尾
        """
        # # 连接数据库
        # conn = sqlite3.connect(dbName, check_same_thread = False)
        # # 创建游标
        # cur = conn.cursor()
    def create_conn(self):
        return sqlite3.connect('sunoapi.db', isolation_level=None)
    # # 创建数据表
    # def create_tabel(self, sql: str):
    #     """
    #     创建表
    #     :param sql: create sql语句
    #     :return: True表示创建表成功
    #     """
    #     try:
    #         conn = self.create_conn()
    #         with conn:
    #             cur = conn.cursor()
    #             cur.execute(sql)
    #             conn.commit()
    #             print("[create table success]")
    #             return True
    #     except Exception as e:
    #         print("[create table error]", e)
    # # 删除数据表
    # def drop_table(self, sql: str):
    #     """
    #     删除表
    #     :param sql: drop sql语句
    #     :return: True表示删除成功
    #     """
    #     try:
    #         conn = self.create_conn()
    #         with conn:
    #             cur = conn.cursor()
    #             cur.execute(sql)
    #             conn.commit()
    #             return True
    #     except Exception as e:
    #         print("[drop table error]", e)
    #         return False
    # 插入或更新表数据，一次插入或更新一条数据
    def operate_one(self, sql: str, value: tuple):
        """
        插入或更新单条表记录
        :param sql: insert语句或update语句
        :param value: 插入或更新的值，形如（）
        :return: True表示插入或更新成功
        """
        try:
            conn = self.create_conn()
            with conn:
                cur = conn.cursor()
                cur.execute(sql, value)
                conn.commit()
                if 'INSERT' in sql.upper():
                    pass
                    # print(f"[insert one record success]:{sql}")
                if 'UPDATE' in sql.upper():
                    pass
                    # print(f"[update one record success]:{sql}")
                return True
        except Exception as e:
            print(f"[insert/update one record error]:{sql}", e)
            return False
    # 插入或更新表数据，一次插入或更新多条数据
    def operate_many(self, sql: str, value: list):
        """
        插入或更新多条表记录
        :param sql: insert语句或update语句
        :param value: 插入或更新的字段的具体值，列表形式为list:[(),()]
        :return: True表示插入或更新成功
        """
        try:
            conn = self.create_conn()
            with conn:
                cur = conn.cursor()
                cur.executemany(sql, value)
                conn.commit()
                if 'INSERT' in sql.upper():
                    print(f"[insert many  records success]:{sql}")
                if 'UPDATE' in sql.upper():
                    print(f"[update many  records success]:{sql}")
                return True
        except Exception as e:
            print(f"[insert/update many  records error]:{sql}", e)
            return False
    # 删除表数据
    def delete_record(self, sql: str):
        """
        删除表记录
        :param sql: 删除记录SQL语句
        :return: True表示删除成功
        """
        try:
            conn = self.create_conn()
            with conn:
                cur = conn.cursor()
                if 'DELETE' in sql.upper():
                    cur.execute(sql)
                    conn.commit()
                    print(f"[detele record success]:{sql}")
                    return True
                else:
                    print(f"[sql is not delete]:{sql}")
                    return False
        except Exception as e:
            print(f"[detele record error]:{sql}", e)
            return False
    # 查询一条数据
    def query_one(self, sql: str, params=None):
        """
        查询单条数据
        :param sql: select语句
        :param params: 查询参数，形如()
        :return: 语句查询单条结果
        """
        try:
            conn = self.create_conn()
            with conn:
                cur = conn.cursor()
                if params:
                    cur.execute(sql, params)
                else:
                    cur.execute(sql)
                # 调用fetchone()方法
                r = cur.fetchone()
                # print(f"[select one record success]:{sql}")
                return r
        except Exception as e:
            print(f"[select one record error]:{sql}", e)
    # 查询多条数据
    def query_many(self, sql: str, params=None):
        """
        查询多条数据
        :param sql: select语句
        :param params: 查询参数，形如()
        :return: 语句查询多条结果
        """
        try:
            conn = self.create_conn()
            with conn:
                cur = conn.cursor()
                if params:
                    cur.execute(sql, params)
                else:
                    cur.execute(sql)
                # 调用fetchall()方法
                r = cur.fetchall()
                print(f"[select many records success]:{sql}")
                return r
        except Exception as e:
            print(f"[select many records error]:{sql}", e)