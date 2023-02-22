import talib
from talib import stream
import yfinance as yf
from datetime import datetime
import sys

name=str(sys.argv[1])

if name=='topix':
	address='topix-1000_symbols.txt'
	code='.T'
	forex=20
if name=='mexico':
	address='mexico_broad_symbols.txt'
	code='.MX'
	forex=3


filel = open(address,'a+')
filel.seek(0)
stock=filel.read().splitlines()
filel.close()
correct=0
incorrect=0
res=[]
for x in range(len(stock)):
	#if len(stock[x])==4:
		#stock[x]=stock[x]+'.T'
		stock[x]=stock[x]+code
		print(stock[x])

		entity=yf.Ticker(stock[x])
		try:
			marketcap=int(entity.fast_info['marketCap'])
		except:
			print('no marketcap')
			marketcap=0
		if marketcap/10000/10000/forex>10:
			
			hist = entity.history(period="1mo")
			#print(hist.columns.values)
	#output = talib.SMA(close)
			mfi=stream.MFI(hist['High'], hist['Low'], hist['Close'], hist['Volume'], timeperiod=14)
			

			'''
			macd_fast, macd_slow, macd_diff=stream.MACD(hist['Close'], fastperiod=12, slowperiod=26, signalperiod=9)
			ratio=abs(macd_diff/macd_fast)
			print(ratio)
			and ratio<0.05 and macd_fast<0 
			'''

			
			if mfi<26:
				with open('picks/mfi_'+name+'_'+datetime.today().strftime('%Y-%m-%d')+'.txt','a+') as f:
					f.write(stock[x]+'\n')
			print(mfi)
			#print(macd)
