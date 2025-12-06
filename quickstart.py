#!/usr/bin/env python3
"""
Quick Start Script - Demonstrates basic functionality without external dependencies.

This script shows the core functionality of the tech stock scraper using mock data,
so you can understand how it works even without live internet access.
"""
import sys
import os
from datetime import datetime

# Add parent directory to path
# NOTE: This is a temporary solution. For proper usage, install the package:
# pip install -e .
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.models.data_models import NewsArticle, StockData, AnalysisResult
from src.analyzer import TechStockAnalyzer


def create_mock_news_articles():
    """Create sample news articles for demonstration."""
    articles = [
        NewsArticle(
            title="NVIDIA Announces Revolutionary AI Chip Architecture",
            url="https://example.com/nvidia-ai-chip",
            source="Tech News Daily",
            published_date="2024-01-15T10:00:00",
            summary="NVIDIA unveiled its next-generation AI chip, promising 10x performance improvement for large language models and AI training workloads.",
            related_stocks=["NVDA"],
            keywords=["AI", "chip", "technology"]
        ),
        NewsArticle(
            title="Tesla Reports Record Q4 Deliveries",
            url="https://example.com/tesla-deliveries",
            source="Auto Industry News",
            published_date="2024-01-14T15:30:00",
            summary="Tesla announced record quarterly deliveries, exceeding analyst expectations and boosting investor confidence.",
            related_stocks=["TSLA"],
            keywords=["Tesla", "electric vehicle", "deliveries"]
        ),
        NewsArticle(
            title="Apple Faces Supply Chain Challenges in China",
            url="https://example.com/apple-supply-chain",
            source="Business Daily",
            published_date="2024-01-13T09:00:00",
            summary="Apple is grappling with supply chain disruptions affecting iPhone production, potentially impacting Q1 revenue.",
            related_stocks=["AAPL"],
            keywords=["Apple", "supply chain", "production"]
        ),
        NewsArticle(
            title="Microsoft Azure Gains Market Share in Cloud Computing",
            url="https://example.com/microsoft-azure",
            source="Cloud Tech Today",
            published_date="2024-01-12T14:00:00",
            summary="Microsoft's Azure platform continues to gain market share, with strong growth in enterprise cloud services.",
            related_stocks=["MSFT"],
            keywords=["Microsoft", "Azure", "cloud computing"]
        ),
        NewsArticle(
            title="Meta Introduces Advanced AI for Content Moderation",
            url="https://example.com/meta-ai-moderation",
            source="Social Media Insider",
            published_date="2024-01-11T11:00:00",
            summary="Meta announced new AI-powered content moderation tools that promise to improve safety across its platforms.",
            related_stocks=["META"],
            keywords=["Meta", "AI", "content moderation"]
        ),
    ]
    return articles


def create_mock_stock_data():
    """Create sample stock data for demonstration."""
    stocks = [
        StockData(
            ticker="NVDA",
            company_name="NVIDIA Corporation",
            current_price=495.50,
            previous_close=482.30,
            open_price=485.00,
            day_high=498.75,
            day_low=483.20,
            volume=45234567,
            market_cap=1220450000000,
            pe_ratio=92.5,
            fifty_two_week_high=502.30,
            fifty_two_week_low=310.50
        ),
        StockData(
            ticker="TSLA",
            company_name="Tesla Inc.",
            current_price=248.30,
            previous_close=242.80,
            open_price=243.50,
            day_high=250.10,
            day_low=241.90,
            volume=102345678,
            market_cap=785230000000,
            pe_ratio=75.3,
            fifty_two_week_high=299.29,
            fifty_two_week_low=152.37
        ),
        StockData(
            ticker="AAPL",
            company_name="Apple Inc.",
            current_price=185.20,
            previous_close=187.50,
            open_price=187.00,
            day_high=187.80,
            day_low=184.50,
            volume=56789012,
            market_cap=2890000000000,
            pe_ratio=28.7,
            fifty_two_week_high=199.62,
            fifty_two_week_low=164.08
        ),
    ]
    return stocks


