import os

from lxml import etree
import requests

from jiangsu.test.te2 import ParseXml


def html_to_xml(html):
    doc = etree.HTML(html)
    xslt = etree.XML(open('C:\\Users\\Liqifeng\Desktop\GeneralScrapy2\\douban.xml', 'rb').read())
    xs = etree.XSLT(xslt)
    result = xs(doc)
    return str(result)


def get_item_by_depth(soup, item_name, depth):
    """
    根据item_name传进来的标签名，查找相应内容
    :param item_name:标签名
    :param isEnd:是否存在结束标识，默认为False
    :return: 如果标签存在内容则且isEnd=False，则返回匹配到的list
             如果标签存在内容则且isEnd=True，则返回匹配到的String
             如果标签不存在内容，则返回None
             如果标签不存在，则返回None
    """
    tags = soup.find_all(item_name)  # 查找标签名
    if tags:  # 如果标签名存在
        content_list = []
        for one in tags:
            if one.string and one["depth"] == str(depth):
                out = one.string.replace("\n", "").replace("\t", "").strip()
                content_list.append(out)
        return content_list if content_list else None
    else:  # 不存在则返回None
        return None


if __name__ == "__main__":
    # doc = requests.get("https://book.douban.com/tag/%E5%B0%8F%E8%AF%B4")
    xml_path = "C:\\Users\\Liqifeng\Desktop\GeneralScrapy2\\douban.xml"
    xslt = open(xml_path, 'r').read()
    print(xslt.__contains__("next_link_depth"))
    # xml_result = ParseXml.html_to_xml(doc.text, xml_path)
    # xml_html = ParseXml(xml_result)
    # soup = xml_html.soups
    # print(soup.find_all("links"))
    # print(get_item_by_depth(soup, "info", 1))
    # path = xml_html.get_attr_all("link_depth")
    # next_links_dict = {'next_link1': ['next_link1','next_link1'], 'next_link2': ['next_link2','next_link2'],'next_link3': ['next_link3','next_link3']}
    # next_links_keys = sorted(next_links_dict.keys())
    # one_next_links = next_links_dict.get(next_links_keys[1])
    # print(one_next_links)
    # print(xml_html.get_item("links", isEnd=True))
    # parse = ParseXml(xml)
    # print(parse.get_item('next_link'))
