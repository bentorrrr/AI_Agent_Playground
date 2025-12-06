"""
Stock data scraper using yfinance to get real-time stock information.
"""
import yfinance as yf
from typing import List, Dict, Optional
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.models.data_models import StockData
from config import TECH_STOCKS


class StockScraper:
    """Scraper for stock data using yfinance."""
    
    def __init__(self):
        self.tech_stocks = TECH_STOCKS
    
    def fetch_stock_data(self, ticker: str) -> Optional[StockData]:
        """
        Fetch current stock data for a given ticker.
        
        Args:
            ticker: Stock ticker symbol (e.g., 'AAPL')
            
        Returns:
            StockData object or None if fetch fails
        """
        try:
            print(f"Fetching stock data for {ticker}...")
            
            # Create ticker object
            stock = yf.Ticker(ticker)
            
            # Get stock info
            info = stock.info
            
            # Get current price (try multiple fields)
            current_price = info.get('currentPrice') or info.get('regularMarketPrice') or info.get('previousClose', 0)
            
            # Get previous close
            previous_close = info.get('previousClose', 0)
            
            # Get open price
            open_price = info.get('open') or info.get('regularMarketOpen', 0)
            
            # Get day high and low
            day_high = info.get('dayHigh') or info.get('regularMarketDayHigh', 0)
            day_low = info.get('dayLow') or info.get('regularMarketDayLow', 0)
            
            # Get volume
            volume = info.get('volume') or info.get('regularMarketVolume', 0)
            
            # Get company name
            company_name = self.tech_stocks.get(ticker, {}).get('name', info.get('longName', ticker))
            
            # Optional fields
            market_cap = info.get('marketCap')
            pe_ratio = info.get('trailingPE') or info.get('forwardPE')
            dividend_yield = info.get('dividendYield')
            fifty_two_week_high = info.get('fiftyTwoWeekHigh')
            fifty_two_week_low = info.get('fiftyTwoWeekLow')
            
            stock_data = StockData(
                ticker=ticker,
                company_name=company_name,
                current_price=float(current_price),
                previous_close=float(previous_close),
                open_price=float(open_price),
                day_high=float(day_high),
                day_low=float(day_low),
                volume=int(volume),
                market_cap=float(market_cap) if market_cap else None,
                pe_ratio=float(pe_ratio) if pe_ratio else None,
                dividend_yield=float(dividend_yield) if dividend_yield else None,
                fifty_two_week_high=float(fifty_two_week_high) if fifty_two_week_high else None,
                fifty_two_week_low=float(fifty_two_week_low) if fifty_two_week_low else None
            )
            
            return stock_data
            
        except Exception as e:
            print(f"Error fetching stock data for {ticker}: {e}")
            return None
    
    def fetch_all_tech_stocks(self) -> List[StockData]:
        """
        Fetch stock data for all configured tech stocks.
        
        Returns:
            List of StockData objects
        """
        all_stock_data = []
        
        for ticker in self.tech_stocks.keys():
            stock_data = self.fetch_stock_data(ticker)
            if stock_data:
                all_stock_data.append(stock_data)
        
        print(f"\nSuccessfully fetched data for {len(all_stock_data)} stocks")
        return all_stock_data
    
    def get_historical_data(self, ticker: str, period: str = "1mo") -> Optional[Dict]:
        """
        Get historical stock data.
        
        Args:
            ticker: Stock ticker symbol
            period: Period for historical data (e.g., '1d', '5d', '1mo', '3mo', '1y')
            
        Returns:
            DataFrame with historical data or None
        """
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period=period)
            
            if not hist.empty:
                return {
                    'ticker': ticker,
                    'period': period,
                    'data': hist.to_dict('records')
                }
            return None
            
        except Exception as e:
            print(f"Error fetching historical data for {ticker}: {e}")
            return None


if __name__ == "__main__":
    # Example usage
    scraper = StockScraper()
    
    print("Fetching stock data for Magnificent 7 tech stocks...\n")
    stocks = scraper.fetch_all_tech_stocks()
    
    print("\n--- Stock Summary ---")
    for stock in stocks:
        print(f"\n{stock.ticker} - {stock.company_name}")
        print(f"  Current Price: ${stock.current_price:.2f}")
        print(f"  Change: ${stock.price_change:.2f} ({stock.price_change_percent:.2f}%)")
        print(f"  Volume: {stock.volume:,}")
        if stock.market_cap:
            print(f"  Market Cap: ${stock.market_cap/1e9:.2f}B")
