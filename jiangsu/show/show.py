import os
import time

import pandas as pd
import pyecharts as py
from pyecharts.engine import create_default_environment

from jiangsu.show.clean import clean

def tag_bar():
    douban = pd.read_csv(os.getcwd() + "\douban_clean.csv")
    douban2 = douban['star'].groupby(douban['name']).count().to_frame()
    douban2 = douban2[douban2['star'] >= 5].reset_index()
    douban3 = pd.merge(douban2, douban, on='name')
    author_info = douban['name'].groupby(douban['tag']).count()
    author_info = (author_info.reset_index())
    author_info['name'] = author_info['name'].astype('int')
    print(author_info)
    bar = py.Bar(page_title="图书类别数量")
    bar.add("数量", author_info['tag'], author_info['name'], is_more_utils=True, is_label_show=True, is_legend_show=True)
    bar.render('numByTag.html')


def year_line():
    douban = pd.read_csv(os.getcwd() + "\douban_clean.csv")
    douban2 = douban['star'].groupby(douban['name']).count().to_frame()
    douban2 = douban2[douban2['star'] >= 5].reset_index()
    douban3 = pd.merge(douban2, douban, on='name')
    year_info = douban['name'].groupby(douban['year']).count()
    year_info2 = douban['people'].groupby(douban['year']).mean()
    year_info3 = douban['star'].groupby(douban['year']).mean()
    year_info = pd.DataFrame(year_info)
    year_info2 = pd.DataFrame(year_info2)
    year_info3 = pd.DataFrame(year_info3)
    year_all = pd.concat([year_info, year_info2, year_info3], axis=1)
    year_all.index = year_all.index.astype('str')
    year_all = year_all.round(2)
    print(year_all)
    line1 = py.Line(page_title="出版年份与出版数量折线图", width=1200)
    line1.add("出版数量", year_all.index, year_all['name'],
              is_label_show=True,
              mark_point=["average", "max", "min"],
              mark_point_symbol="diamond",
              mark_point_textcolor="#40ff27",
              is_more_utils=True,)

    line2 = py.Line(page_title="出版年份与评价平均人数折线图", width=1800)
    line2.add("评价平均人数", year_all.index, year_all['people'],
              is_label_show=True, is_more_utils=True,)

    line3 = py.Line(page_title="出版年份与评价平均数折线图", width=1800)
    line3.add("评分平均数", year_all.index, year_all['star'],
              is_label_show=True,
              mark_point=["average", "max", "min"],
              mark_point_symbol="diamond",
              mark_point_textcolor="#40ff27",
              is_more_utils=True,)
    line1.render("numByYear1.html")
    line2.render("numByYear2.html")
    line3.render("numByYear3.html")


if __name__ == '__main__':
    clean()
    tag_bar()
    year_line()
