"""
Data models for storing scraped information about news and stocks.
"""
from datetime import datetime
from typing import List, Optional, Dict, Any
from dataclasses import dataclass, asdict


@dataclass
class NewsArticle:
    """Model for a news article."""
    title: str
    url: str
    source: str
    published_date: str
    summary: Optional[str] = None
    content: Optional[str] = None
    related_stocks: Optional[List[str]] = None
    sentiment_score: Optional[float] = None
    keywords: Optional[List[str]] = None
    scraped_at: str = None
    
    def __post_init__(self):
        if self.scraped_at is None:
            self.scraped_at = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class StockData:
    """Model for stock data."""
    ticker: str
    company_name: str
    current_price: float
    previous_close: float
    open_price: float
    day_high: float
    day_low: float
    volume: int
    market_cap: Optional[float] = None
    pe_ratio: Optional[float] = None
    dividend_yield: Optional[float] = None
    fifty_two_week_high: Optional[float] = None
    fifty_two_week_low: Optional[float] = None
    timestamp: str = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)
    
    @property
    def price_change(self) -> float:
        """Calculate price change from previous close."""
        return self.current_price - self.previous_close
    
    @property
    def price_change_percent(self) -> float:
        """Calculate percentage price change from previous close."""
        if self.previous_close == 0:
            return 0.0
        return (self.price_change / self.previous_close) * 100


@dataclass
class AnalysisResult:
    """Model for analysis results combining news and stock data."""
    ticker: str
    company_name: str
    analysis_date: str
    stock_data: Dict[str, Any]
    related_news: List[Dict[str, Any]]
    sentiment_summary: Optional[str] = None
    average_sentiment: Optional[float] = None
    news_count: int = 0
    recommendation: Optional[str] = None
    confidence_score: Optional[float] = None
    
    def __post_init__(self):
        if self.analysis_date is None:
            self.analysis_date = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)
