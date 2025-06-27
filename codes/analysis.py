import numpy as np
import pickle
import datetime  # For datetime objects
import sys
total=0
correct=0
res=[]
file_name=sys.argv[1]
present=datetime.datetime.today()
li=pickle.load(open('results/'+file_name, "rb" ) )
for t in li:
    if not t is None:
        result=t[0] 
        if result['trades']>0:
            total+=result['trades']
            #print(total)
            correct+=result['success_rate']*result['trades']
            res=res+result['returns']
            dt=t[1][0].lastBuy

            if dt>present:
                with open('res.txt','a+') as f:
                    f.write(result['stock_name'])

print(total)
print(correct)
print(correct/total)
print(np.mean(res))
print(np.std(res))
