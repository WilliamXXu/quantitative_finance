from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from threading import Thread
import time
import yfinance as yf
import os
import json
from datetime import datetime
import pandas as pd

class StockMetadataSystem:
    """
    A comprehensive system to retrieve all metadata for a given stock using yfinance.
    """
    
    def __init__(self, ticker_symbol):
        """
        Initialize the system with a stock ticker symbol.
        
        Parameters:
        ticker_symbol (str): The stock ticker symbol (e.g., 'AAPL', 'GOOGL')
        """
        self.ticker_symbol = ticker_symbol.upper()
        self.ticker = yf.Ticker(self.ticker_symbol)
        self.metadata = {}
        
    def get_basic_info(self):
        """Get comprehensive basic information about the stock."""
        try:
            info = self.ticker.info
            self.metadata['basic_info'] = info
            return info
        except Exception as e:
            print(f"Error fetching basic info: {e}")
            return None
    
    def get_fast_info(self):
        """Get fast access to key metrics."""
        try:
            fast_info = self.ticker.fast_info
            self.metadata['fast_info'] = {
                'last_price': fast_info.get('lastPrice'),
                'previous_close': fast_info.get('previousClose'),
                'open': fast_info.get('open'),
                'day_high': fast_info.get('dayHigh'),
                'day_low': fast_info.get('dayLow'),
                'volume': fast_info.get('volume'),
                'market_cap': fast_info.get('marketCap'),
                'shares': fast_info.get('shares'),
                'currency': fast_info.get('currency'),
                'timezone': fast_info.get('timezone')
            }
            return self.metadata['fast_info']
        except Exception as e:
            print(f"Error fetching fast info: {e}")
            return None
    
    def get_history_metadata(self):
        """Get historical data metadata."""
        try:
            hist_metadata = self.ticker.history_metadata
            self.metadata['history_metadata'] = hist_metadata
            return hist_metadata
        except Exception as e:
            print(f"Error fetching history metadata: {e}")
            return None
    
    def get_isin(self):
        """Get ISIN (International Securities Identification Number)."""
        try:
            isin = self.ticker.isin
            self.metadata['isin'] = isin
            return isin
        except Exception as e:
            print(f"Error fetching ISIN: {e}")
            return None
    
    def get_major_holders(self):
        """Get major holders information."""
        try:
            major_holders = self.ticker.major_holders
            self.metadata['major_holders'] = major_holders.to_dict() if major_holders is not None else None
            return major_holders
        except Exception as e:
            print(f"Error fetching major holders: {e}")
            return None
    
    def get_institutional_holders(self):
        """Get institutional holders information."""
        try:
            inst_holders = self.ticker.institutional_holders
            self.metadata['institutional_holders'] = inst_holders.to_dict() if inst_holders is not None else None
            return inst_holders
        except Exception as e:
            print(f"Error fetching institutional holders: {e}")
            return None
    
    def get_mutualfund_holders(self):
        """Get mutual fund holders information."""
        try:
            mf_holders = self.ticker.mutualfund_holders
            self.metadata['mutualfund_holders'] = mf_holders.to_dict() if mf_holders is not None else None
            return mf_holders
        except Exception as e:
            print(f"Error fetching mutual fund holders: {e}")
            return None
    
    def get_insider_transactions(self):
        """Get insider transactions."""
        try:
            insider_trans = self.ticker.insider_transactions
            self.metadata['insider_transactions'] = insider_trans.to_dict() if insider_trans is not None else None
            return insider_trans
        except Exception as e:
            print(f"Error fetching insider transactions: {e}")
            return None
        
    def get_all_metadata(self, silent=True, use_cache=True,directory='metadata/'):
        """
        Retrieve all available metadata for the stock, with optional cache.

        Parameters:
        silent (bool): Suppress output if True (default: True).
        use_cache (bool): Use cached file if available (default: True).

        Returns:
        dict: Comprehensive metadata dictionary.
        """
        # Define a consistent cache filename
        cache_file = directory+f"{self.ticker_symbol}_metadata.json"
        
        # Check for cache
        if use_cache and os.path.exists(cache_file):
            if not silent:
                print(f"✓ Loading metadata from cache: {cache_file}")
            with open(cache_file, "r") as f:
                self.metadata = json.load(f)
            return self.metadata

        # If no cache, proceed with normal retrieval
        if not silent:
            print(f"Fetching all metadata for {self.ticker_symbol}...\n")
            print("✓ Fetching basic info...")
        self.get_basic_info()

        if not silent:
            print("✓ Fetching fast info...")
        self.get_fast_info()

        if not silent:
            print("✓ Fetching history metadata...")
        # self.get_history_metadata()

        if not silent:
            print("✓ Fetching ISIN...")
        self.get_isin()

        if not silent:
            print("✓ Fetching major holders...")
        self.get_major_holders()

        if not silent:
            print("✓ Fetching institutional holders...")
        self.get_institutional_holders()

        if not silent:
            print("✓ Fetching mutual fund holders...")
        self.get_mutualfund_holders()

        if not silent:
            print("✓ Fetching insider transactions...")
        self.get_insider_transactions()

        if not silent:
            print(f"\n✓ All metadata retrieved successfully!")
        
        # Save to cache for future runs
        with open(cache_file, "w") as f:
            json.dump(self.metadata, f, indent=2, default=str)

        return self.metadata
        
    def display_key_metrics(self):
        """Display key metrics in a readable format."""
        if not self.metadata:
            self.get_all_metadata()
        
        info = self.metadata.get('basic_info', {})
        
        print(f"\n{'='*60}")
        print(f"KEY METRICS FOR {self.ticker_symbol}")
        print(f"{'='*60}\n")
        
        # Company Information
        print("COMPANY INFORMATION:")
        print(f"  Name: {info.get('longName', 'N/A')}")
        print(f"  Sector: {info.get('sector', 'N/A')}")
        print(f"  Industry: {info.get('industry', 'N/A')}")
        print(f"  Country: {info.get('country', 'N/A')}")
        print(f"  Website: {info.get('website', 'N/A')}")
        print(f"  Employees: {info.get('fullTimeEmployees', 'N/A')}")
        
        # Market Data
        print("\nMARKET DATA:")
        print(f"  Current Price: ${info.get('currentPrice', 'N/A')}")
        print(f"  Market Cap: ${info.get('marketCap', 'N/A'):,}" if info.get('marketCap') else "  Market Cap: N/A")
        print(f"  52-Week High: ${info.get('fiftyTwoWeekHigh', 'N/A')}")
        print(f"  52-Week Low: ${info.get('fiftyTwoWeekLow', 'N/A')}")
        print(f"  Volume: {info.get('volume', 'N/A'):,}" if info.get('volume') else "  Volume: N/A")
        print(f"  Avg Volume: {info.get('averageVolume', 'N/A'):,}" if info.get('averageVolume') else "  Avg Volume: N/A")
        
        # Valuation Metrics
        print("\nVALUATION METRICS:")
        print(f"  P/E Ratio (TTM): {info.get('trailingPE', 'N/A')}")
        print(f"  Forward P/E: {info.get('forwardPE', 'N/A')}")
        print(f"  PEG Ratio: {info.get('pegRatio', 'N/A')}")
        print(f"  Price to Book: {info.get('priceToBook', 'N/A')}")
        print(f"  Price to Sales: {info.get('priceToSalesTrailing12Months', 'N/A')}")
        
        # Financial Metrics
        print("\nFINANCIAL METRICS:")
        print(f"  Revenue: ${info.get('totalRevenue', 'N/A'):,}" if info.get('totalRevenue') else "  Revenue: N/A")
        print(f"  Profit Margin: {info.get('profitMargins', 'N/A')}")
        print(f"  Operating Margin: {info.get('operatingMargins', 'N/A')}")
        print(f"  ROE: {info.get('returnOnEquity', 'N/A')}")
        print(f"  ROA: {info.get('returnOnAssets', 'N/A')}")
        
        # Dividend Info
        print("\nDIVIDEND INFORMATION:")
        print(f"  Dividend Rate: ${info.get('dividendRate', 'N/A')}")
        print(f"  Dividend Yield: {info.get('dividendYield', 'N/A')}")
        print(f"  Payout Ratio: {info.get('payoutRatio', 'N/A')}")
        
        print(f"\n{'='*60}\n")
    
    def save_metadata_to_file(self, filename=None,directory='metadata/'):
        """
        Save metadata to a JSON file.
        
        Parameters:
        filename (str): Output filename (default: {ticker}_metadata.json)
        """
        if not self.metadata:
            self.get_all_metadata()
        
        if filename is None:
            filename = directory+f"{self.ticker_symbol}_metadata.json"
        
        # Convert DataFrames to dict for JSON serialization
        serializable_metadata = {}
        for key, value in self.metadata.items():
            if isinstance(value, pd.DataFrame):
                serializable_metadata[key] = value.to_dict()
            else:
                serializable_metadata[key] = value
        
        try:
            with open(filename, 'w') as f:
                json.dump(serializable_metadata, f, indent=2, default=str)
            print(f"✓ Metadata saved to {filename}")
        except Exception as e:
            print(f"Error saving metadata: {e}")




