from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import datetime  # For datetime objects
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])

# Import the backtrader platform
import backtrader as bt

import numpy as np
class TestStrategy(bt.Strategy):

    params = (('exitbars', 30),('maperiod', 14))
    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f, time %s' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm,
                     order.executed.dt))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f, time %s' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm,
                          order.executed.dt))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None


    def notify_trade(self, trade):

        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close

        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None
        self.flag=False
        self.priceStore=None

        self.mfi= bt.talib.MFI(self.data.high,self.data.low,self.data.close,self.data.volume, timeperiod=self.params.maperiod)
        #self.mfi = bt.talib.MFI(self.data)
    def pl(self,compare=False):
        if compare:
            price=compare
        else:
            price=self.position.price
        return 100*(self.dataclose[0]/price-1)

    def since_last(self):
        return len(self)-self.bar_executed

    def take_profit(self):
        day=self.since_last()
        profit=self.pl()
        if profit>2:
            if profit>day/3:
                return True
        return False

    def next(self):
        # Simply log the closing price of the series from the reference
        #self.log('Close, %.2f' % self.dataclose[0])
        #self.log(self.sma[0])
        if not self.position:

            if self.mfi[0] <26:
                # current close less than previous close
                    # BUY, BUY, BUY!!! (with all possible default parameters)
                    '''
                    self.log('BUY CREATE, %.2f' % self.dataclose[0])
                    self.order = self.buy()
                    '''
                    self.flag=True
                    self.priceStore=self.dataclose[0]

            if self.flag:
                ind=[self.mfi[0] < 30,self.pl(compare=self.priceStore)<-5]
                if np.product(ind) :
                    # current close less than previous close
                        # BUY, BUY, BUY!!! (with all possible default parameters)
                        self.log('BUY CREATE, %.2f' % self.dataclose[0])
                        self.order = self.buy()

            # Already in the market ... we might sell
        else:
            #if self.mfi[0]>70 or len(self) >= (self.bar_executed + self.params.exitbars) or self.earn(5):
            ind1=[self.mfi[0]>70,self.since_last() >=self.params.exitbars,self.take_profit()]

            if np.sum(ind1):
                print(ind1)
                # SELL, SELL, SELL!!! (with all possible default parameters)
                self.log('SELL CREATE, %.2f' % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell(size=self.position.size)



if __name__ == '__main__':
    # Create a cerebro entity
    cerebro = bt.Cerebro()

    cerebro.addstrategy(TestStrategy)

    # Datas are in a subfolder of the samples. Need to find where the script is
    # because it could have been called from anywhere
    #modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
    #datapath = os.path.join(modpath, 'MSFT.csv')

    import yfinance as yf

    stock="9513.T"
    stock="5901.T"
    stock="9020.T"
    stock="VIV"
    stock="CVS"
    msft = yf.Ticker(stock)
    hist = msft.history(period="max")
    #print(hist)
    # Create a Data Feed
    data = bt.feeds.PandasData(
        dataname=hist,
        # Do not pass values before this date
        fromdate=datetime.datetime(2007, 12, 11),
        # Do not pass values after this date
        todate=datetime.datetime(2023, 2, 10))

    # Add the Data Feed to Cerebro

    cerebro.adddata(data)

    # Set our desired cash start
    cerebro.broker.setcash(100000.0)
    cerebro.broker.setcommission(commission=0.001)


    # Print out the starting conditions
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # Run over everything
    cerebro.run()

    # Print out the final result
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.plot()