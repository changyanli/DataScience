"""
@author: cyli
"""
from bs4 import BeautifulSoup
from operator import itemgetter
import requests
import time
ban_list = ['/bbs/Beauty/M.1490936972.A.60D.html', 
            '/bbs/Beauty/M.1494776135.A.50A.html', 
            '/bbs/Beauty/M.1503194519.A.F4C.html', 
            '/bbs/Beauty/M.1504936945.A.313.html', 
            '/bbs/Beauty/M.1505973115.A.732.html', 
            '/bbs/Beauty/M.1507620395.A.27E.html', 
            '/bbs/Beauty/M.1510829546.A.D83.html', 
            '/bbs/Beauty/M.1512141143.A.D31.html']
def crawl():
    allarticle = open("all_articles.txt", "w", encoding = 'utf8')
    allpopular = open("all_popular.txt", "w", encoding = 'utf8')
    for index in range(2000,2353):
        url = "https://www.ptt.cc/bbs/Beauty/index"+str(index)+".html"
        r = requests.get(url)
        content = r.text
        soup = BeautifulSoup(content, 'html.parser')
        articles = soup.find_all('div','r-ent')
        for data in articles:
            if data.find('a') and str(data.find('a').text)[1] != "公":
                if index == 2000 and data.find('div','date').string == "12/31":
                    continue
                if index == 2352 and data.find('div','date').string == " 1/01":
                    break
                href = str(data.find('a')['href'])
                if href in ban_list:
                    continue
                title = data.find('a').text
                date = data.find('div','date').string
                if date[0] == " ":
                    date = ""+date[1]+""+date[3]+""+date[4]
                else:
                    date = ""+date[0]+""+date[1]+""+date[3]+""+date[4]
                allarticle.write(str(date)+","+str(title)+",https://www.ptt.cc"+href+"\n")
                if data.find('div','nrec').string == "爆":
                    allpopular.write(str(date)+","+str(title)+",https://www.ptt.cc"+href+"\n")
        time.sleep(0.2)
    allarticle.close();
    allpopular.close();
def push(start_date = 101, end_date = 1231):
    allarticle = open("all_articles.txt", encoding = 'utf8')
    push_list = {}
    boo_list = {}
    for line in allarticle:
        date = line[:line.find(",")]
        url = line[line.rfind(",") + 1:]
        url = url.split()[0]
        if(int(date) < start_date):
            continue
        if(int(date) > end_date):
            break
        r = requests.get(str(url))
        content = r.text
        soup = BeautifulSoup(content, 'html.parser')
        pushes = soup.find_all('div','push')
        for data in pushes:
            if data.find('span','f3 hl push-userid'):
                user_id = data.find('span','push-userid').string
                push_tag = data.find('span','push-tag').string
                if push_tag == "推 ":
                    if user_id in push_list:
                        push_list[user_id] -= 1
                    else:
                        push_list[user_id] = -1
                elif push_tag  == "噓 ":
                    if user_id in boo_list:
                        boo_list[user_id] -= 1
                    else:
                        boo_list[user_id] = -1
        time.sleep(0.2)
    pushfile = open("push[" + str(start_date) + "-" + str(end_date) + "].txt", "w", encoding = 'utf8')
    pushfile.write("all like: " + str(-sum(push_list.values())) + "\n")
    pushfile.write("all boo: " + str(-sum(boo_list.values())) + "\n")
    push_list = sorted(push_list.items(), key = itemgetter(1,0))
    boo_list = sorted(boo_list.items(), key = itemgetter(1,0))
    for rank in range(10):
        pushfile.write("like #" + str(rank + 1) + 
                       ": " + str(push_list[rank][0]) + 
                       " " + str(-push_list[rank][1]) + "\n")
    for rank in range(10):
        pushfile.write("boo #" + str(rank + 1) + 
                       ": " + str(boo_list[rank][0]) + 
                       " " + str(-boo_list[rank][1]) + "\n")

def popular(start_date = 101, end_date = 1231):
    allpopular = open("all_popular.txt", encoding = 'utf8')
    sumPopular = 0
    imgList = []
    for line in allpopular:
        date = line[:line.find(",")]
        url = line[line.rfind(",") + 1:]
        url = url.split()[0]
        if(int(date) < start_date):
            continue
        if(int(date) > end_date):
            break
        sumPopular += 1
        r = requests.get(str(url))
        content = r.text
        soup = BeautifulSoup(content, 'html.parser')
        main_content = soup.find('div',{'id':'main-content'})
        hrefs = main_content.find_all('a')
        for href in hrefs:
            url = str(href.text)
            if url.endswith('.jpg') or url.endswith('.jpeg') or url.endswith('.png') or url.endswith('.gif'):
                imgList.append(url)
        time.sleep(0.2)
    popularfile = open("popular [" + str(start_date) + "-" + str(end_date) + "].txt", "w", encoding = 'utf8')
    popularfile.write("number of popular articles: " + str(sumPopular) + "\n")
    for url in imgList:
        popularfile.write(url+"\n")
def keyword(keyword, start_date = 101, end_date = 1231):
    allarticle = open("all_articles.txt", encoding = 'utf8')
    keywordFile = open("keyword(" + keyword + ")[" + str(start_date) + "-" + str(end_date) + "].txt", "w", encoding = 'utf8')
    for line in allarticle:
        date = line[:line.find(",")]
        url = line[line.rfind(",") + 1:]
        url = url.split()[0]
        if(int(date) < start_date):
            continue
        if(int(date) > end_date):
            break
        r = requests.get(str(url))
        soup = BeautifulSoup(r.text, 'html.parser')
        main_content = soup.find('div',{'id':'main-content'})
        content = str(main_content.text)
        content = content[:content.find('--\n※ 發信站: 批踢踢實業坊')]
        if content.find(keyword) == -1:
            continue
        hrefs = main_content.find_all('a')
        for href in hrefs:
            url = str(href.text)
            if url.endswith('.jpg') or url.endswith('.jpeg') or url.endswith('.png') or url.endswith('.gif'):
                keywordFile.write(url + "\n")
        time.sleep(0.2)
def test():
    crawl()
    push()
    popular(101,201)
    keyword('正妹',101,201)