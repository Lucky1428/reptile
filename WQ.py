# -*- coding: utf-8 -*-
"""
Created on Tue Sep 27 15:49:13 2022

@author: yanyan
"""

# from fake_useragent import UserAgent
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time  
import csv


option = webdriver.ChromeOptions()
option.add_argument('headless')  # 设置option
driver = webdriver.Chrome()



rain_total = pd.DataFrame([])
#
#
url = 'https://szzdjc.cnemc.cn:8070/GJZ/Business/Publish/RealDatas.html'
driver.get(url)

driver.find_element(By.ID,'ddm_Area').click()
time.sleep(2)
driver.find_element(By.LINK_TEXT,'全国').click()
time.sleep(10)
soup = BeautifulSoup(driver.page_source,"lxml")
#
driver.close()
dq=soup.find_all(class_='dq')
ly=soup.find_all(class_='ly')
loc=soup.find_all(class_='MN')
dt=soup.find_all(class_='dt')
wt=soup.find_all(class_='sp_wt')
parm=soup.find_all(class_='parm')

#处理地区
city=[]
n=1
for i in dq:
    if n==1:
        city.append('省份')
        n=n+1
    else:
        i=str(i)
        begin=i.find('n>')+2
        end=i.find('</')
        city.append(i[begin:end])
#处理流域
drainage_basin=[]
n=1
for i in ly:
    if n==1:
        drainage_basin.append('流域')
        n=n+1
    else:
        i=str(i)
        begin=i.find('n>')+2
        end=i.find('</')
        drainage_basin.append(i[begin:end])
#处理断面名称,与河流名,地级市
dm=[]
rvnm=[]
ds=[]
n=1
for i in loc:
    if n==1:
        dm.append('断面名称')
        rvnm.append('河流名')
        ds.append('地级市')
        n=n+1
    else:
        i=str(i)
        begin=i.find('"">')+3
        end=i.find('</')
        dm.append(i[begin:end])
        begin=i.find('市:')+2
        end=i.find('\n')
        ds.append(i[begin:end])
        begin=i.find('河流:')+3
        end=i.find('" data')
        rvnm.append(i[begin:end])
#时间
time=[]
n=1
for i in dt:
    if n==1:
        time.append('时间')
        n=n+1
    else:
        i=str(i)
        begin=i.find('>')+1
        end=i.find('</')
        time.append(i[begin:end])
#水质
sz=[]
n=1
sz.append('水质')
for i in wt:
    i=str(i)
    begin=i.find('>')+1
    end=i.find('</')
    sz.append(i[begin:end])
#其它数据
data = [[0] * 11 for _ in range(int(len(parm)/11 ))]
for i in range(int(len(parm)/11 )):
    for j in range(11):
        if i==0:
            begin=str(parm[i*11+j]).find('>')+1
            end=str(parm[i*11+j]).find('<br/>')
            b=str(parm[i*11+j]).find('t">')+3
            e=str(parm[i*11+j]).find('</')
            data[i][j]=str(parm[i*11+j])[begin:end]+str(parm[i*11+j])[b:e]
        else:
            begin=str(parm[i*11+j]).find('：')+1
            end=str(parm[i*11+j]).find('" data')
            data[i][j]=str(parm[i*11+j])[begin:end]
            if len(data[i][j])>20:
                data[i][j]='*'
        
        
        
## 保存数据
with open('0127.csv', 'w', encoding='utf-8-sig', newline='') as file:
    writer = csv.writer(file)
    for i in range(len(dm)):
        l=[]
        l.append(city[i])
        l.append(ds[i])
        l.append(drainage_basin[i])
        l.append(rvnm[i])
        l.append(dm[i])
        l.append(time[i])
        l.append(sz[i])
        for j in range(11):
            l.append(data[i][j])
        writer.writerow(l)


    
    