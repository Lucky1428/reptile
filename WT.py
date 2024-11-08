# -*- coding: utf-8 -*-
"""
Created on Tue Sep 27 15:49:13 2022

@author: yanyan
"""

import requests
from fake_useragent import UserAgent
import csv

# 获取网页信息的通用框架
def getHtmlText(url):
#    try:
        headers= {'User-Agent':str(UserAgent().random)}
        r = requests.get(url,timeout=100,headers=headers)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
#    except:
#        return '爬取失败'
    
demo=getHtmlText('http://xxfb.mwr.cn/hydroSearch/greatRiver')
start=demo.find('[')+2
end=demo.find(']')-1
data=demo[start:end].split('},{')
store = [[0]*len(data[1].split(',')) for _ in range(len(data))]
n=0
for i in data:
    q=i.split(',')
    for j in range(len(q)):
        if j==0 :
            store[n][j]=q[j].split(':')[1]+':'+q[j].split(':')[2]
        else:
            store[n][j]=q[j].split(':')[1]
    n=n+1
title=[]
for i in q:
    title.append(i.split(':')[0][1:-1])


with open('0127.csv', 'w', encoding='utf-8-sig', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(title)
    writer.writerows(store)
    
    
    