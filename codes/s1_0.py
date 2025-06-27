import backtrader as bt
import numpy as np
import time
class TestStrategy(bt.Strategy):
    params = (('exitbars', 30),('maperiod', 14))
    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                '''
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f, time %s' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm,
                     order.executed.dt))
                '''
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
                self.lastBuy=bt.num2date(order.executed.dt)
            else:  # Sell
                '''
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f, time %s' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm,
                          order.executed.dt))
                '''

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None


    def notify_trade(self, trade):

        if not trade.isclosed:
            self.invest=self.position.price*self.position.size
            return

        #self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f value %.2f' %(trade.pnl, trade.pnlcomm,trade.price))
        res=trade.pnlcomm/self.invest
        if res>0.01:
            self.correct+=1
        if res<-0.01:
            self.incorrect+=1
        if res<-0.5:
            print('huge loss!')
            #time.sleep(5)
        self.pnl.append(res)
        self.invest=0

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
        self.priceStart=None
        self.barStart=False
        self.correct=0
        self.incorrect=0
        self.pnl=[]
        self.lastBuy=None
        self.invest=0


        self.mfi= bt.talib.MFI(self.data.high,self.data.low,self.data.close,self.data.volume, timeperiod=self.params.maperiod)
        #self.mfi = bt.talib.MFI(self.data)
    def pl(self,price=None):
        price=price or self.position.price
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
                    
                    '''
                    self.log('BUY CREATE, %.2f' % self.dataclose[0])
                    self.order = self.buy()
                    self.flag=True
                    self.priceStart=self.dataclose[0]
                    self.barStart=len(self)



            # Already in the market ... we might sell
        else:
            if self.flag and self.barStart:

                ind=[self.mfi[0] < 30,self.pl(price=self.priceStart)<-3,len(self)-self.barStart<14]
                if np.product(ind) :
                    self.log('BUY CREATE, %.2f' % self.dataclose[0])
                    self.flag=False
                    self.priceStart=None
                    self.barStart=False                    
                    # current close less than previous close
                        # BUY, BUY, BUY!!! (with all possible default parameters)
                        #self.log('BUY CREATE, %.2f' % self.dataclose[0])
                    self.order = self.buy()

            #if self.mfi[0]>70 or len(self) >= (self.bar_executed + self.params.exitbars) or self.earn(5):
            ind1=[self.mfi[0]>73,self.since_last() >=self.params.exitbars,self.take_profit()]

            if np.sum(ind1):
                #print(ind1)
                # SELL, SELL, SELL!!! (with all possible default parameters)
                #self.log('SELL CREATE, %.2f' % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                #print('sell')
                #print(self.position.size)
                self.log('SELL CREATE, %.2f' % self.dataclose[0])
                self.order = self.sell(size=self.position.size)

