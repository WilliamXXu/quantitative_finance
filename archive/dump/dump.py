import json
import pandas as pd
import requests
from numpy.random import exponential

def get_exchange_data(key, exchange='MX'):
    """
    returns metadata for a specific exchange
    available: US, NASDAQ, OTCBB, PINK, BATS
    """
    endpoint = f"https://eodhistoricaldata.com/api/exchange-symbol-list/"
    endpoint += f"{exchange}?api_token={key}&fmt=json"
    print("Downloading data")
    call =requests.get(endpoint).text
    exchange_data = pd.DataFrame(json.loads(call))
    print("Completed")
    return exchange_data

def main():
    #key = open('api_token.txt').read()
    key='63d494f299aee1.28248669';
    print(get_exchange_data(key))

def getTicker(company_name):
    yfinance = "https://query2.finance.yahoo.com/v1/finance/search"
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    params = {"q": company_name, "quotes_count": 1, "country": "Japan"}

    res = requests.get(url=yfinance, params=params, headers={'User-Agent': user_agent})
    data = res.json()

    company_code = data['quotes'][0]['symbol']
    return company_code


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
    print(url)
    soup=fetch(url)
    fullName=soup.find('h1',class_="text-2xl font-semibold instrument-header_title__gCaMF mobile:mb-2")
    print(fullName)
    text=fullName.get_text()
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
   # page_number=2
    
    #ind='nzx-50'
 #   base='https://www.investing.com'
 #   u=base+'/indices/'+ind+'-components/'
#   headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}

    ind='topix-1000'
    filel = open('data/'+ind+'_links.txt','a+')
    filet = open('data/'+ind+'_titles.txt','a+')
    files = open('data/'+ind+'_symbols.txt','a+')

    filel.seek(0)
    filet.seek(0)
    files.seek(0)

    links=filel.read().splitlines()
    titles=filet.read().splitlines()
    symbols=files.read().splitlines()
    print(filet.read())
    print(titles)
    filet.close()
    files.close()
    filel.close()

    with open('Topix 1000 Index Stocks Prices - Investing.com.html','r') as f:
        html=f.read()
    soup = BeautifulSoup(html, 'html.parser')

    for td in soup.find_all('td',class_="bold left noWrap elp plusIconTd"):
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
            time.sleep(exponential(8))






