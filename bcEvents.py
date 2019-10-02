#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 18:27:00 2019

@author: Gary Ge
"""

import requests
from bs4 import BeautifulSoup

def get_html(url):
    try:
        r = requests.get(url,timeout=30)
        r.raise_for_status()
        r.encoding='utf-8'
        return r.text
    except:
        return " ERROR "
#test = get_html(url1)
def get_content(url):
    '''
    分析网页
    '''
    # 初始化一个列表来保存所有的信息：
    cases = []
    # 首先，我们把需要爬取信息的网页下载到本地
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    #返回一个列表类型
    event_list = soup.find_all('div', attrs={'class': 'item event_item vevent'})
#    event = event_list[7]
#    descrips=[]
#    for descrip in event.find_all('h4',attrs={'class':'description'}):
#        descrips.append(descrip.string)
#    print(descrips)
#    summary_title=event.find('h3',attrs={'class':'summary'})
#    summarys=[]
#    for summary in summary_title.find_all('a'):
#        summarys.append(summary.string)
#    print(summarys)
#    case['link'] = links[0]
    
    # 通过循环找到每个帖子里的我们需要的信息：
    for event in event_list:
        # 初始化一个字典来存储文章信息
        case = {}
        # 这里使用一个try except 防止爬虫找不到信息从而停止运行
        try:
            # 开始筛选信息，并保存到字典中
            links=[]
            for link in event.find_all('a',attrs={'class':'box_left'}):
                links.append(link.get('href'))
            case['links']=links[0]
            cases.append(case)
            summary_title=event.find('h3',attrs={'class':'summary'})
            summarys=[]
            for summary in summary_title.find_all('a'):
                summarys.append(summary.string)
            case['summarys']=summarys[0]
            descrips=[]
            for descrip in event.find_all('h4',attrs={'class':'description'}):
                descrips.append(descrip.string)
            case['descrips']=descrips[0]
#            print(comment)
##            comment['link'] = "http://tieba.baidu.com/" + \
##                event.find('a', attrs={'class': 'j_th_tit '})['href']
##            comment['name'] = event.find(
##                'span', attrs={'class': 'tb_icon_author '}).text.strip()
##            comment['time'] = event.find(
##                'span', attrs={'class': 'pull-right is_show_create_time'}).text.strip()
##            comment['replyNum'] = event.find(
##                'span', attrs={'class': 'threadlist_rep_num center_text'}).text.strip()
##            comments.append(comment)
        except:
            print('出了点小问题')
    return cases

def Out2File(dict):
    '''
    将爬取到的文件写入到本地
    保存到当前目录的 learn.txt文件中。

    '''
    with open('bcEvents.txt', 'a+') as f:
        count=1
        for event in dict:
            f.write('事件{}:\n概述： {}\n内容： {}  \n详细链接： {}\n\n'.format(str(count),event['summarys'],event['descrips'],event['links']))
            count+=1
        print('当前页面爬取完成')
#输出结果
        
def main(base_url, deep):
    url_list = []
    # 将所有需要爬去的url存入列表
    for i in range(0, deep):
        url_list.append(base_url)
    print('所有的网页已经下载到本地！ 开始筛选信息。。。。')

    #循环写入所有的数据
    for url in url_list:
        content = get_content(url)
        Out2File(content)
    print('所有的信息都已经保存完毕！')
base_url = 'https://events.bc.edu/calendar'
# 设置需要爬取的页码数量
deep = 1

if __name__ == '__main__':
    main(base_url, deep)