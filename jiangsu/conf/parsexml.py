import lxml

import bs4
from bs4 import BeautifulSoup as bs
from lxml import etree


class ParseXml:

    @staticmethod
    def html_to_xml(html, xslt):
        """
        此方法将网页经过xslt文件筛选
        :param html: 网页源码，需要经过编码
        :param xslt_name: xslt文件路径
        :return: 解析过后的xml内容
        """
        try:
            html = etree.HTML(html)
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
        """
        self.soups = bs(xml_content, 'lxml')

    def get_item_by_attr(self, item_name, attr_name, attr_value):
        """
        根据item_name传进来的标签名，查找相应内容
        :param attr_value:
        :param attr_name:
        :param item_name:标签名
        :return: 如果标签存在内容则且isEnd=False，则返回匹配到的list
                 如果标签存在内容则且isEnd=True，则返回匹配到的String
                 如果标签不存在内容，则返回None
                 如果标签不存在，则返回None
        """
        tags = self.soups.find_all(item_name)  # 查找标签名
        if tags:  # 如果标签名存在
            content_list = []
            for one in tags:
                if one.string and one.get(attr_name) == str(attr_value):
                    out = one.string.replace("\n", "").replace("\t", "").strip()
                    content_list.append(out)
            return content_list if content_list else None
        else:  # 不存在则返回None
            return None

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
                    if tags[0].string:
                        out = str(tags[0].string.replace("\n", "").replace("\t", "").strip())
                        return out if out else "empty"
                    else:
                        return "empty"
                else:
                    content_string = ""
                    for one in tags:
                        if one.string:
                            content_string += one.string + ","
                        else:
                            content_string += "empty,"
                    return content_string.replace("\n", "").replace("\t", "").strip() if content_string else "empty"
            else:
                content_list = []
                for one in tags:
                    if one.string:
                        out = one.string.replace("\n", "").replace("\t", "").strip()
                        if out:
                            content_list.append(out)
                        else:
                            content_list.append("empty")
                return content_list if content_list else None
        else:  # 不存在则返回None
            return None

    def get_depth_all(self, depth_num, attr_name="depth", isEnd=False):
        """
        获取指定深度下的所有内容
        :param attr_name:
        :param depth_num: 深度，类型为int
        :param isEnd: 是否为最后一级深度
        :return:返回当前深度下 标签名和内容相对应的一个字典
        """
        depth_content_dict = {}
        tag_list = []
        for tag_k, depth_v in self.get_dict_by_attr(attr_name).items():
            if depth_v == str(depth_num):  # 如果深度为当前深度，则添加相对应的标签名
                tag_list.append(tag_k)
        tag_set = set(tag_list)
        for one_tag in tag_set:
            tag_content = self.get_item(one_tag, isEnd)  # 获取当前标签的内容
            if tag_content:
                depth_content_dict[one_tag] = tag_content
        return depth_content_dict

    def get_attr_all(self, attr_name="depth"):
        """
        获取指定属性下的所有内容
        :param attr_name:
        :param isEnd: 是否为最后一级深度
        :return:返回当前深度下 标签名和内容相对应的一个字典
        """
        depth_content_dict = {}
        for one_tag in self.get_dict_by_attr(attr_name).keys():
            tag_content = self.get_item(one_tag)  # 获取当前标签的内容
            if tag_content:
                depth_content_dict[one_tag] = tag_content
        return depth_content_dict

    def get_dict_by_attr(self, attr_name):
        """
        获取xml中所有标签与属性相对的字典
        :return: xml中所有标签与深度相对的字典
        """
        attr_tag_dict = {}
        out = self.soups.body
        if out is None:
            out = self.soups.head
        if out is not None:
            for on in out:
                if isinstance(on, bs4.element.Tag):
                    if on.attrs.get(attr_name):
                        attr = on.attrs.get(attr_name)
                        attr_tag_dict[on.name] = attr
        return attr_tag_dict

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
