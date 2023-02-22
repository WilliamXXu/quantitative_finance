import json
import pandas as pd
import requests
from numpy.random import exponential




def fetch(url):

    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    req = urllib.request.Request(url=url, headers=headers)
    with urllib.request.urlopen(req) as url:
        s=url.read()
    soup = BeautifulSoup(s)
    return soup


def getSymbol(url):
    import re
    #base='https://www.investing.com'
    #url=base+title
    flag=True
    

    while flag:
        try:
            soup=fetch(url)
            fullName=soup.find('h1',class_="text-2xl font-semibold instrument-header_title__gCaMF mobile:mb-2")
            text=fullName.get_text()

        except urllib.error.HTTPError:
            print('forced_pause1')
            time2=time.time()
            time.sleep(exponential(20))
        except AttributeError:
            print('forced_pause2')
            time2=time.time()
            time.sleep(exponential(20))
        else:
            flag=False

    text=re.search('(?<=\().+?(?=\))',text)
    return text[0]

def writeOut(li,name):
    file = open(name+'.txt','w')
    for item in li:
        file.write(item+"\n")
    file.close()





if __name__ == '__main__':
    import urllib.request
    from bs4 import BeautifulSoup
    import time
    pause_avg=10
   # page_number=2
    
    #ind='nzx-50'
 #   base='https://www.investing.com'
 #   u=base+'/indices/'+ind+'-components/'
#   headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}

    ind='HK_A+H'
    address='Hong Kong Financial Markets - Investing.com.html'

    ind='topix-1000'
    address='Topix 1000 Index Stocks Prices - Investing.com.html'
    address='Topix 1000 Index Stocks Prices - Investing.com - Page 2.html'


    ind='mexico_broad'
    address='Mexico Stock Market - Investing.com.html'

    ind='singapore_broad'
    address='Singapore Stock Market - Investing.com.html'
    ind='shanghai_comp'
    address='China Stock Market - Investing.com.html'



    filel = open('data/'+ind+'_links.txt','a+')
    filet = open('data/'+ind+'_titles.txt','a+')
    files = open('data/'+ind+'_symbols.txt','a+')

    filel.seek(0)
    filet.seek(0)
    files.seek(0)

    links=filel.read().splitlines()
    titles=filet.read().splitlines()
    symbols=files.read().splitlines()

    filet.close()
    files.close()
    filel.close()

    with open(address,'r') as f:
        html=f.read()
    soup = BeautifulSoup(html, 'html.parser')
    
    clas='noWrap bold elp left plusIconTd'
    clas="bold left noWrap elp plusIconTd"
    for td in soup.find_all('td',class_=clas):
        a=td.a
        link=a.get('href')
        title=a.get('title')
        print(link)
        print(title)
        if not(title in titles):
            symbol=getSymbol(link)


            filel = open('data/'+ind+'_links.txt','a+')
            filet = open('data/'+ind+'_titles.txt','a+')
            files = open('data/'+ind+'_symbols.txt','a+')

            files.write(symbol+"\n")
            filet.write(title+"\n")
            filel.write(link+"\n")

            filet.close()
            files.close()
            filel.close()

            print(symbol)
            time2=time.time()
            time.sleep(exponential(pause_avg))






