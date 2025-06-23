import yfinance as yf

stock="MSFT"
msft = yf.Ticker(stock)
hist = msft.history(period="1mo")
hist.to_csv("{}.csv".format(stock))
print(hist)
print(type(hist))