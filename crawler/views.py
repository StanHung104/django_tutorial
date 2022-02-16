from http import cookies
from ipaddress import IPV4LENGTH
from re import A
from tempfile import TemporaryFile
from bs4 import BeautifulSoup
from django.shortcuts import render
import datetime
import csv
import re
import time
import requests


# Create your views here.
from django.shortcuts import render, HttpResponse
from bs4 import BeautifulSoup

import numpy as np
def hello_view(request):
    return render(request, 'hello_django.html', {
        'data': "Hello Django",
    })

def homepage(request):
    now = datetime.datetime.now()
    context = {'now':now}
    return render(request, 'homepage.html', context)

def simple_crawl(request):
    return render(request, 'simple_craw.html')

def get_web_page(url):
        resp = requests.get(
            url=url,
            cookies= {'over18': '1'}
        )
        if resp.status_code != 200:
            print('Invalid_url:', resp.url)
            return None
        else:
            return resp.text
    
def get_articles(dom, date):
        soup = BeautifulSoup(dom, 'html.parser')

        #取得上一頁連結
        paging_div = soup.find('div', 'btn-group btn-group-paging')
        prev_url = paging_div.find_all('a')[1]['href']
        articles = []
        authortotal = []
        divs = soup.find_all('div', 'r-ent')
        for d in divs:
            if d.find('div', 'date').text.strip() == date: #發文日期正確
                #取得推文數
                push_count = 0
                push_str = d.find('div', 'nrec').text
                if push_str:
                    try:
                        push_count = int(push_str) #轉換字串為數字
                    except ValueError:
                        #若轉換失敗，可能是'爆' or 'X1','X2'.....
                        #若不是,不做任何事，push_count保持為0
                        if push_str == '爆':
                            push_count = 99
                        elif push_str.startswith('X'):
                            push_count = -10.
                #取得文章連結及標題
                if d.find('a'): #有超連結，表示文章存在，未被刪除
                    href = d.find('a')['href']
                    title = d.find('a').text
                    author = d.find('div', 'author').text if d.find('div', 'author') else ''
                    articles.append({
                        'title': title,
                        'href': href,
                        'push_count':push_count,
                        'author':author
                    })
                    authortotal.append(author)
        return articles, prev_url, authortotal

def get_ip(dom):
    pattern= '來自: \d+\.\d+\.\d+'
    match = re.search(pattern, dom)
    if match:
        return match.group(0).replace('來自:', '')
    else:
        return None

def get_conutry(ip):
        if ip:
            url = 'http://api.ipstack.com/{}?access_key={}'.format(ip, API_KEY)
            data = requests.get(url).json()
            country_name = data['country_name'] if data['country_name'] else None
            return country_name
        return None


def POST_crawl(request):
    APIkey = request.POST.get('APIkey', None)
    PTT_URL = 'https://www.ptt.cc'
    API_KEY = 'b310ae343691cb1ece2d90f2aa2ad057'
    def get_conutry(ip):
        if ip:
            url = 'http://api.ipstack.com/{}?access_key={}'.format(ip, API_KEY)
            data = request.get(url).json()
            country_name = data['country_name'] if data['country_name'] else None
            return country_name
        return None
    
    data = request.POST.get('title, None')
    print(data)
    number = data
    print('取得今日文章列表')
    current_page = get_web_page(PTT_URL + '/bbs/Gossiping/index/html')
    if current_page:
        articles =[]
        author=[]
        country=[]
        title =[]
        iptotal=[]
        today = time.strftime('%m%d').lstrip('0')
        current_articles, prev_url,authortotal = get_articles(current_page, today) #今天文章

        for i in range(int(number)):
            articles += current_articles
            current_page = get_web_page(PTT_URL + prev_url)
            current_articles, prev_url,authortotal = get_articles(current_page, today)
        print('共 %d 篇文章' % (len(articles)))

        #已取得文章列表，進入個文章尋找發文者IP
        print('取得前100篇文章IP')
        country_to_count = dict()
        for article in articles[:len(articles)]:
            #print('查詢IP：, article['title])
            page = get_web_page(PTT_URL + article['href'])
            if page:
                ip = get_ip(page)
                country = get_conutry(ip)
                if country in country_to_count.keys():
                    country_to_count[country] += 1
                else:
                    country_to_count[country] = 1
            #print("來自",country, end='')
            #print("  ","作者是",article['author'])
            author.append(article['author'])
            title.append(article['title'])
            countryT.append(country)
            iptotal.append(ip)

            #印出各國IP次數資訊
            print('各國IP分布')
            for k, v in country_to_count.items():
                print(k, v)
                countryT=np.array(countryT)
                countryT.reshape(countryT.shape[0], 1)
                articlenumber = len(articles)

        with open('產生的文件檔案.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            writer.writerow(['文章標題', '作者', 'IP', '國家'])
            for i in range(len(author)):
                writer.writerow([title[i],author[i],iptotal[i],countryT[i]])
            
        return render(request, 'simple_crawl_result.html',locals())
    
#     def get_web_page(url):
#         resp = request.get(
#             url=url,
#             cookies= {'over18': '1'}
#         )
#         if resp.status_code != 200:
#             print('Invalid_url:', resp.url)
#             return None
#         else:
#             return resp.text
    
#     def get_articles(dom, date):
#         soup = BeautifulSoup(dom, 'html.parser')

#         #取得上一頁連結
#         paging_div = soup.find('div', 'btn-group btn-group-paging')
#         prev_url = paging_div.find_all('a')[1]['href']
#         articles = []
#         authortotal = []
#         divs = soup.find_all('div', 'r-ent')
#         for d in divs:
#             if d.find('div', 'date').text.strip() == date: #發文日期正確
#                 #取得推文數
#                 push_count = 0
#                 push_str = d.find('div', 'nrec').text
#                 if push_str:
#                     try:
#                         push_count = int(push_str) #轉換字串為數字
#                     except ValueError:
#                         #若轉換失敗，可能是'爆' or 'X1','X2'.....
#                         #若不是,不做任何事，push_count保持為0
#                         if push_str == '爆':
#                             push_count = 99
#                         elif push_str.startswith('X'):
#                             push_count = -10.
#                 #取得文章連結及標題
#                 if d.find('a'): #有超連結，表示文章存在，未被刪除
#                     href = d.find('a')['href']
#                     title = d.find('a').text
#                     author = d.find('div', 'author').text if d.find('div', 'author') else ''
#                     articles.append({
#                         'title': title,
#                         'href': href,
#                         'push_count':push_count,
#                         'author':author
#                     })
#                     authortotal.append(author)
#         return articles, prev_url, authortotal

# def get_ip(dom):
#     pattern= '來自: \d+\.\d+\.\d+'
#     match = re.search(pattern, dom)
#     if match:
#         return match.group(0).replace('來自：', '')
#     else:
#         return None

# def get_conutry(ip):
#         if ip:
#             url = 'http://api.ipstack.com/{}?access_key={}'.format(ip, API_KEY)
#             data = request.get(url).json()
#             country_name = data['country_name'] if data['country_name'] else None
#             return country_name
#         return None

            







