import os

import pandas
import numpy as np


def clean():
    print()
    douban = pandas.read_csv(os.getcwd() + '\douban.csv', names=['tag', 'info', 'name', 'star', 'people'])
    douban = douban.drop_duplicates().reset_index(drop=True)
    infos = douban['info'].str.split('/')
    authors = []
    date = []
    money = []
    country = []
    error = []
    for num in range(len(infos)):
        # money.append(one[-1])
        if len(infos[num]) >= 3:
            author_info = infos[num][0].strip()
            if len(author_info) > 3:
                if author_info.startswith('(') and author_info.__contains__(')'):
                    authors.append(author_info.split(')')[1])
                    country.append(author_info.split(")")[0].split("(")[1])
                    money.append(infos[num][-1].strip())
                    date.append(infos[num][-2].strip())
                elif author_info.startswith('[') and author_info.__contains__(']'):
                    authors.append(author_info.split(']')[1])
                    country.append(author_info.split("]")[0].split("[")[1])
                    money.append(infos[num][-1].strip())
                    date.append(infos[num][-2].strip())
                elif author_info.startswith('（') and author_info.__contains__('）'):
                    authors.append(author_info.split('）')[1])
                    country.append(author_info.split("）")[0].split("（")[1])
                    money.append(infos[num][-1].strip())
                    date.append(infos[num][-2].strip())
                elif author_info.startswith('【') and author_info.__contains__('】'):
                    authors.append(author_info.split('】')[1])
                    country.append(author_info.split("】")[0].split("【")[1])
                    money.append(infos[num][-1].strip())
                    date.append(infos[num][-2].strip())
                else:
                    error.append(num)
            else:
                country.append('中')
                authors.append(author_info)
                money.append(infos[num][-1].strip())
                date.append(infos[num][-2].strip())
        else:
            error.append(num)
    gudai = '唐宋元明清台台湾'
    country = ["中" if gudai.__contains__(x) else x for x in country]
    douban = douban.drop(index=error).reset_index(drop=True)
    douban['author'] = authors
    douban['money'] = money
    douban['country'] = country
    years = []
    for one in date:
        try:
            years.append(int(one.split("-")[0]))
        except:
            years.append(0)
    douban['year'] = years
    douban = douban[douban['year'] > 1800].reset_index(drop=True)
    douban['people'] = douban['people'].str.split('(').str[1].str.split("人").str[0]
    douban['author'] = douban['author'].str.replace(" ", "")
    douban['tag'] = douban['tag'].str.split(':').str[1].str.strip()
    douban['money'] = douban['money'].str.replace("元", "").str.replace("CNY ", "").str.replace("（全三册）", "").str.replace(
        "NT$ ", "").str.replace("NT$", "").str.replace("NT", "").str.replace(" TWD", "").str.replace("$ ","").str.replace(
        "$", "").str.replace("HKD", "").str.replace("HK$", "")
    money_bak = douban['money']
    index_money = []
    for k in range(len(money_bak)):
        try:
            float(money_bak[k])
        except:
            index_money.append(k)
    douban = douban.drop(index_money).reset_index(drop=True)
    df = douban[douban['people'].isnull()]
    people_index = df.index
    douban = douban.drop(people_index).reset_index(drop=True)
    douban['money'] = douban['money'].astype(float)
    douban['people'] = douban['people'].astype(int)
    douban['star'] = douban['star'].astype(float)
    douban['year'] = douban['year'].astype(int)
    douban = douban.drop(columns=['info'], axis=1)
    douban = douban.drop_duplicates().reset_index(drop=True)
    douban.to_csv("douban_clean.csv", index=None)


if __name__ == '__main__':
    clean()
