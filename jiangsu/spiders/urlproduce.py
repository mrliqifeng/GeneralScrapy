class UrlProduce:
    """
    此类用来生成需要采集网页的一个列表
    """

    @staticmethod
    def get_jiangsu_url():
        url_list = []
        caigou = {"shengji": 99, "nanjing": 80, "suzhou": 99, "wuxi": 99, "changzhou": 66, "zhenjiang": 29,
                  "nantong": 66,
                  "taizhou": 63, "yangzhou": 55, "yancheng": 5, "huaian": 99, "suqian": 33, "lianyungang": 14,
                  "xuzhou": 47}
        te = {"yancheng": 15, "nanjing": 15, "suzhou": 15}
        chengjiao = {"shengji": 99, "nanjing": 63, "suzhou": 99, "wuxi": 99, "changzhou": 48, "zhenjiang": 20,
                     "nantong": 16,
                     "taizhou": 60, "yangzhou": 37, "yancheng": 4, "huaian": 88, "suqian": 18, "lianyungang": 11,
                     "xuzhou": 53}
        page_info = {"cggg": te}  # , "gzgg": chengjiao, "htgg": chengjiao
        for type, info in page_info.items():
            for city, num in info.items():
                for page in range(1, num + 1):
                    url = "http://www.ccgp-jiangsu.gov.cn/cgxx/%s/%s/index_%d.html" % (type, city, page)
                    url_list.append(url)
        return url_list

    @staticmethod
    def get_hainan_url():
        url_list = []
        for num in range(1, 1797):
            url = "http://www.ccgp-hainan.gov.cn/cgw/cgw_list_gglx.jsp?currentPage=%d" % num
            url_list.append(url)
        return url_list

    @staticmethod
    def get_douban_url():
        url_list = []
        for num in range(0, 13):
            url = "https://book.douban.com/tag/%E5%B0%8F%E8%AF%B4?start={}&type=T".format(num * 20)
            # url2 = "https://book.douban.com/tag/%E6%96%87%E5%AD%A6?start={}&type=T".format(num * 20)
            # url5 = "https://book.douban.com/tag/%E9%9A%8F%E7%AC%94?start={}&type=T".format(num * 20)
            # url3 = "https://book.douban.com/tag/%E6%95%A3%E6%96%87?start={}&type=T".format(num * 20)
            # url4 = "https://book.douban.com/tag/%E8%AF%97%E6%AD%8C?start={}&type=T".format(num * 20)
            url_list.append(url)
            # url_list.append(url2)
            # url_list.append(url3)
            # url_list.append(url4)
            # url_list.append(url5)

        return url_list


if __name__ == '__main__':
    UrlProduce.get_douban_url()
