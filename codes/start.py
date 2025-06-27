from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import datetime  # For datetime objects
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])

# Import the backtrader platform
import backtrader as bt
import numpy as np
import yfinance as yf
if __name__ == "__main__":
    package=str(sys.argv[2])
    stock=str(sys.argv[1])


def back_test_stock(stock,from_file='unified_strategy0',strategy_name='TestStrategy',commission=0.005,verbose=True,plot=True):
    #if __name__ == '__main__':
        # Create a cerebro entity
    try:
        eps=7./3 - 4./3 -1
        strategy_class=__import__(from_file, fromlist=[strategy_name])
        cerebro = bt.Cerebro()
        cerebro.addstrategy(getattr(strategy_class, strategy_name))
        # Datas are in a subfolder of the samples. Need to find where the script is
        # because it could have been called from anywhere
        #modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
        #datapath = os.path.join(modpath, 'MSFT.csv')
        #print(stock)
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
        #print('data_added')
        # Set our desired cash start
        cerebro.broker.setcash(100000.0)
        cerebro.broker.setcommission(commission=commission)
        dic={'stock_name':stock,'starting_val':cerebro.broker.getvalue()}
        result=cerebro.run()
        dic['finishing_val']=cerebro.broker.getvalue()
        dic['trades']=result[0].total_trades
        dic['success_rate']=result[0].correct_trades/(result[0].total_trades+eps)
        dic['returns']=result[0].pnl
        dic['mean_return']=np.mean(result[0].pnl)
        dic['std_return']=np.std(result[0].pnl)
        if verbose:
            print(stock)
            # Print out the starting conditions
            print('Starting Portfolio Value: %.2f' % dic['starting_val'])
            # Run over everything
            print('Total trades: {}, success rate:{}'.format(dic['trades'],dic['success_rate']))
            print('All returns:{}'.format(dic['returns']))
            print('Mean return: {}, Std return: {}'.format(dic['mean_return'],dic['std_return']))
            # Print out the final result
            print('Final Portfolio Value: %.2f' % dic['finishing_val'])
        if plot:
            cerebro.plot()
        return dic,result
    except:
        return None

