#coding=utf-8
#从几大卫计委的网站上抓取助产专业招聘信息并写入Excel文件
#copyright@BillyCui

#import json
#import os
import re
import csv
#import string

import requests
from bs4 import BeautifulSoup

#import pymysql

url='http://www.nbwjw.gov.cn/col/col144/index.html'
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
headers = { 'User-Agent' : user_agent }
r = requests.get(url,headers=headers)  #连接
content = r.text #获取内容，自动转码unicode

soup = BeautifulSoup(content,"lxml")

tags = soup.find_all('script',language = 'javascript')

tagstr = tags[3]

tagstr = ''.join(tagstr)

rgs = re.findall(r'art/\d{4}/\d{1,2}/\d{1,2}/\w*',tagstr)

url_list=[] #通知公告的具体地址

for rg in rgs:
    url_list.append('http://www.nbwjw.gov.cn/' + rg + '.html') 






def read_url_info(url):

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    headers = { 'User-Agent' : user_agent }
    r = requests.get(url,headers=headers)  #连接
    content = r.text #获取内容，自动转码unicode
    
    soup = BeautifulSoup(content,"lxml")

    url_detail=soup.title
   
    return url_detail


csv_write = csv.writer(open('Stu_csv.csv','a', newline=''),dialect='excel')
#写入具体内容
p = read_url_info(url_list[5]).encode('utf-8')
csv_write.writerow(p)
print ("write over")

