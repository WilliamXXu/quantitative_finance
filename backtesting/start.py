from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import datetime  # For datetime objects
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])

# Import the backtrader platform
import backtrader as bt
import numpy as np
package=str(sys.argv[2])
name='TestStrategy'


#if __name__ == '__main__':
    # Create a cerebro entity
cerebro = bt.Cerebro()
cerebro.addstrategy(getattr(__import__(package, fromlist=[name]), name))

# Datas are in a subfolder of the samples. Need to find where the script is
# because it could have been called from anywhere
#modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
#datapath = os.path.join(modpath, 'MSFT.csv')
import yfinance as yf
stock=str(sys.argv[1])
print(stock)
msft = yf.Ticker(stock)
hist = msft.history(period="max")
#print(hist)
# Create a Data Feed
data = bt.feeds.PandasData(
    dataname=hist,
    # Do not pass values before this date
    fromdate=datetime.datetime(2007, 12, 11),
    # Do not pass values after this date
    todate=datetime.datetime.today())

# Add the Data Feed to Cerebro

cerebro.adddata(data)

# Set our desired cash start
cerebro.broker.setcash(100000.0)
cerebro.broker.setcommission(commission=0.001)


# Print out the starting conditions
print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

# Run over everything
result=cerebro.run()

print(result[0].correct)
print(result[0].incorrect)
print(np.mean(result[0].pnl))

# Print out the final result
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.plot()

