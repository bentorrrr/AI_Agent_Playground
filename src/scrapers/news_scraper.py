"""
News scraper for tech companies using RSS feeds and web scraping.
"""
import feedparser
from bs4 import BeautifulSoup
from typing import List, Dict, Any
from datetime import datetime
import time
import sys
import os

# Add parent directory to path for imports
# NOTE: This is a temporary solution. For proper usage, install the package:
# pip install -e .
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.models.data_models import NewsArticle
from src.utils.helpers import rate_limit, clean_text
from config import TECH_STOCKS, NEWS_SOURCES, SCRAPER_SETTINGS


class NewsScraper:
    """Scraper for tech news from various sources."""
    
    def __init__(self):
        self.sources = NEWS_SOURCES
        self.tech_stocks = TECH_STOCKS
        self.request_timeout = SCRAPER_SETTINGS['request_timeout']
        self.user_agent = SCRAPER_SETTINGS['user_agent']
        self.max_articles = SCRAPER_SETTINGS['max_articles_per_source']
        
    @rate_limit(delay=SCRAPER_SETTINGS['rate_limit_delay'])
    def _fetch_rss_feed(self, url: str) -> List[Dict[str, Any]]:
        """
        Fetch and parse an RSS feed.
        
        Args:
            url: RSS feed URL
            
        Returns:
            List of parsed feed entries
        """
        try:
            print(f"Fetching RSS feed: {url}")
            feed = feedparser.parse(url)
            return feed.entries[:self.max_articles]
        except Exception as e:
            print(f"Error fetching RSS feed {url}: {e}")
            return []
    
    def _find_related_stocks(self, text: str) -> List[str]:
        """
        Find related stock tickers mentioned in text.
        
        Args:
            text: Text to search
            
        Returns:
            List of related stock tickers
        """
        if not text:
            return []
        
        text_lower = text.lower()
        related_stocks = []
        
        for ticker, info in self.tech_stocks.items():
            # Check if company name or keywords are mentioned
            if info['name'].lower() in text_lower:
                related_stocks.append(ticker)
                continue
            
            for keyword in info.get('keywords', []):
                if keyword.lower() in text_lower:
                    related_stocks.append(ticker)
                    break
        
        return list(set(related_stocks))  # Remove duplicates
    
    def _parse_rss_entry(self, entry: Dict[str, Any], source_name: str) -> NewsArticle:
        """
        Parse an RSS feed entry into a NewsArticle object.
        
        Args:
            entry: Feed entry dictionary
            source_name: Name of the news source
            
        Returns:
            NewsArticle object
        """
        # Extract title
        title = clean_text(entry.get('title', ''))
        
        # Extract URL
        url = entry.get('link', '')
        
        # Extract published date
        published_date = entry.get('published', '')
        if not published_date and 'published_parsed' in entry:
            try:
                published_date = datetime(*entry.published_parsed[:6]).isoformat()
            except:
                published_date = datetime.now().isoformat()
        
        # Extract summary/description
        summary = clean_text(entry.get('summary', entry.get('description', '')))
        
        # Find related stocks
        combined_text = f"{title} {summary}"
        related_stocks = self._find_related_stocks(combined_text)
        
        # Extract keywords (if available)
        keywords = []
        if 'tags' in entry:
            keywords = [tag.get('term', '') for tag in entry.get('tags', [])]
        
        return NewsArticle(
            title=title,
            url=url,
            source=source_name,
            published_date=published_date,
            summary=summary,
            related_stocks=related_stocks,
            keywords=keywords
        )
    
    def scrape_all_sources(self) -> List[NewsArticle]:
        """
        Scrape news from all configured sources.
        
        Returns:
            List of NewsArticle objects
        """
        all_articles = []
        
        for source_name, source_url in self.sources.items():
            print(f"\nScraping {source_name}...")
            
            try:
                entries = self._fetch_rss_feed(source_url)
                
                for entry in entries:
                    try:
                        article = self._parse_rss_entry(entry, source_name)
                        all_articles.append(article)
                    except Exception as e:
                        print(f"Error parsing entry: {e}")
                        continue
                
                print(f"Found {len(entries)} articles from {source_name}")
                
            except Exception as e:
                print(f"Error scraping {source_name}: {e}")
                continue
        
        print(f"\nTotal articles scraped: {len(all_articles)}")
        return all_articles
    
    def filter_by_stocks(self, articles: List[NewsArticle], 
                        tickers: List[str] = None) -> List[NewsArticle]:
        """
        Filter articles by specific stock tickers.
        
        Args:
            articles: List of NewsArticle objects
            tickers: List of stock tickers to filter by (None = all)
            
        Returns:
            Filtered list of NewsArticle objects
        """
        if not tickers:
            return articles
        
        filtered = []
        for article in articles:
            if article.related_stocks:
                if any(ticker in article.related_stocks for ticker in tickers):
                    filtered.append(article)
        
        return filtered


if __name__ == "__main__":
    # Example usage
    scraper = NewsScraper()
    articles = scraper.scrape_all_sources()
    
    print(f"\n--- Sample Articles ---")
    for i, article in enumerate(articles[:5], 1):
        print(f"\n{i}. {article.title}")
        print(f"   Source: {article.source}")
        print(f"   Related stocks: {article.related_stocks}")
        print(f"   URL: {article.url}")
