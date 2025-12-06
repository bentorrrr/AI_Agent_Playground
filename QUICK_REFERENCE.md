# Quick Reference Guide

## 🚀 Quick Start

```bash
# Install
pip install -r requirements.txt

# Run Demo (no internet needed)
python quickstart.py

# Run Full Scraper (requires internet)
python main.py

# View Examples
python examples/usage_examples.py
```

## 📁 Project Files

| File | Purpose |
|------|---------|
| `main.py` | Main application - scrapes news and stocks |
| `quickstart.py` | Demo with mock data - no internet needed |
| `config.py` | Configuration - stocks, sources, settings |
| `setup.py` | Package installation |
| `requirements.txt` | Python dependencies |

## 📚 Documentation

| Document | Description |
|----------|-------------|
| `README.md` | Complete user guide |
| `SETUP.md` | Installation & configuration |
| `ML_IMPLEMENTATION_PLAN.md` | ML roadmap (6 months) |
| `ROADMAP.md` | Development plan |
| `PROJECT_SUMMARY.md` | Complete overview |

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────┐
│                   CONFIG.PY                      │
│  (Stocks, Sources, Settings)                     │
└──────────────────────────────────────────────────┘
                      │
         ┌────────────┴────────────┐
         ▼                         ▼
┌─────────────────┐       ┌─────────────────┐
│  NEWS SCRAPER   │       │  STOCK SCRAPER  │
│  (RSS Feeds)    │       │  (yfinance)     │
└────────┬────────┘       └────────┬────────┘
         │                         │
         └────────────┬────────────┘
                      ▼
         ┌────────────────────────┐
         │  SENTIMENT ANALYZER    │
         │  (TextBlob NLP)        │
         └────────────┬───────────┘
                      ▼
         ┌────────────────────────┐
         │  RECOMMENDATION        │
         │  ENGINE                │
         └────────────┬───────────┘
                      ▼
         ┌────────────────────────┐
         │  DATA STORAGE          │
         │  (JSON Files)          │
         └────────────────────────┘
```

## 🎯 Key Components

### News Scraper (`src/scrapers/news_scraper.py`)
- Fetches RSS feeds
- Detects related stocks
- Extracts article metadata

### Stock Scraper (`src/scrapers/stock_scraper.py`)
- Gets real-time prices
- Fetches market metrics
- Tracks 7 tech stocks

### Analyzer (`src/analyzer.py`)
- Sentiment analysis (TextBlob)
- Combines news + stock data
- Generates recommendations

### Data Models (`src/models/data_models.py`)
- `NewsArticle`: News metadata
- `StockData`: Stock metrics
- `AnalysisResult`: Combined analysis

## 📊 Tracked Stocks

| Ticker | Company |
|--------|---------|
| AAPL | Apple Inc. |
| MSFT | Microsoft Corporation |
| AMZN | Amazon.com Inc. |
| GOOGL | Alphabet Inc. (Google) |
| META | Meta Platforms Inc. |
| NVDA | NVIDIA Corporation |
| TSLA | Tesla Inc. |

## 🔧 Configuration Options

Edit `config.py` to customize:

```python
# Add more stocks
TECH_STOCKS = {
    "NEW": {
        "name": "Company Name",
        "keywords": ["keyword1", "keyword2"]
    }
}

# Add news sources
NEWS_SOURCES = {
    "source_name": "https://example.com/rss"
}

# Adjust scraping
SCRAPER_SETTINGS = {
    "max_articles_per_source": 50,
    "rate_limit_delay": 2,
}
```

## 📈 Output Files

Located in `data/` directory:

- `news_articles.json` - All scraped news
- `stock_data.json` - Current stock data
- `analysis_results.json` - Combined analysis

## 🎨 Example Output

```
NVDA - NVIDIA Corporation
────────────────────────────────────────
Price: $495.50 (+$13.20, +2.74%) 📈
Volume: 45,234,567
Market Cap: $1,220.45B

News Analysis:
  Articles Found: 15
  Sentiment: Positive
  Average Score: 0.342

Recommendation: BUY - Strong positive sentiment
Confidence: 0.78

Recent Headlines:
  📈 NVIDIA announces breakthrough in AI chips
  📈 AI demand drives record earnings
  ➡️ NVIDIA expands partnerships
```

## 🛠️ Common Commands

```bash
# Install in development mode
pip install -e .

# View data
cat data/analysis_results.json | python -m json.tool

# Check Python version
python --version  # Requires 3.8+

# List dependencies
pip list
```

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| Import errors | Run `pip install -r requirements.txt` |
| Network errors | Check internet connection |
| Rate limiting | Increase delay in config.py |
| No data | Run `python main.py` first |

## 📝 API Usage

```python
# Scrape news
from src.scrapers import NewsScraper
scraper = NewsScraper()
articles = scraper.scrape_all_sources()

# Get stock data
from src.scrapers import StockScraper
scraper = StockScraper()
stock = scraper.fetch_stock_data('NVDA')

# Analyze sentiment
from src.analyzer import TechStockAnalyzer
analyzer = TechStockAnalyzer()
sentiment = analyzer.analyze_sentiment("Great news!")
```

## ⚠️ Important Notes

1. **Not Financial Advice**: Educational tool only
2. **Internet Required**: For live data (demo works offline)
3. **Rate Limits**: Respect source policies
4. **Data Accuracy**: Verify from primary sources
5. **Risk Warning**: Investing carries risk

## 🚀 Next Steps

1. ✅ Run `python quickstart.py` to see demo
2. ✅ Install dependencies
3. ✅ Run `python main.py` with internet
4. ✅ Read `README.md` for details
5. ✅ Check `ML_IMPLEMENTATION_PLAN.md` for ML roadmap

## 📞 Support

- Documentation: See `README.md` and `SETUP.md`
- Examples: Run `python examples/usage_examples.py`
- Issues: Open on GitHub

---

**Version**: 1.0
**Status**: Ready for Testing
**Last Updated**: December 2024
