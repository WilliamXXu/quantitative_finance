from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import datetime  # For datetime objects
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])

# Import the backtrader platform
import backtrader as bt
import numpy as np

import yfinance as yf
present=datetime.datetime.today()

package=str(sys.argv[2])
name='TestStrategy'
#if __name__ == '__main__':
    # Create a cerebro entity


# Datas are in a subfolder of the samples. Need to find where the script is
# because it could have been called from anywhere
#modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
#datapath = os.path.join(modpath, 'MSFT.csv')

#filel = open('mfi.txt','a+')
filel=open(str(sys.argv[1]),'a+')
filel.seek(0)

stock=filel.read().splitlines()

filel.close()
correct=0
incorrect=0
res=[]
for x in range(len(stock)):
    #if len(stock[x])==4:
        stock[x]=stock[x]+'.SS'

        print(stock[x])
        try:
            hist = yf.Ticker(stock[x]).history(period="max")
            #print(hist)
            # Create a Data Feed
            cerebro = bt.Cerebro()
            cerebro.addstrategy(getattr(__import__(package, fromlist=[name]), name))
            data = bt.feeds.PandasData(
                dataname=hist,
                # Do not pass values before this date
                fromdate=datetime.datetime(2007, 6,1),
                # Do not pass values after this date
                todate=datetime.datetime(2023, 2, 10))

            # Add the Data Feed to Cerebro
            cerebro.adddata(data)

            # Set our desired cash start
            cerebro.broker.setcash(100000.0)
            cerebro.broker.setcommission(commission=0.001)


            # Run over everything
            result=cerebro.run()
            print(result[0].correct)
            print(result[0].incorrect)
            print(np.mean(result[0].pnl))
            correct+=result[0].correct
            incorrect+=result[0].incorrect
            res=res+result[0].pnl
            dt=result[0].lastBuy
            print(dt)
            if dt>present:
                with open('res.txt','a+') as f:
                    f.write(stock[x])
        except:
            pass
print(correct)
print(incorrect)
tot=correct+incorrect
print(correct/(tot))

import seaborn as sns

sns.displot(res)
import matplotlib.pyplot as plt
plt.show()
import numpy as np
print(np.mean(res))
