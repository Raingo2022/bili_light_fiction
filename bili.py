import requests
import os
import re
from bs4 import BeautifulSoup

if __name__ == '__main__' :
    ##通过关键词请求到查询界面
    searchkey = input('please enter the novel you want to inquire : ')
    url_inquire = 'https://www.linovelib.com/S6/'
    url = 'https://www.linovelib.com'
    headers = {
        'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.55'
    }
    data = {
        'searchkey' : searchkey ,
        'searchtype' : 'all'
    }
    page_inquire = requests.post(url=url_inquire,data=data,headers=headers).text
    #创建一个soup对象
    soup = BeautifulSoup(page_inquire,'lxml')
    #信息提取
    search_tips = soup.find('div',class_='search-tips').text #搜寻结果
    last_page = soup.find('a',class_='last').text#最大页数

    #获取所有页面的信息
    ex1 = '<h2 class="tit"><a href="(.*?)"'
    novel_href = []
    novel_name = []
    for page in range(1,int(last_page)+1) :
        url_more = url_inquire + searchkey + '_' + str(page) + '.html'
        pageTemp = requests.get(url=url_more,headers=headers).text
        souptemp = BeautifulSoup(pageTemp,'lxml')
        ##提取标题
        name = souptemp.find_all('h2',class_='tit')
        for i in name :
            novel_name.append(i.text)
        #提取并且封装链接
        href = re.findall(ex1,pageTemp,re.S)
        for i in href :
            i = i.split('.')[0]
            novel_href.append(url+i+'/catalog')

    #将名字与链接存入字典
    novel =  dict(zip(novel_name,novel_href))

    #打印出搜索列表供用户参考
    print(search_tips + ' :')
    for i in novel.keys() :
        print(i)
    print('-----------------------------------------------------')

    #用户输入小说名，进行下载
    want = input('which one do you want to download : ')
    filename =want

    #----------------------小说下载-----------------------
    url_catalog = novel[want]
    #请求目录
    catalog = requests.get(url=url_catalog,headers=headers).text
    #创建soup对象
    soup_catalog = BeautifulSoup(catalog,'lxml')
    li_list = soup_catalog.find_all('li',class_='col-4')

    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Mobile Safari/537.36 Edg/109.0.1518.55'
    }
    with open('./'+want+'.txt','w',encoding='utf-8') as fp :
        for li in li_list :
            title = li.a.string
            if li.a['href'] == 'javascript:cid(0)' :
                print(title,'下载失败！')
                continue
            detail_url ='https://www.linovelib.com' + li.a['href']
            detail_page_text = requests.get(url=detail_url,headers=headers).text
            detali_soup = BeautifulSoup(detail_page_text,'lxml')
            content = detali_soup.find('div',class_='acontent').text
            fp.write(title + ':' + content +'\n')
            print(title+'.txt 下载完成!')
    print("Over!!")










