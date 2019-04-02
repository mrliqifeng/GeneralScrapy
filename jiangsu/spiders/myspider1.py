import sys
from lxml import etree
from jiangsu.items import JiangsuItem
from jiangsu.send.sendkafka import *

sys.setrecursionlimit(10000)
import scrapy
from scrapy import Request
from jiangsu.conf.parsexml import ParseXml
from jiangsu.spiders.urlproduce import UrlProduce
from jiangsu.conf.parseconf import task_conf

URLPRODUCE = UrlProduce()
UUID = task_conf.get_uuid()
MQ = get_or_save_mq("pythonjava")
XSLT = etree.XML(open(task_conf.get_xslt_file(), 'rb').read())
XPATH_CONTENT = open(task_conf.get_xslt_file(), 'r', encoding="utf-8").read()


def get_parse(response):
    """
    根据返回的response，返回解析过后的xml格式内容
    :param response:
    :return:
    """
    html = response.body  # 获取网页源码
    try:
        html = html.decode('utf-8')
    except:
        pass
        MQ.send_data("网页解码失败，请更换其他解码器")
    try:
        result_xml = ParseXml.html_to_xml(html, XSLT)  # 将网页内容经过xslt文件进行筛选
    except Exception as e:
        MQ.send_data("规则文件解析失败，请检查规则文件是否正确")
        raise e
    parse = ParseXml(result_xml)  # 解析筛选过后的xml格式内容
    return parse


class ZhaotoubiaoSpider(scrapy.Spider):
    """
    此类是爬虫的运行逻辑
    """
    name = 'mySpider'
    num = 1  # 记录当前采集次数

    def start_requests(self):
        url = task_conf.get_url()
        if task_conf.get_zuhe_link() == "true":
            yield Request(url, callback=self.parse_next_link)
        else:
            yield Request(url, callback=self.parse)

    def parse_next_link(self, response):
        """
        进行组合链接爬取
        :param response:
        :return:
        """
        meta = response.meta
        print(meta)
        this_link_depth = meta.get('this_link_depth')  # 获取当前网页深度
        if not this_link_depth:  # 如果当前深度不存在，则默认为1
            this_link_depth = 1
        parse_xml = get_parse(response)
        tag_name = "next_link" + str(this_link_depth)
        next_links = parse_xml.get_item_by_attr(tag_name, "next_link_depth", this_link_depth)
        if XPATH_CONTENT.__contains__("next_link" + str(this_link_depth + 1)):
            for one_next_link in next_links:
                yield Request(response.urljoin(one_next_link), callback=self.parse_next_link,
                              meta={"this_link_depth": this_link_depth + 1})
        else:
            for one_next_link in next_links:
                yield Request(response.urljoin(one_next_link), callback=self.parse)

    def parse(self, response):
        meta = response.meta  # 获取上一级网页传来的meta内容
        this_depth = meta.get('mydepth')  # 获取当前网页深度
        if not this_depth:  # 如果当前深度不存在，则默认为1
            this_depth = 1
        parse = get_parse(response)
        links = parse.get_item('links')  # 获取当前爬取页面的links标签 （link代表链接）
        next_page = parse.get_item('next_page', isEnd=True)
        if next_page:
            yield Request(response.urljoin(next_page), callback=self.parse)
        if isinstance(links, list):  # 如果links存在且为list对象，说明当前页面还有下一级待爬取的页面
            depth_content_dict = parse.get_depth_all(this_depth)  # 获取当前深度下的所有内容
            depth_content_dict.pop('links')  # 删除链接
            if depth_content_dict.__contains__("next_page"): depth_content_dict.pop('next_page')
            next_key = list(depth_content_dict.keys())
            len_links = len(links)  # 此级深度链接的长度
            for num in range(len(links)):
                all_depth_meta = meta.get('all_depth_meta')  # 获取上一级深度传过来的内容
                if not all_depth_meta:
                    all_depth_meta = {}
                all_depth_meta[this_depth] = {}  # 为当前深度创建一个列表，存储当前深度所采集到的内容
                next_meta = None
                if len(depth_content_dict) > 0:  # 如果当前深度除了链接没有要采集的内容，则不操作
                    next_meta = {}
                    for k in next_key:
                        if len_links == len(depth_content_dict.get(k)):
                            next_meta[k] = depth_content_dict.get(k)[num]
                        elif len(depth_content_dict.get(k)) == 1:
                            next_meta[k] = depth_content_dict.get(k)[0]
                        else:
                            next_meta[k] = None
                all_depth_meta[this_depth][num] = next_meta
                print(all_depth_meta)
                yield Request(response.urljoin(links[num]),
                              meta={"all_depth_meta": all_depth_meta, "mydepth": this_depth + 1, "pageNum": num},
                              callback=self.parse)
        else:  # 如果当前不存在下一级链接，则默认判定为最后一级深度
            item = JiangsuItem()
            if meta.get('all_depth_meta') is not None:
                all_depth_meta = meta.get('all_depth_meta')  # 获取之前深度传过来的所有的meta数据
                num = meta.get("pageNum")  # 获取页数
                end_depth_dict = parse.get_depth_all(this_depth, isEnd=True)  # 获取当前深度的所有标签里的内容
                last_depth_dict = all_depth_meta.get(this_depth - 1).get(num)  # 获取上一级深度传过来的内容
                if last_depth_dict:  # 将上一级深度的内容和当前深度的内容整合在一起
                    for k, v in last_depth_dict.items():
                        if v:
                            end_depth_dict[k] = v
                end_depth_dict['source_url'] = response.url
                end_depth_dict['taskname'] = task_conf.get_taskname()
                end_depth_dict['scrapy_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                item['info'] = end_depth_dict
                item['num'] = num
                self.num = self.num + 1  # 当前采集次数+1并且打印
                yield item
            else:
                end_depth_dict = parse.get_depth_all(this_depth)  # 获取当前深度的所有标签里的内容
                out = {}
                for key, value in end_depth_dict.items():
                    for num in range(len(value)):
                        di = {key: value[num]}
                        if num in out.keys():
                            out[num].append(di)
                        else:
                            li = [di]
                            out[num] = li
                for k, v in out.items():
                    info = {}
                    for one in v:
                        for key, value in one.items():
                            info[key] = value
                    info['source_url'] = response.url
                    info['taskname'] = task_conf.get_taskname()
                    info['scrapy_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                    item['info'] = info
                    yield item
