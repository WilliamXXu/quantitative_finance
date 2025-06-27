from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])
import pickle
# Import the backtrader platform
import backtrader as bt
import numpy as np
import yfinance as yf
from start import back_test_stock
import seaborn as sns
import matplotlib.pyplot as plt

from joblib import Parallel, delayed


#package=str(sys.argv[2])

#if __name__ == '__main__':
    # Create a cerebro entity


# Datas are in a subfolder of the samples. Need to find where the script is
# because it could have been called from anywhere
#modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
#datapath = os.path.join(modpath, 'MSFT.csv')

#filel = open('mfi.txt','a+')
ending=''
save_name=sys.argv[2]
filel=open(str(sys.argv[1]),'a+')
filel.seek(0)
multiprocess=True
n_jobs=5

stock_list=filel.read().splitlines()

filel.close()





if multiprocess:
    generator=Parallel(n_jobs=n_jobs)(delayed(back_test_stock)(stock_list[i]+ending,verbose=False,plot=False) for i in range(len(stock_list)))
else:
    generator=(back_test_stock(stock_list[i]+ending,verbose=True,plot=False) for i in range(len(stock_list)))
li=list(generator)

pickle.dump(li, open('results/'+save_name+'.pkl', "wb" ))


