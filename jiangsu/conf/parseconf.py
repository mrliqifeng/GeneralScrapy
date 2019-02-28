import configparser
import os


class ScrapyConf:
    def __init__(self, conf_name):
        self.conf_path = os.getcwd() + "/jiangsu/conf/"
        self.conf_name = self.conf_path + conf_name
        self.conf_dict = self.get_conf_dict()

    def get_conf_dict(self):
        """
        获取配置信息并返回
        :return:返回一个字典，包含所有配置项
        """
        try:
            conf = configparser.ConfigParser()
            conf.read(self.conf_name)
            sections = conf.sections()
            conf_dict = {}
            for se in sections:
                conf_dict[se] = dict(conf.items(se))
            return conf_dict
        except configparser.ParsingError as e:
            print("配置文件出错，请检查")
            print(e)

    def get_scrapy_mysql(self):
        return self.conf_dict.get("scrapy_mysql")

    def get_sqlalchemy(self):
        return self.conf_dict.get("task_mysql").get("url")

    def get_csv_path(self):
        return self.conf_dict.get("scrapy_csv").get("path")

    def get_delay_time(self):
        return self.conf_dict.get("delay").get("delay_time")


class TaskConf:
    def __init__(self, conf_name):
        self.conf_path = os.getcwd() + "/jiangsu/conf/"
        self.conf_name = self.conf_path + conf_name
        self.conf_dict = self.get_conf_dict()

    def get_conf_dict(self):
        """
        获取配置信息并返回
        :return:返回一个字典，包含所有配置项
        """
        try:
            conf = configparser.ConfigParser()
            conf.read(self.conf_name)
            sections = conf.sections()
            conf_dict = {}
            for se in sections:
                conf_dict[se] = dict(conf.items(se))
            return conf_dict
        except configparser.ParsingError as e:
            print("配置文件出错，请检查")
            print(e)

    def get_xslt_file(self):
        return self.conf_path + '/rule/' + self.conf_dict.get('rule').get('rulename')

    def get_uuid(self):
        uuid = self.conf_dict.get("info").get("uuid")
        return uuid

    def get_taskid(self):
        taskid = self.conf_dict.get("info").get("taskid")
        return taskid

    def get_url(self):
        url = self.conf_dict.get("info").get("url")
        return url

    def get_table_name(self):
        table_name = self.conf_dict.get("info").get("user") + "_" + self.conf_dict.get("info").get("taskname")
        return table_name

    def get_csv_name(self):
        table_name = self.conf_dict.get("info").get("user") + "_" + self.conf_dict.get("info").get("taskname") + ".csv"
        return table_name


task_conf = TaskConf("task.ini")
scrapy_conf = ScrapyConf("scrapy.ini")
