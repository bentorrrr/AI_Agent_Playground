"""
Analyzer module for combining news and stock data with sentiment analysis.
"""
from textblob import TextBlob
from typing import List, Dict, Any, Optional
from datetime import datetime
import sys
import os

# Add parent directory to path for imports
# NOTE: This is a temporary solution. For proper usage, install the package:
# pip install -e .
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.models.data_models import NewsArticle, StockData, AnalysisResult

# Constants for recommendation algorithm
CONFIDENCE_SCALING_FACTOR = 10  # Number of articles needed for full confidence
POSITIVE_SENTIMENT_THRESHOLD = 0.2  # Threshold for positive sentiment
NEGATIVE_SENTIMENT_THRESHOLD = -0.2  # Threshold for negative sentiment


class TechStockAnalyzer:
    """Analyzer for tech stocks combining news sentiment and stock data."""
    
    def __init__(self):
        pass
    
    def analyze_sentiment(self, text: str) -> float:
        """
        Analyze sentiment of text using TextBlob.
        
        Args:
            text: Text to analyze
            
        Returns:
            Sentiment polarity score between -1 (negative) and 1 (positive)
        """
        if not text:
            return 0.0
        
        try:
            blob = TextBlob(text)
            return blob.sentiment.polarity
        except Exception as e:
            print(f"Error analyzing sentiment: {e}")
            return 0.0
    
    def analyze_articles(self, articles: List[NewsArticle]) -> List[NewsArticle]:
        """
        Add sentiment scores to news articles.
        
        Args:
            articles: List of NewsArticle objects
            
        Returns:
            List of NewsArticle objects with sentiment scores
        """
        for article in articles:
            # Combine title and summary for sentiment analysis
            text = f"{article.title} {article.summary or ''}"
            article.sentiment_score = self.analyze_sentiment(text)
        
        return articles
    
    def generate_stock_analysis(self, 
                                stock_data: StockData, 
                                related_articles: List[NewsArticle]) -> AnalysisResult:
        """
        Generate analysis report for a stock combining price data and news sentiment.
        
        Args:
            stock_data: StockData object
            related_articles: List of NewsArticle objects related to this stock
            
        Returns:
            AnalysisResult object
        """
        # Calculate average sentiment from related articles
        sentiments = [article.sentiment_score for article in related_articles 
                     if article.sentiment_score is not None]
        
        avg_sentiment = sum(sentiments) / len(sentiments) if sentiments else 0.0
        
        # Generate sentiment summary
        if avg_sentiment > POSITIVE_SENTIMENT_THRESHOLD:
            sentiment_summary = "Positive - News sentiment is generally favorable"
        elif avg_sentiment < NEGATIVE_SENTIMENT_THRESHOLD:
            sentiment_summary = "Negative - News sentiment is generally unfavorable"
        else:
            sentiment_summary = "Neutral - News sentiment is mixed or neutral"
        
        # Generate basic recommendation (this is a placeholder for future ML model)
        recommendation = self._generate_recommendation(stock_data, avg_sentiment)
        
        # Calculate confidence score based on article volume and sentiment strength
        # More articles and stronger sentiment = higher confidence
        confidence_score = min(abs(avg_sentiment) * len(related_articles) / CONFIDENCE_SCALING_FACTOR, 1.0)
        
        # Convert articles to dict format
        articles_dict = [article.to_dict() for article in related_articles]
        
        analysis = AnalysisResult(
            ticker=stock_data.ticker,
            company_name=stock_data.company_name,
            analysis_date=datetime.now().isoformat(),
            stock_data=stock_data.to_dict(),
            related_news=articles_dict,
            sentiment_summary=sentiment_summary,
            average_sentiment=avg_sentiment,
            news_count=len(related_articles),
            recommendation=recommendation,
            confidence_score=confidence_score
        )
        
        return analysis
    
    def _generate_recommendation(self, stock_data: StockData, sentiment: float) -> str:
        """
        Generate a basic investment recommendation.
        
        NOTE: This is a simplified placeholder. In production, this should be
        replaced with a proper ML model trained on historical data.
        
        Args:
            stock_data: StockData object
            sentiment: Average news sentiment score
            
        Returns:
            Recommendation string
        """
        price_change_percent = stock_data.price_change_percent
        
        # Simple rule-based recommendation (placeholder)
        # Using threshold constants for consistency
        if sentiment > POSITIVE_SENTIMENT_THRESHOLD + 0.1 and price_change_percent > 0:
            return "BUY - Strong positive sentiment and upward price momentum"
        elif sentiment > 0.1 and price_change_percent > 2:
            return "BUY - Positive sentiment with strong price movement"
        elif sentiment < NEGATIVE_SENTIMENT_THRESHOLD - 0.1 and price_change_percent < 0:
            return "SELL - Negative sentiment and downward price momentum"
        elif sentiment < -0.1 and price_change_percent < -2:
            return "SELL - Negative sentiment with declining price"
        elif abs(price_change_percent) < 1 and abs(sentiment) < 0.1:
            return "HOLD - Stable price and neutral sentiment"
        else:
            return "HOLD - Mixed signals, monitor for clearer trends"
    
    def analyze_all_stocks(self, 
                          stock_data_list: List[StockData],
                          all_articles: List[NewsArticle]) -> List[AnalysisResult]:
        """
        Generate analysis for all stocks.
        
        Args:
            stock_data_list: List of StockData objects
            all_articles: List of all NewsArticle objects
            
        Returns:
            List of AnalysisResult objects
        """
        # First, add sentiment scores to all articles
        articles_with_sentiment = self.analyze_articles(all_articles)
        
        # Generate analysis for each stock
        results = []
        
        for stock in stock_data_list:
            # Filter articles related to this stock
            related = [article for article in articles_with_sentiment 
                      if article.related_stocks and stock.ticker in article.related_stocks]
            
            # Generate analysis
            analysis = self.generate_stock_analysis(stock, related)
            results.append(analysis)
            
            print(f"\nAnalyzed {stock.ticker}: {len(related)} related articles, "
                  f"avg sentiment: {analysis.average_sentiment:.3f}")
        
        return results


if __name__ == "__main__":
    # Example usage
    from src.scrapers import NewsScraper, StockScraper
    
    print("Fetching stock data and news...\n")
    
    # Fetch stock data
    stock_scraper = StockScraper()
    stocks = stock_scraper.fetch_all_tech_stocks()
    
    # Fetch news
    news_scraper = NewsScraper()
    articles = news_scraper.scrape_all_sources()
    
    # Analyze
    analyzer = TechStockAnalyzer()
    results = analyzer.analyze_all_stocks(stocks, articles)
    
    print("\n--- Analysis Summary ---")
    for result in results:
        print(f"\n{result.ticker} - {result.company_name}")
        print(f"  Current Price: ${result.stock_data['current_price']:.2f}")
        print(f"  Price Change: {result.stock_data['current_price'] - result.stock_data['previous_close']:.2f} "
              f"({((result.stock_data['current_price'] - result.stock_data['previous_close']) / result.stock_data['previous_close'] * 100):.2f}%)")
        print(f"  Related News: {result.news_count} articles")
        print(f"  Sentiment: {result.sentiment_summary}")
        print(f"  Average Sentiment Score: {result.average_sentiment:.3f}")
        print(f"  Recommendation: {result.recommendation}")
        print(f"  Confidence: {result.confidence_score:.2f}")
