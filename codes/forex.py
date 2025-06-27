# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
key='5NB5DVBEY1EAUZRU'
import requests
import pandas as pd
# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
out='USD'
inn='CNY'
url = 'https://www.alphavantage.co/query?function=FX_DAILY&outputsize=full&from_symbol='+out+'&to_symbol='+inn+'&apikey='+key
r = requests.get(url)
data = r.json()
data=data['Time Series FX (Daily)']
df = pd.DataFrame.from_dict(data,orient = 'index')

print(df['4. close'])

