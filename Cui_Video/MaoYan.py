'''
内容：
	爬取猫眼电影排行Top250
使用：
	1. Requests库
	2. re库
	3. json库
	4. Multiprocessing库中dummy方法
'''

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author  : Chauncey-chen

import json
from multiprocessing.dummy import Pool as ThreadPool

import requests
import time
from requests.exceptions import RequestException
import re


def get_one_page(offset):
    '''
    解析文本，获得请求
    '''
    url = "http://maoyan.com/board/4?offset={}".format(offset)
    headers = {
            'user-agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0',
        }
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        return r.text
    except RequestException:
        return "Error"


def parse_one_page(html):
    pattern = re.compile(r'<dd>.*?<i.*?board-index.*?>(\d+)</i>.*?' +
                         'data-src="(.*?)".*?name"><a.*?>(.*?)</a>'+
                         '.*?star">(.*?)</p>.*?releasetime">(.*?)</p>'+
                         '.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>', re.S)
    info = re.findall(pattern, html)
    for item in info:
        yield {
            'index': item[0],
            'image_url': item[1],
            'title': '<<'+item[2]+'>>',
            'actor': item[3].strip()[3:],
            'time': item[4].strip()[5:],
            'score': item[5]+item[6]
        }


def save_file(content):
    with open('result.txt', 'a' ,encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')
        # json.dumps(xx)将字典转换为字符串
        # 但是对于中文，dumps会转换为ascii编码，加上ensure_ascii=False解决


def main(offset):
    html = get_one_page(offset)
    # print(html)
    for item in parse_one_page(html):
        # print(item)
        save_file(item)


if __name__ == '__main__':

    # offset 为：0, 10, 20, 30, 40, 50, 60, 70, 80, 90
    offset = 10

    # 单进程
    t1 = time.clock()
    for i in range(offset):
        res = get_one_page(i*10)
        for info in parse_one_page(res):
            # print(info)
            save_file(info)
    t2 = time.clock()
    print(t2 - t1)           # 3.2487624623265137


    # 多进程红线程dummy形式
    t3 = time.clock()
    p = ThreadPool(4)
    # p.map(main, [i*10 for i in range(10)])
    res = p.map(get_one_page, [i*10 for i in range(10)])
    for item in res:
        for info in parse_one_page(item):
            # print(info)
            save_file(info)
    t4 = time.clock()
    print(t4 - t3)          # 0.6742832772483505

    # 操作整个过程的多进程
    t5 = time.clock()
    for i in range(offset):
        main(i*10)
    t6 = time.clock()
    print(t6 - t5)
		
'''
1.测试结果：
	2.1939430498903576
	0.7281949910085377
	2.014040821353269
2.由于不太清楚爬虫多线程设计策略, 故而多写出几个不同的爬取方法作比较, 先 埋个坑, 后面来填坑
'''
