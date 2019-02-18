import sys

from jiangsu.items import JiangsuItem
from jiangsu.send.sendkafka import *

sys.setrecursionlimit(10000)
import scrapy
from scrapy import Request
from jiangsu.conf.parsexml import ParseXml
from jiangsu.spiders.urlproduce import UrlProduce
from jiangsu.conf.parseconf import task_conf

URLPRODUCE = UrlProduce()
print(task_conf.conf_path)
UUID = task_conf.get_uuid()
MQ = get_or_save_mq("pythonjava")


class ZhaotoubiaoSpider(scrapy.Spider):
    """
    此类是爬虫的运行逻辑
    """
    name = 'mySpider'
    num = 1  # 记录当前采集次数

    # start_urls = "https://book.douban.com/tag/%E5%B0%8F%E8%AF%B4"

    # 初始化DataToMysql类实例，此实例用来将爬取的内容写入到mysql数据库

    def start_requests(self):
        #     """
        #     此方法作测试用方法，仅使用部分网页检测规则文件是否可用
        #     :return:
        #     """
        # url = "http://www.ccgp-hainan.gov.cn/cgw/cgw_list.jsp"
        url = "https://book.douban.com/tag/%E5%B0%8F%E8%AF%B4"
        yield Request(url, callback=self.parse)

    def parse(self, response):
        meta = response.meta  # 获取上一级网页传来的meta内容
        this_depth = meta.get('mydepth')  # 获取当前网页深度
        if not this_depth:  # 如果当前深度不存在，则默认为1
            this_depth = 1
        html = response.body  # 获取网页源码
        try:
            html = html.decode('utf-8')
        except:
            pass
            MQ.send_data("网页解码失败，请更换其他解码器")
        try:
            result_xml = ParseXml.html_to_xml(html, task_conf.get_xslt_file())  # 将网页内容经过xslt文件进行筛选
        except Exception as e:
            MQ.send_data("规则文件解析失败，请检查规则文件是否正确")
            raise e
        parse = ParseXml(result_xml)  # 解析筛选过后的xml格式内容
        links = parse.get_item('links')  # 获取当前爬取页面的links标签 （link代表链接）
        next_page = parse.get_item('next_link', isEnd=True)
        if next_page:
            yield Request(response.urljoin(next_page), callback=self.parse)
        if isinstance(links, list):  # 如果links存在且为list对象，说明当前页面还有下一级待爬取的页面
            depth_content_dict = parse.get_depth_all(this_depth)  # 获取当前深度下的所有内容
            depth_content_dict.pop('links')  # 删除链接
            if depth_content_dict.__contains__("next_link"): depth_content_dict.pop('next_link')
            next_depth = this_depth + 1  # 下一级深度
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
                yield Request(response.urljoin(links[num]),
                              meta={"all_depth_meta": all_depth_meta, "mydepth": next_depth, "pageNum": num},
                              callback=self.parse)
        else:  # 如果当前不存在下一级链接，则默认判定为最后一级深度
            all_depth_meta = meta.get('all_depth_meta')  # 获取之前深度传过来的所有的meta数据
            num = meta.get("pageNum")  # 获取页数
            item = JiangsuItem()
            try:
                end_depth_dict = parse.get_depth_all(this_depth, isEnd=True)  # 获取当前深度的所有标签里的内容
                last_depth_dict = all_depth_meta.get(this_depth - 1).get(num)  # 获取上一级深度传过来的内容
                if last_depth_dict:  # 将上一级深度的内容和当前深度的内容整合在一起
                    for k, v in last_depth_dict.items():
                        if v:
                            end_depth_dict[k] = v
                item['info'] = end_depth_dict
                item['num'] = num
                self.num = self.num + 1  # 当前采集次数+1并且打印
                print(item['info'])
                yield item
            except Exception:
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
                    item['info'] = info
                    print(item['info'])
                    yield item
