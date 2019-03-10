import pymysql
import csv
import pandas as pd
from jiangsu.send.sendkafka import *
from jiangsu.conf.parseconf import task_conf

MQ = get_or_save_mq("pythonjava")


class DataToMysql:
    def __init__(self, host, user, pwd, db, table, port=3306, **kwargs):
        try:
            if not isinstance(port, int):
                port = int(port)
            self.conn = pymysql.connect(host=host, user=user, passwd=pwd, db=db,
                                        port=port, charset='utf8')  # 链接数据库
            self.cursor = self.conn.cursor()
            self.table = table
        except pymysql.Error as e:
            MQ.send_data("数据库连接信息报错")
            print("数据库连接信息报错")
            raise e

    def write(self, info_dict, table_name=None):
        """
        根据table_name与info自动生成建表语句和insert插入语句
        :param table_name: 数据需要写入的表名
        :param info_dict: 需要写入的内容，类型为字典
        :return:
        """
        if not table_name:
            table_name = self.table
        sql_key = ''  # 数据库行字段
        sql_value = ''  # 数据库值
        for key in info_dict.keys():  # 生成insert插入语句
            sql_value = (sql_value + '"' + pymysql.escape_string(info_dict[key]) + '"' + ',')
            sql_key = sql_key + ' ' + key + ','

        try:
            self.cursor.execute(
                "INSERT INTO %s (%s) VALUES (%s)" % (table_name, sql_key[:-1], sql_value[:-1]))
            self.conn.commit()  # 提交当前事务
        except pymysql.Error as e:
            if str(e).split(',')[0].split('(')[1] == "1146":  # 当表不存在时，生成建表语句并建表
                sql_key_str = ''  # 用于数据库创建语句
                columnStyle = ' text'  # 数据库字段类型
                for key in info_dict.keys():
                    sql_key_str = sql_key_str + ' ' + key + columnStyle + ','
                self.cursor.execute("CREATE TABLE %s (%s)" % (table_name, sql_key_str[:-1]))
                self.cursor.execute("INSERT INTO %s (%s) VALUES (%s)" %
                                    (table_name, sql_key[:-1], sql_value[:-1]))
                self.conn.commit()  # 提交当前事务
            else:
                MQ.send_data(str(e))


class DataToCSV:
    def __init__(self, path, **kwargs):
        try:
            f = open(path, 'w', encoding='utf-8', newline='')
            self.writer = csv.writer(f)
        except FileNotFoundError as e:
            MQ.send_data('No such file or directory: %s' % path)
            raise e
        except PermissionError as e:
            MQ.send_data("此文件正被占用")
            raise e

    def write(self, info_dict):
        self.writer.writerow(info_dict.values())


def getCunchu(func, **kwargs):
    if func == 'csv':
        return DataToCSV(**kwargs)
    elif func == 'mysql':
        return DataToMysql(**kwargs)
    else:
        print('请输入正确的存储方式')


if __name__ == '__main__':
    dm = DataToMysql(host="localhost", user="root", pwd="000000", db="xiapu", table="info")
    data = pd.read_csv("info.csv")
    print(data.head(10))
