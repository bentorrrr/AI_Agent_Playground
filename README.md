# Tech Stock News & Analysis Scraper

A Python-based web scraper and analyzer for gathering tech news and stock data related to the "Magnificent 7" technology companies. This tool combines real-time stock data with news sentiment analysis to provide insights into market trends and potential investment opportunities.

## 🎯 Features

- **News Scraping**: Automatically scrapes tech news from multiple RSS feeds
- **Stock Data**: Fetches real-time stock prices and metrics using yfinance
- **Sentiment Analysis**: Analyzes news sentiment using NLP (TextBlob)
- **Stock Analysis**: Combines news sentiment with stock data for insights
- **Automated Recommendations**: Provides basic investment recommendations (placeholder for future ML model)
- **Data Persistence**: Stores data in JSON format for historical tracking

## 📊 Supported Stocks (Magnificent 7)

- **AAPL** - Apple Inc.
- **MSFT** - Microsoft Corporation
- **AMZN** - Amazon.com Inc.
- **GOOGL** - Alphabet Inc. (Google)
- **META** - Meta Platforms Inc.
- **NVDA** - NVIDIA Corporation
- **TSLA** - Tesla Inc.

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/bentorrrr/AI_Agent_Playground.git
cd AI_Agent_Playground
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Basic Usage

Run the main scraper and analyzer:
```bash
python main.py
```

This will:
1. Scrape news articles from configured sources
2. Fetch current stock data for all Magnificent 7 stocks
3. Analyze sentiment and generate recommendations
4. Save all data to the `data/` directory

### Running Examples

To see individual component examples:
```bash
python examples/usage_examples.py
```

## 📁 Project Structure

```
AI_Agent_Playground/
├── main.py                 # Main application entry point
├── config.py              # Configuration (stocks, sources, settings)
├── requirements.txt       # Python dependencies
├── data/                  # Data storage directory
│   ├── news_articles.json
│   ├── stock_data.json
│   └── analysis_results.json
├── src/
│   ├── models/
│   │   ├── __init__.py
│   │   └── data_models.py # Data models (NewsArticle, StockData, etc.)
│   ├── scrapers/
│   │   ├── __init__.py
│   │   ├── news_scraper.py   # News scraping functionality
│   │   └── stock_scraper.py  # Stock data fetching
│   ├── utils/
│   │   ├── __init__.py
│   │   └── helpers.py     # Utility functions
│   └── analyzer.py        # Sentiment analysis and recommendations
└── examples/
    └── usage_examples.py  # Example usage scripts
```

## 🔧 Configuration

Edit `config.py` to customize:

- **TECH_STOCKS**: Add or modify stock tickers and keywords
- **NEWS_SOURCES**: Add or modify RSS feed sources
- **SCRAPER_SETTINGS**: Adjust scraping parameters (rate limits, timeouts)
- **DATA_SETTINGS**: Change data storage locations

## 📈 Data Models

### NewsArticle
- title, url, source
- published_date, summary
- related_stocks (detected automatically)
- sentiment_score (calculated)

### StockData
- ticker, company_name
- current_price, previous_close
- volume, market_cap
- day_high, day_low
- 52-week high/low

### AnalysisResult
- Stock data snapshot
- Related news articles
- Sentiment summary
- Investment recommendation
- Confidence score

## 🤖 Future ML Implementation Plan

The current version uses a simple rule-based system for recommendations. Future versions will include:

1. **Data Collection Phase** (Current)
   - Gather historical news and stock data
   - Build labeled dataset

2. **Feature Engineering**
   - Technical indicators (RSI, MACD, Moving averages)
   - Sentiment features (polarity, subjectivity)
   - Volume and price patterns
   - News frequency and source credibility

3. **Model Training**
   - Time series forecasting (LSTM/Transformer)
   - Classification models (buy/sell/hold)
   - Ensemble methods
   - Backtesting framework

4. **Production Deployment**
   - Real-time predictions
   - Model monitoring and retraining
   - Risk management integration

## 📊 Example Output

```
NVDA - NVIDIA Corporation
────────────────────────────────────────
Price: $495.50 (+$12.30, +2.55%)
Volume: 45,234,567
Market Cap: $1,220.45B

News Analysis:
  Articles Found: 15
  Sentiment: Positive - News sentiment is generally favorable
  Average Score: 0.342 (range: -1 to +1)

Recommendation: BUY - Strong positive sentiment and upward price momentum
Confidence: 0.78

Recent Headlines:
  📈 NVIDIA announces breakthrough in AI chip technology
  📈 AI demand drives NVIDIA's record quarterly earnings
  ➡️ NVIDIA expands data center partnerships
```

## ⚠️ Disclaimer

**IMPORTANT**: This tool is for educational and research purposes only. The recommendations provided should NOT be used as actual investment advice. Always:

- Do your own research
- Consult with financial advisors
- Consider your risk tolerance
- Never invest more than you can afford to lose

The accuracy of news sources, stock data, and sentiment analysis cannot be guaranteed. Past performance does not indicate future results.

## 🛠️ Development

### Adding New News Sources

1. Find an RSS feed URL
2. Add to `NEWS_SOURCES` in `config.py`
3. Test with the news scraper

### Adding New Stocks

1. Add ticker to `TECH_STOCKS` in `config.py`
2. Include company name and relevant keywords
3. Run the scraper to verify data collection

### Extending Analysis

1. Modify `src/analyzer.py` to add new analysis methods
2. Update `AnalysisResult` model if needed
3. Adjust recommendation logic in `_generate_recommendation()`

## 📝 License

MIT License - feel free to use and modify for your own purposes.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

**Note**: This project is actively being developed. Star ⭐ the repository to stay updated with new features!