"""
RSS Feed Parser Module
Fetches and parses RPP RSS feed
"""

import requests, feedparser
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict

def save_articles_to_json(articles: List[Dict], output_path: str = "data/rss_feed.json"):
    """
    Save articles to JSON file
    
    Args:
        articles: List of article dictionaries
        output_path: Path to save JSON file
    """
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)
    
    print(f"Articles saved to: {output_path}")


def load_articles_from_json(input_path: str = "data/rss_feed.json") -> List[Dict]:
    """
    Load articles from JSON file
    
    Args:
        input_path: Path to JSON file
        
    Returns:
        List of article dictionaries
    """
    with open(input_path, 'r', encoding='utf-8') as f:
        articles = json.load(f)
    
    print(f"Loaded {len(articles)} articles from: {input_path}")
    return articles


if __name__ == "__main__":
    # Test the module
    articles = fetch_rpp_news()
    save_articles_to_json(articles)
    print("\nSample article:")
    print(json.dumps(articles[0], indent=2, ensure_ascii=False))

