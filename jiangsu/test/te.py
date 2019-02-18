import os

from lxml import etree
import requests


def html_to_xml(html):
    doc = etree.HTML(html)
    xslt = etree.XML(open(os.getcwd()+'\jiangsu\guize\douban.xml', 'rb').read())
    xs = etree.XSLT(xslt)
    result = xs(doc)
    return str(result)


if __name__ == "__main__":
    doc = requests.get("https://book.douban.com/tag/%E5%B0%8F%E8%AF%B4")
    # doc = requests.get("http://www.ccgp-hainan.gov.cn/cgw/cgw_list.jsp")
    # doc = requests.get("https://book.douban.com/subject/26878124/")
    # soup = bs(doc, 'lxml')
    # source = soup.select("body > div.neibox > div.neibox02 > div.box > div > div.nei03_02")[0]
    # source = soup.select("body > div.neibox > div.neibox02 > div.box > div > div.nei03_02")
    # print(source)
    # print(doc.text)
    xml = html_to_xml(doc.text)
    print(xml)
    # parse = ParseXml(xml)
    # print(parse.get_item('next_link'))

