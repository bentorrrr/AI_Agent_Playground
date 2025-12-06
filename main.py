"""
Main application for Tech Stock News & Analysis Scraper.
"""
import os
import sys
from datetime import datetime

# Add parent directory to path
# NOTE: This is a temporary solution. For proper usage, install the package:
# pip install -e .
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.scrapers import NewsScraper, StockScraper
from src.analyzer import TechStockAnalyzer
from src.utils import save_to_json, load_from_json, merge_and_deduplicate, filter_by_date
from config import DATA_SETTINGS, TECH_STOCKS


def main():
    """Main function to run the tech stock scraper and analyzer."""
    
    print("=" * 80)
    print("Tech Stock News & Analysis Scraper")
    print("Magnificent 7 Tech Stocks: AAPL, MSFT, AMZN, GOOGL, META, NVDA, TSLA")
    print("=" * 80)
    print()
    
    # Create data directory if it doesn't exist
    data_dir = DATA_SETTINGS['data_dir']
    os.makedirs(data_dir, exist_ok=True)
    
    # File paths
    news_file = os.path.join(data_dir, DATA_SETTINGS['news_file'])
    stock_file = os.path.join(data_dir, DATA_SETTINGS['stock_file'])
    analysis_file = os.path.join(data_dir, DATA_SETTINGS['analysis_file'])
    
    # Step 1: Scrape news articles
    print("\n[Step 1/4] Scraping tech news articles...")
    print("-" * 80)
    news_scraper = NewsScraper()
    new_articles = news_scraper.scrape_all_sources()
    
    # Convert to dict format
    new_articles_dict = [article.to_dict() for article in new_articles]
    
    # Load existing articles and merge
    existing_articles = load_from_json(news_file)
    all_articles = merge_and_deduplicate(existing_articles, new_articles_dict, key='url')
    
    # Filter to keep only recent articles (last 30 days)
    all_articles = filter_by_date(all_articles, date_field='published_date', days=30)
    
    # Save articles
    save_to_json(all_articles, news_file)
    print(f"Total articles in database: {len(all_articles)}")
    
    # Step 2: Fetch stock data
    print("\n[Step 2/4] Fetching current stock data...")
    print("-" * 80)
    stock_scraper = StockScraper()
    stocks = stock_scraper.fetch_all_tech_stocks()
    
    # Convert to dict format and save
    stocks_dict = [stock.to_dict() for stock in stocks]
    save_to_json(stocks_dict, stock_file)
    
    # Step 3: Analyze stocks with sentiment
    print("\n[Step 3/4] Analyzing stocks with news sentiment...")
    print("-" * 80)
    analyzer = TechStockAnalyzer()
    analysis_results = analyzer.analyze_all_stocks(stocks, new_articles)
    
    # Convert to dict format and save
    results_dict = [result.to_dict() for result in analysis_results]
    save_to_json(results_dict, analysis_file)
    
    # Step 4: Display summary
    print("\n[Step 4/4] Analysis Summary")
    print("=" * 80)
    
    for result in analysis_results:
        print(f"\n{result.ticker} - {result.company_name}")
        print("-" * 80)
        
        # Stock data
        stock_data = result.stock_data
        current_price = stock_data['current_price']
        previous_close = stock_data['previous_close']
        price_change = current_price - previous_close
        price_change_pct = (price_change / previous_close * 100) if previous_close > 0 else 0
        
        print(f"Price: ${current_price:.2f} ", end="")
        if price_change >= 0:
            print(f"(+${price_change:.2f}, +{price_change_pct:.2f}%)")
        else:
            print(f"(${price_change:.2f}, {price_change_pct:.2f}%)")
        
        print(f"Volume: {stock_data['volume']:,}")
        
        if stock_data.get('market_cap'):
            market_cap_b = stock_data['market_cap'] / 1e9
            print(f"Market Cap: ${market_cap_b:.2f}B")
        
        # News sentiment
        print(f"\nNews Analysis:")
        print(f"  Articles Found: {result.news_count}")
        print(f"  Sentiment: {result.sentiment_summary}")
        print(f"  Average Score: {result.average_sentiment:.3f} (range: -1 to +1)")
        
        # Recommendation
        print(f"\nRecommendation: {result.recommendation}")
        print(f"Confidence: {result.confidence_score:.2f}")
        
        # Show some recent headlines
        if result.related_news:
            print(f"\nRecent Headlines (showing up to 3):")
            for i, article in enumerate(result.related_news[:3], 1):
                sentiment_emoji = "📈" if article.get('sentiment_score', 0) > 0.1 else "📉" if article.get('sentiment_score', 0) < -0.1 else "➡️"
                print(f"  {sentiment_emoji} {article['title'][:100]}{'...' if len(article['title']) > 100 else ''}")
    
    print("\n" + "=" * 80)
    print("Analysis complete! Data saved to:")
    print(f"  - News: {news_file}")
    print(f"  - Stocks: {stock_file}")
    print(f"  - Analysis: {analysis_file}")
    print("=" * 80)
    print()
    
    print("NOTE: The recommendations provided are based on a simple rule-based system")
    print("and should NOT be used as actual investment advice. This is a demonstration")
    print("tool for educational purposes only. Future versions will include ML models.")
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
