import backtrader as bt
import numpy as np
import time

#sharp

class TestStrategy(bt.Strategy):
    params = (('exitbars', 30),('maperiod', 14),('profit_percent_max',8),('profit_percent_min',2),('profit_percent_daily',3)\
              ,('mfi_low',26),('mfi_still_low',30),('dive_percent',0.0001),('more_dive_percent',0.00001),('observation_window',14),('add_window',21)\
                ,('max_bet',3),('mfi_high',73))
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
                self.cost_basis+=order.executed.value+order.executed.comm
                if self.verbose:
                    print('buy price: {}'.format(self.buyprice))
            else:  # Sell
                if self.verbose:
                    print('sell price: {}'.format(order.executed.price))
                self.cost_basis+=order.executed.comm
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

        if trade.isclosed:
            #self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f value %.2f' %(trade.pnl, trade.pnlcomm,trade.price))
            res=trade.pnlcomm/self.cost_basis
            if self.verbose:
                print('pnl: {}, cost basis: {}\n'.format(trade.pnlcomm,self.cost_basis))
            eps=7./3 - 4./3 -1
            self.total_trades+=1
            if res>eps:
                self.correct_trades+=1
            if res<-0.5 and self.verbose:
                print('huge loss!')
                #time.sleep(5)
            self.pnl.append(res)
            self.cost_basis=0

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self,verbose=False):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close

        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None
        self.flag=False
        self.priceStart=None
        self.barStart=False
        self.correct_trades=0
        self.total_trades=0
        self.pnl=[]
        self.lastBuy=None
        self.cost_basis=0
        self.verbose=verbose

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
        if profit > self.params.profit_percent_max or (profit>self.params.profit_percent_min and profit>day/self.params.profit_percent_daily):
                return True
        return False

    def next(self):
        # Simply log the closing price of the series from the reference
        #self.log('Close, %.2f' % self.dataclose[0])
        #self.log(self.sma[0])
        if not self.position:

            if self.mfi[0] <self.params.mfi_low:
                # current close less than previous close
                    # BUY, BUY, BUY!!! (with all possible default parameters)
                    '''
                    self.log('BUY CREATE, %.2f' % self.dataclose[0])
                    self.order = self.buy()
                    '''
                    self.flag=True
                    self.priceStart=self.dataclose[0]
                    self.barStart=len(self)

            if self.flag and self.barStart:

                ind=[self.mfi[0] < self.params.mfi_still_low,self.pl(price=self.priceStart)<-self.params.dive_percent,len(self)-self.barStart<self.params.observation_window]
                if np.product(ind) :
                    
                    # current close less than previous close
                        # BUY, BUY, BUY!!! (with all possible default parameters)
                        #self.log('BUY CREATE, %.2f' % self.dataclose[0])
                    self.order = self.buy()
                    if self.verbose:
                        self.log('BUY CREATE')#, %.2f' % self.dataclose[0])
            # Already in the market ... we might sell
        else:
            ind1=[self.mfi[0]>self.params.mfi_high,self.since_last() >=self.params.exitbars,self.take_profit()]
            if np.sum(ind1):
                #print(ind1)
                # SELL, SELL, SELL!!! (with all possible default parameters)
                #self.log('SELL CREATE, %.2f' % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                #print('sell')
                #print(self.position.size)
                self.order = self.sell(size=self.position.size)
                if self.verbose:
                    self.log('SELL CREATE')#, %.2f' % self.dataclose[0])
                self.flag=False
                self.priceStart=None
                self.barStart=False
            else:
                ind=[self.mfi[0] < self.params.mfi_still_low,self.pl(price=self.priceStart)<-self.params.more_dive_percent,len(self)-self.barStart <self.params.add_window,self.position.size<self.params.max_bet]
                #
                if np.product(ind):
                    #print('already')
                    #print(self.position.size)
                    self.order=self.buy()
                    if self.verbose:
                        self.log('BUY MORE CREATE')#, %.2f' % self.dataclose[0])
                #if self.mfi[0]>70 or len(self) >= (self.bar_executed + self.params.exitbars) or self.earn(5):

