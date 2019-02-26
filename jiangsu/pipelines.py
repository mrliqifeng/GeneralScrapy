# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

from jiangsu.sql.scrapysql import getCunchu
from jiangsu.send.sendkafka import *
from jiangsu.sql.tasksql import *
from jiangsu.conf.parseconf import task_conf
from jiangsu.conf.parseconf import scrapy_conf

UUID = task_conf.get_uuid()
TASKID = task_conf.get_taskid()
MQ = get_or_save_mq("pythonjava")
KA = get_or_save_ka("spark")


class JiangsuPipeline(object):
    def __init__(self):
        print("****************__init__*******************")
        mysql_conf = scrapy_conf.get_scrapy_mysql()
        mysql_conf['table'] = task_conf.get_table_name()
        csv_conf = scrapy_conf.get_csv_path() + task_conf.get_table_name() + '.csv'
        self.cunchu_list = []
        self.cunchu_list.append(getCunchu("mysql", **mysql_conf))
        self.cunchu_list.append(getCunchu("csv", **{"path": csv_conf}))

    def process_item(self, item, spider):
        for one in self.cunchu_list:
            one.write(item['info'])
        # print(type(item['info']))
        KA.send_data(json.dumps(item['info']))
    def close_spider(self, spider):
        print("****************close_spider*******************")
        update_status(0, TASKID)
        MQ.send_data("爬虫已结束运行")
