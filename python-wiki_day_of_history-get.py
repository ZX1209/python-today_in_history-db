import requests
from bs4 import BeautifulSoup
from string import Template
import logging

import time
import random

import json

logging.basicConfig(level=logging.INFO)

#                1  2  3  4  5  6  7  8  9  10 11 12
day_of_months = [31,29,31,30,31,30,31,31,30,31,30,31]

todayTemplate = Template('${yue}月${re}日')
todayTemplate.substitute(yue=1,re=2)


proxies={'http':'127.0.0.1:1080','https':'127.0.0.1:1080'}

# requests.get('http://www.google.com',proxies=proxies)

todays = {}
todays_simple = {}
# todays
#     date
#     bigThings
#         []
#     birthDays
#         []
#     passDays
#         []
#     hoildays
#         []

try:
    yue = 1
    while yue<=12:
        re = 1
        while re<=day_of_months[yue-1]:
            baseUrl = 'https://zh.wikipedia.org/wiki/'
            date = todayTemplate.substitute(yue=yue,re=re)
            targetUrl = baseUrl+date
            logging.info(targetUrl)

            # sleep
            sleepTime = int(random.uniform(1,5)+0.5)
            time.sleep(sleepTime)

            # get
            response = requests.get(targetUrl, proxies=proxies)

            # parser
            if response.status_code == 200:
                soup = BeautifulSoup(response.text,features="html.parser")
                quotes = soup.select('div.mw-parser-output')[0]

                cata = "未知"
                tag = "未知"
                todays[date] = {}
                todays[date][cata] = {}
                todays[date][cata][tag] = None
                
                todays_simple[date] = []

                for child in quotes.children:
                    if not child.name:
                        continue

                    elif child.name == 'h2':
                        cata = str(child('span')[1].get_text())
                        todays[date][cata] = {}

                    elif child.name == 'h3':
                        tag = str(child('span')[1].get_text())
                        todays[date][cata][tag] = {}

                    elif child.name == 'ul':
                        tmplist = list(map(str,child.children))
                        todays[date][cata][tag] = tmplist

                        todays_simple[date].extend(tmplist)
                        logging.info((date,cata,tag))
                    
                logging.info((date,'finished'))
            re+=1

        yue+=1
except:
    f = open('todays.json','w')
    json.dump(todays,f) 

    f_simple = open('todays-simple.json','w')
    json.dump(todays_simple,f_simple) 
