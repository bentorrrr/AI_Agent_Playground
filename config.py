# Configuration file for tech stock scraper

# Magnificent 7 tech stocks
TECH_STOCKS = {
    "AAPL": {
        "name": "Apple Inc.",
        "sector": "Technology",
        "keywords": ["apple", "iphone", "ipad", "mac", "tim cook", "ios", "macos"]
    },
    "MSFT": {
        "name": "Microsoft Corporation",
        "sector": "Technology",
        "keywords": ["microsoft", "windows", "azure", "office", "satya nadella", "xbox", "teams"]
    },
    "AMZN": {
        "name": "Amazon.com Inc.",
        "sector": "Technology/E-commerce",
        "keywords": ["amazon", "aws", "prime", "jeff bezos", "andy jassy", "alexa"]
    },
    "GOOGL": {
        "name": "Alphabet Inc. (Google)",
        "sector": "Technology",
        "keywords": ["google", "alphabet", "android", "youtube", "search", "sundar pichai", "gemini", "bard"]
    },
    "META": {
        "name": "Meta Platforms Inc.",
        "sector": "Technology/Social Media",
        "keywords": ["meta", "facebook", "instagram", "whatsapp", "mark zuckerberg", "metaverse", "oculus"]
    },
    "NVDA": {
        "name": "NVIDIA Corporation",
        "sector": "Technology/Semiconductors",
        "keywords": ["nvidia", "gpu", "ai chip", "jensen huang", "cuda", "geforce", "artificial intelligence"]
    },
    "TSLA": {
        "name": "Tesla Inc.",
        "sector": "Automotive/Technology",
        "keywords": ["tesla", "electric vehicle", "elon musk", "ev", "autopilot", "model s", "model 3", "model x", "model y"]
    }
}

# News sources (RSS feeds)
NEWS_SOURCES = {
    "techcrunch": "https://techcrunch.com/feed/",
    "reuters_tech": "https://www.reuters.com/technology/",
    "theverge": "https://www.theverge.com/rss/index.xml",
    "hackernews": "https://news.ycombinator.com/rss",
    "cnbc_tech": "https://www.cnbc.com/id/19854910/device/rss/rss.html"
}

# Scraper settings
SCRAPER_SETTINGS = {
    "max_articles_per_source": 50,
    "request_timeout": 30,
    "rate_limit_delay": 2,  # seconds between requests
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

# Data storage settings
DATA_SETTINGS = {
    "data_dir": "data",
    "news_file": "news_articles.json",
    "stock_file": "stock_data.json",
    "analysis_file": "analysis_results.json"
}
