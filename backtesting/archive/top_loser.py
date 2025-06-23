import yfinance as yf
import pandas as pd
import time
import random

def get_intraday_losers(tickers, n=10, ending=''):
    """Get top N intraday losers from a predefined S&P 500 ticker list with company details
    
    Returns DataFrame with company name, sector, market cap, current price, and percentage change.
    Includes random sleep intervals between API calls to prevent rate limiting.
    """
    losers = []
    
    def get_market_cap_formatted(market_cap):
        """Convert market cap to readable format"""
        if not market_cap:
            return 'N/A'
        billion = 1_000_000_000
        if market_cap >= billion:
            return f"${round(market_cap/billion, 1)}B"
        else:
            return f"${round(market_cap/1_000_000, 1)}M"
    
    for ticker in tickers:
        print(ticker)
        try:
            # Random sleep between 0 and 3 seconds
            time.sleep(random.uniform(0, 1))
            
            stock = yf.Ticker(ticker+ending)
            data = stock.history(period='1d', interval='1m')
            
            if len(data) < 2:
                continue
                
            latest_price = data['Close'].iloc[-1]
            prev_close = stock.info.get('regularMarketPreviousClose', None)
            
            if prev_close and latest_price:
                pct_change = (latest_price - prev_close) / prev_close * 100
                losers.append({
                    'Ticker': ticker,
                    'Company Name': stock.info.get('longName', 'N/A'),
                    'Sector': stock.info.get('sector', 'N/A'),
                    'Market Cap': get_market_cap_formatted(stock.info.get('marketCap', None)),
                    'Price': round(latest_price, 2),
                    '% Change': round(pct_change, 2)
                })
        except Exception as e:
            continue
    
    losers_df = pd.DataFrame(losers)
    if len(losers_df) == 0:
        return pd.DataFrame(columns=['Ticker', 'Company Name', 'Sector', 'Market Cap', 'Price', '% Change'])
    
    losers_df = losers_df.sort_values(by='% Change').head(n)
    return losers_df[['Ticker', 'Company Name', 'Sector', 'Market Cap', 'Price', '% Change']].reset_index(drop=True)


# if __name__ == '__main__':
#     # Example usage with predefined S&P 500 tickers
#     sp500_tickers = ['FMC', 'EL', 'PYPL', 'MRK', 'CLX', 'MDLZ', 'BALL', 'MRNA', 'MTCH', 'HSY']  # Pass your ticker list here:cite[3]:cite[10]
    
#     n = int(input("Enter number of top losers to retrieve (1-20): "))
#     print(f"\nTop {n} Intraday Losers in S&P 500:")
#     print(get_intraday_losers(sp500_tickers, n).to_string(index=False))
list_name='ftse250.txt'
ending='.L'
list_name='SP500.txt'
ending=''
filel=open('../gathering/data/'+list_name,'a+')
filel.seek(0)
stocklist=filel.read().splitlines()
filel.close()

res=get_intraday_losers(stocklist,ending=ending)
print(res)