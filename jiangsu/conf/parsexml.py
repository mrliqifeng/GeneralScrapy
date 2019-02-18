import lxml

import bs4
from bs4 import BeautifulSoup as bs
from lxml import etree


class ParseXml:

    @staticmethod
    def html_to_xml(html, xslt_name):
        """
        此方法将网页经过xslt文件筛选
        :param html: 网页源码，需要经过编码
        :param xslt_name: xslt文件路径
        :return: 解析过后的xml内容
        """
        try:
            html = etree.HTML(html)
            xslt = etree.XML(open(xslt_name, 'rb').read())
            translate = etree.XSLT(xslt)
            result = translate(html)
            return str(result)
        except lxml.etree.XMLSyntaxError as e:
            raise e

    """
    此类用来解析Xml格式文件，并且从中获取相对应的内容
    """

    def __init__(self, xml_content):

        """
        根据xml内容，初始化BeautifulSoup
        :param xml_content:xml内容
        :arg soup
        :arg depth_tag_dict:xml中所有标签与深度相对的字典s
        :arg all_tags:xml中所有的标签名
        """
        self.soups = bs(xml_content, 'lxml')
        self.depth_tag_dict = self.get_depth_tag_dict()
        self.all_tags = self.get_all_tags()

    def get_item(self, item_name, isEnd=False):
        """
        根据item_name传进来的标签名，查找相应内容
        :param item_name:标签名
        :param isEnd:是否存在结束标识，默认为False
        :return: 如果标签存在内容则且isEnd=False，则返回匹配到的list
                 如果标签存在内容则且isEnd=True，则返回匹配到的String
                 如果标签不存在内容，则返回None
                 如果标签不存在，则返回None
        """
        tags = self.soups.find_all(item_name)  # 查找标签名
        if tags:  # 如果标签名存在
            if isEnd:
                if len(tags) == 1:  # 如果标签长度为1且存在文本内容
                    return str(tags[0].string) if tags[0].string else None
                else:
                    content_string = ""
                    for one in tags:
                        if one.string:
                            content_string += one.string+","
                    return content_string if content_string else None
            else:
                content_list = []
                for one in tags:
                    if one.string:
                        content_list.append(one.string)
                return content_list if content_list else None
        else:  # 不存在则返回None
            return None

    def get_depth_all(self, depth, isEnd=False):
        """
        获取指定深度下的所有内容
        :param depth: 深度，类型为int
        :param isEnd: 是否为最后一级深度
        :return:返回当前深度下 标签名和内容相对应的一个字典
        """
        depth_content_dict = {}
        tag_list = []
        for tag_k, depth_v in self.depth_tag_dict.items():
            if depth_v == str(depth):  # 如果深度为当前深度，则添加相对应的标签名
                tag_list.append(tag_k)
        tag_set = set(tag_list)
        for one_tag in tag_set:
            tag_content = self.get_item(one_tag,isEnd)  # 获取当前标签的内容
            if tag_content:
                depth_content_dict[one_tag] = tag_content
        return depth_content_dict

    def get_depth_tag_dict(self):
        """
        获取xml中所有标签与深度相对的字典
        :return: xml中所有标签与深度相对的字典
        """
        depth_tag_dict = {}
        out = self.soups.body
        if out is None:
            out = self.soups.head
        if out is not None:
            for on in out:
                if isinstance(on, bs4.element.Tag):
                    depth = on.attrs.get('depth')
                    depth_tag_dict[on.name] = depth
        return depth_tag_dict

    def get_all_tags(self):
        """
        获取xml中所有的标签名
        :return:xml中所有的标签名，类型为list
        """
        tag_list = []
        out = self.soups.head
        if out is None:
            out = self.soups.body
        if out is not None:
            for o in out.contents:
                if isinstance(o, bs4.element.Tag):
                    tag_list.append(o.name)
        return list(set(tag_list))
