# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import time

import redis
from scrapy import signals
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
from jiangsu.conf.parseconf import scrapy_conf, task_conf
from jiangsu.sql.scrapysql import DataToMysql


class JiangsuSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class DuplicatesMiddleware(object):
    def __init__(self):
        print("启动增量引擎*******************")
        self.table_name = task_conf.get_table_name()
        conn = DataToMysql(**scrapy_conf.get_scrapy_mysql()).conn
        self.redis_db = redis.Redis(host='127.0.0.1', port=6379, db=1)
        self.redis_db.flushdb()
        sql = "SELECT source_url FROM %s ;" % self.table_name
        df = pd.read_sql(sql, conn)
        for url in df["source_url"].get_values():  # 把每一条的值写入key的字段里
            self.redis_db.hset(self.table_name, url, 0)

    def process_request(self, request, spider):
        if request.meta.get("pageNum") is not None:
            if self.redis_db.hexists(self.table_name,
                                     request.url):  # 取item里的url和key里的字段对比，看是否存在，存在就丢掉这个item。不存在返回item给后面的函数处理
                return HtmlResponse(url=request.url, status=404, request=request)

    def spider_closed(self, spider):
        print("关闭去重方法")


class SeleniumMiddleware(object):
    def __init__(self):
        print("启动动态引擎*********************")
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        prefs = {"profile.managed_default_content_settings.images": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        chrome_options.add_argument('user-agent="Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"')
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        self.driver.set_page_load_timeout(1000)

    def __del__(self):
        self.driver.close()

    def process_request(self, request, spider):
        try:
            self.driver.get(request.url)
            return HtmlResponse(url=request.url, body=self.driver.page_source,
                                request=request, encoding="utf-8", status=200)

        except:
            print("动态网页抓取失败")
            return HtmlResponse(url=request.url, status=404, request=request)

    def spider_closed(self, spider):
        self.driver.close()


class JiangsuDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        print(request.url)
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