def main():
    """Demonstrate the tech stock analyzer with mock data."""
    
    print("=" * 80)
    print("Tech Stock News & Analysis - Quick Start Demo")
    print("=" * 80)
    print("\nThis demo uses mock data to show how the system works.")
    print("Run 'python main.py' with internet access for real data.\n")
    
    # Create mock data
    print("[1/3] Creating sample news articles...")
    articles = create_mock_news_articles()
    print(f"✓ Created {len(articles)} sample articles")
    
    print("\n[2/3] Creating sample stock data...")
    stocks = create_mock_stock_data()
    print(f"✓ Created {len(stocks)} sample stocks")
    
    print("\n[3/3] Analyzing stocks with sentiment...")
    analyzer = TechStockAnalyzer()
    
    # Add sentiment scores to articles
    articles = analyzer.analyze_articles(articles)
    
    # Analyze each stock
    results = []
    for stock in stocks:
        # Find related articles
        related = [a for a in articles if stock.ticker in (a.related_stocks or [])]
        
        if related:
            result = analyzer.generate_stock_analysis(stock, related)
            results.append(result)
    
    print(f"✓ Analyzed {len(results)} stocks\n")
    
    # Display results
    print("=" * 80)
    print("ANALYSIS RESULTS")
    print("=" * 80)
    
    for result in results:
        print(f"\n{result.ticker} - {result.company_name}")
        print("-" * 80)
        
        # Stock metrics
        stock_data = result.stock_data
        price_change = stock_data['current_price'] - stock_data['previous_close']
        price_change_pct = (price_change / stock_data['previous_close'] * 100)
        
        print(f"Current Price: ${stock_data['current_price']:.2f}")
        print(f"Price Change: ", end="")
        if price_change >= 0:
            print(f"+${price_change:.2f} (+{price_change_pct:.2f}%) 📈")
        else:
            print(f"${price_change:.2f} ({price_change_pct:.2f}%) 📉")
        
        print(f"Volume: {stock_data['volume']:,}")
        print(f"Market Cap: ${stock_data['market_cap']/1e9:.2f}B")
        
        # Sentiment analysis
        print(f"\nNews Sentiment:")
        print(f"  Articles: {result.news_count}")
        print(f"  Sentiment: {result.sentiment_summary}")
        print(f"  Score: {result.average_sentiment:.3f} (range: -1 to +1)")
        
        # Recommendation
        print(f"\nRecommendation: {result.recommendation}")
        print(f"Confidence: {result.confidence_score:.2f}")
        
        # Show headlines
        if result.related_news:
            print(f"\nRelated Headlines:")
            for article in result.related_news:
                sentiment = article.get('sentiment_score', 0) or 0
                emoji = "📈" if sentiment > 0.1 else "📉" if sentiment < -0.1 else "➡️"
                print(f"  {emoji} {article['title']}")
    
    print("\n" + "=" * 80)
    print("Demo Complete!")
    print("=" * 80)
    print()
    print("Key Features Demonstrated:")
    print("  ✓ News article data collection and storage")
    print("  ✓ Stock price tracking and metrics")
    print("  ✓ Sentiment analysis on news content")
    print("  ✓ Automated recommendation generation")
    print("  ✓ Confidence scoring system")
    print()
    print("Next Steps:")
    print("  1. Install dependencies: pip install -r requirements.txt")
    print("  2. Run with live data: python main.py")
    print("  3. View examples: python examples/usage_examples.py")
    print("  4. Read documentation: README.md and SETUP.md")
    print("  5. Plan ML implementation: ML_IMPLEMENTATION_PLAN.md")
    print()
    print("⚠️  DISCLAIMER: This is for educational purposes only.")
    print("    Not financial advice. Do your own research before investing.")
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nDemo cancelled by user.")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
