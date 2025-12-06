"""
Example script showing how to use individual components of the scraper.
"""
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.scrapers import NewsScraper, StockScraper
from src.analyzer import TechStockAnalyzer
from config import TECH_STOCKS


def example_news_scraper():
    """Example: Scrape and display news articles."""
    print("\n" + "=" * 80)
    print("Example 1: News Scraper")
    print("=" * 80)
    
    scraper = NewsScraper()
    articles = scraper.scrape_all_sources()
    
    # Show articles related to specific stocks
    print("\nArticles related to NVIDIA (NVDA):")
    nvda_articles = [a for a in articles if a.related_stocks and 'NVDA' in a.related_stocks]
    
    for i, article in enumerate(nvda_articles[:3], 1):
        print(f"\n{i}. {article.title}")
        print(f"   Source: {article.source}")
        print(f"   URL: {article.url}")
        print(f"   Summary: {article.summary[:150]}..." if article.summary else "")


def example_stock_scraper():
    """Example: Fetch and display stock data."""
    print("\n" + "=" * 80)
    print("Example 2: Stock Data Scraper")
    print("=" * 80)
    
    scraper = StockScraper()
    
    # Fetch data for a single stock
    stock = scraper.fetch_stock_data('NVDA')
    
    if stock:
        print(f"\n{stock.ticker} - {stock.company_name}")
        print(f"Current Price: ${stock.current_price:.2f}")
        print(f"Previous Close: ${stock.previous_close:.2f}")
        print(f"Change: ${stock.price_change:.2f} ({stock.price_change_percent:.2f}%)")
        print(f"Day Range: ${stock.day_low:.2f} - ${stock.day_high:.2f}")
        print(f"Volume: {stock.volume:,}")
        
        if stock.market_cap:
            print(f"Market Cap: ${stock.market_cap/1e9:.2f}B")
        if stock.pe_ratio:
            print(f"P/E Ratio: {stock.pe_ratio:.2f}")


def example_sentiment_analysis():
    """Example: Analyze sentiment of news articles."""
    print("\n" + "=" * 80)
    print("Example 3: Sentiment Analysis")
    print("=" * 80)
    
    analyzer = TechStockAnalyzer()
    
    # Test sentiment on sample texts
    test_texts = [
        "NVIDIA announces breakthrough AI chip with incredible performance gains!",
        "Tesla faces challenges with declining sales and production issues.",
        "Apple releases new iPhone with minor updates.",
    ]
    
    print("\nSentiment Analysis Examples:")
    for text in test_texts:
        sentiment = analyzer.analyze_sentiment(text)
        sentiment_label = "Positive" if sentiment > 0.1 else "Negative" if sentiment < -0.1 else "Neutral"
        print(f"\nText: {text}")
        print(f"Sentiment: {sentiment_label} (score: {sentiment:.3f})")


def example_full_analysis():
    """Example: Complete analysis combining news and stock data."""
    print("\n" + "=" * 80)
    print("Example 4: Full Stock Analysis")
    print("=" * 80)
    
    # Fetch stock data
    stock_scraper = StockScraper()
    stock = stock_scraper.fetch_stock_data('TSLA')
    
    # Fetch news
    news_scraper = NewsScraper()
    all_articles = news_scraper.scrape_all_sources()
    
    # Filter articles related to Tesla
    tsla_articles = [a for a in all_articles if a.related_stocks and 'TSLA' in a.related_stocks]
    
    # Analyze
    analyzer = TechStockAnalyzer()
    if stock and tsla_articles:
        result = analyzer.generate_stock_analysis(stock, tsla_articles)
        
        print(f"\n{result.ticker} - {result.company_name}")
        print(f"Price: ${result.stock_data['current_price']:.2f}")
        print(f"Related News Articles: {result.news_count}")
        print(f"Average Sentiment: {result.average_sentiment:.3f}")
        print(f"Sentiment Summary: {result.sentiment_summary}")
        print(f"Recommendation: {result.recommendation}")
        print(f"Confidence Score: {result.confidence_score:.2f}")
    else:
        print("Could not fetch data for analysis")


def main():
    """Run all examples."""
    print("\n" + "=" * 80)
    print("Tech Stock Scraper - Usage Examples")
    print("=" * 80)
    
    try:
        example_news_scraper()
        example_stock_scraper()
        example_sentiment_analysis()
        example_full_analysis()
        
        print("\n" + "=" * 80)
        print("Examples completed!")
        print("=" * 80)
        print()
        
    except Exception as e:
        print(f"\nError running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