def yfinance_quick_live_prices(symbols):
    # yf.Tickers batch fetch avoids repeated network calls when possible
    tickers = yf.Tickers(" ".join(symbols))
    out = dict()
    for s in symbols:
        print(s)
        t = getattr(tickers.tickers, s, None) or yf.Ticker(s)
        info = t.fast_info or {}
        # Prefer fast_info last_price; fallback to info['regularMarketPrice']
        price = getattr(t, "fast_info", {}).get("last_price")
        if price is None:
            try:
                price = t.info.get("regularMarketPrice")
            except Exception:
                price = None
        out[s]=price
    return out



class IBApp(EWrapper, EClient):
    def __init__(self, target_account):
        EClient.__init__(self, self)
        self.target_account = target_account
        self.accounts = []
        self.positions = []
        self.account_values = []
        self.news_providers=[]
        self.greeks_cache = {}
        self.cash_balance = {}
        
    def error(self, reqId, errorCode, errorString, advancedOrderReject=""):
        print(f"Error: {reqId}, {errorCode}, {errorString}")
    
    def managedAccounts(self, accountsList: str):
        self.accounts = accountsList.split(",")
        print(f"Available accounts: {self.accounts}")
    
    def nextValidId(self, orderId):
        print(f"Requesting portfolio for account: {self.target_account}")
        self.reqAccountUpdates(True, self.target_account)
        self.reqNewsProviders()
        self.reqAccountSummary(9001, "All", "$LEDGER:ALL")

    def newsProviders(self, newsProviders):
        """Callback for available news providers"""
        print("\nAvailable News Providers:")
        for provider in newsProviders:
            print(f"  {provider.code}: {provider.name}")
            self.news_providers.append(provider.code)
    
    def updatePortfolio(self, contract: Contract, position: float, 
                       marketPrice: float, marketValue: float, 
                       averageCost: float, unrealizedPNL: float, 
                       realizedPNL: float, accountName: str):
        print(f"Portfolio Update - Account: {accountName}")
        print(f"  Symbol: {contract.symbol}, SecType: {contract.secType}")
        print(f"  Position: {position}, Market Value: ${marketValue}")
        print(f"  Avg Cost: ${averageCost}, Unrealized P&L: ${unrealizedPNL}")
        
        self.positions.append({
            'account': accountName,
            'contract':contract,
            # 'symbol': contract.symbol,
            # 'secType': contract.secType,
            # 'exchange': contract.primaryExchange,
            'position': position,
            'marketPrice': marketPrice,
            'marketValue': marketValue,
            'avgCost': averageCost,
            'unrealizedPNL': unrealizedPNL,
            'realizedPNL': realizedPNL
        })
        #self.positions.append(contract)

    def accountSummary(self, reqId: int, account: str, tag: str, value: str, currency: str):
        if tag == 'CashBalance':
            print(f"Cash Balance for account {account}, currency {currency}: {value}")
            if account not in self.cash_balance:
                self.cash_balance[account] = {}
            self.cash_balance[account][currency] = float(value)

    def accountSummaryEnd(self, reqId: int):
        print("Account summary download complete.")

    def accountDownloadEnd(self, accountName: str):
        print(f"\nAccount data download complete for: {accountName}")
    
    def stop(self, account_id):
        self.reqAccountUpdates(False, account_id)
        self.disconnect()