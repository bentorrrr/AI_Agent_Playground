# Setup and Usage Guide

## Quick Start Guide

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/bentorrrr/AI_Agent_Playground.git
cd AI_Agent_Playground

# Install dependencies
pip install -r requirements.txt
```

### 2. Basic Usage

#### Run the complete scraper and analyzer:
```bash
python main.py
```

This will:
- Scrape tech news from multiple sources
- Fetch current stock data for Magnificent 7 stocks
- Perform sentiment analysis on news
- Generate investment recommendations
- Save all data to the `data/` directory

#### View usage examples:
```bash
python examples/usage_examples.py
```

### 3. Understanding the Output

The tool creates three JSON files in the `data/` directory:

1. **news_articles.json** - All scraped news articles with:
   - Title, URL, source
   - Publication date
   - Related stock tickers (auto-detected)
   - Sentiment scores

2. **stock_data.json** - Current stock information:
   - Current price and previous close
   - Day high/low and volume
   - Market cap and P/E ratio
   - 52-week high/low

3. **analysis_results.json** - Combined analysis:
   - Stock performance metrics
   - Related news articles
   - Sentiment summary
   - Investment recommendations
   - Confidence scores

## Advanced Usage

### Custom Stock Selection

To analyze specific stocks, modify `config.py`:

```python
# Focus on specific stocks
selected_stocks = ['NVDA', 'TSLA', 'GOOGL']
```

### Custom News Sources

Add your own RSS feeds in `config.py`:

```python
NEWS_SOURCES = {
    "my_source": "https://example.com/rss",
    # ... other sources
}
```

### Adjusting Scraping Parameters

In `config.py`, modify:

```python
SCRAPER_SETTINGS = {
    "max_articles_per_source": 100,  # Increase for more articles
    "rate_limit_delay": 5,           # Increase to be more polite
    "request_timeout": 60,           # Increase for slow connections
}
```

## Component Testing

### Test Individual Components

```python
# Test stock scraper
from src.scrapers.stock_scraper import StockScraper
scraper = StockScraper()
stock = scraper.fetch_stock_data('NVDA')
print(f"NVDA Price: ${stock.current_price}")

# Test news scraper
from src.scrapers.news_scraper import NewsScraper
scraper = NewsScraper()
articles = scraper.scrape_all_sources()
print(f"Found {len(articles)} articles")

# Test sentiment analyzer
from src.analyzer import TechStockAnalyzer
analyzer = TechStockAnalyzer()
sentiment = analyzer.analyze_sentiment("Great news for tech!")
print(f"Sentiment: {sentiment}")
```

## Troubleshooting

### Common Issues

1. **Network Errors**
   - Check your internet connection
   - Some RSS feeds may be temporarily unavailable
   - Increase `request_timeout` in config

2. **Rate Limiting**
   - Increase `rate_limit_delay` in config
   - Some sources may block frequent requests

3. **Missing Dependencies**
   ```bash
   pip install -r requirements.txt --upgrade
   ```

4. **Permission Errors**
   - Ensure the `data/` directory is writable
   - Run with appropriate permissions

### Getting Help

- Check the README.md for detailed documentation
- Review examples/usage_examples.py for code samples
- Open an issue on GitHub for bugs or questions

## Data Privacy and Ethics

- This tool scrapes publicly available data
- Respect robots.txt and rate limits
- Use scraped data responsibly
- Do not use for automated trading without proper risk management
- Always verify information from primary sources

## Performance Tips

1. **Reduce Article Count**: Lower `max_articles_per_source` for faster execution
2. **Selective Sources**: Comment out less relevant sources in `config.py`
3. **Parallel Processing**: Future versions will support concurrent scraping
4. **Caching**: Data is automatically cached in JSON files to avoid re-fetching

## Next Steps

1. **Collect Historical Data**: Run the scraper daily to build a dataset
2. **Analyze Trends**: Look for patterns in sentiment vs. stock performance
3. **ML Model Development**: Use collected data to train prediction models
4. **Automation**: Set up cron jobs or scheduled tasks for regular scraping

## Example Workflow

```bash
# Step 1: Initial data collection
python main.py

# Step 2: View the data
cat data/analysis_results.json | python -m json.tool

# Step 3: Run examples to understand components
python examples/usage_examples.py

# Step 4: Customize config.py for your needs

# Step 5: Set up daily automation (cron example)
# Add to crontab: 0 18 * * 1-5 cd /path/to/project && python main.py
```

## Future Enhancements

The project roadmap includes:

- [ ] Web dashboard for visualization
- [ ] Historical data tracking and charting
- [ ] Machine learning model for predictions
- [ ] Email/SMS alerts for significant events
- [ ] Support for more stock exchanges
- [ ] Real-time streaming data
- [ ] Portfolio optimization recommendations
- [ ] Risk assessment metrics

---

**Note**: Always do your own research and consult financial advisors before making investment decisions. This tool is for educational purposes only.
