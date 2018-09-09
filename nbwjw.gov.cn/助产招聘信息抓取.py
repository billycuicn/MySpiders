#coding=utf-8
#从几大卫计委的网站上抓取助产专业招聘信息并写入Excel文件
#copyright@BillyCui

import re
import csv
import docx

import requests
from bs4 import BeautifulSoup

url='http://www.nbwjw.gov.cn/col/col144/index.html'
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
headers = { 'User-Agent' : user_agent }
r = requests.get(url,headers=headers)  #连接
content = r.text 
soup = BeautifulSoup(content,"lxml")
tags = soup.find_all('script',language = 'javascript')
tagstr = tags[3]
tagstr = ''.join(tagstr)
rgs = re.findall(r'art/\d{4}/\d{1,2}/\d{1,2}/\w*',tagstr)
url_list=[] #通知公告的具体地址

for rg in rgs:
    url_list.append('http://www.nbwjw.gov.cn/' + rg + '.html') 

for url in url_list:
    #写入具体内容
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    headers = { 'User-Agent' : user_agent }
    r = requests.get(url,headers=headers)  #连接
    r.encoding='utf-8'
    content = r.text #获取内容，自动转码unicode
    soup = BeautifulSoup(content,"lxml")

    url_alltext=soup.get_text()
    url_date = soup.find(attrs={'name':'Maketime'})
    url_title = soup.title
    url_attach = re.findall(r'classid=0&filename=\w*.docx',str(soup.head))
    url_detail=[url,url_date,url_title,url_attach]
    csv_write = csv.writer(open('zczp_csv.csv','a', newline=''),dialect='excel')
    if ('招聘' in str(url_title)) and ('公告' in str(url_title) and ('助产' in url_alltext)):
        csv_write.writerow(url_detail)
    elif url_attach != '':
        if (str(url_attach)[-4:] == 'docx'  or str(url_attach)[-3:] == 'doc'):
            if '助产' in getdocText(url_attach):
                csv_write.writerow(url_detail)

print ('OK')

def getdocText(filename):
    doc = docx.Document(filename)
    fullText = []
    for i in doc.paragraphs:    #迭代docx文档里面的每一个段落
        fullText.append(i.text) #保存每一个段落的文本
    return '\n'.join(fullText)
