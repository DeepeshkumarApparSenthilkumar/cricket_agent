import logging
from duckduckgo_search import DDGS
from datetime import datetime
from src.utils import setup_logging, save_data

logger = setup_logging()

import requests
import os
from bs4 import BeautifulSoup

def fetch_cricket_news(time_window=None):
    """
    Fetches cricket news using DuckDuckGo Search with strict site filtering.
    """
    logger.info(f"Starting news scrape for time window: {time_window}")
    
    results = {
        "timestamp": datetime.now().isoformat(),
        "headlines": [],
        "match_results": [],
        "injuries": []
    }

    try:
        with DDGS() as ddgs:
            # 1. Match Results - Strictly from ESPNcricinfo/Cricbuzz
            logger.info("Fetching Match Results...")
            # Query for recent match reports
            matches_query = "site:espncricinfo.com/series/ match report result"
            matches = list(ddgs.text(matches_query, region='wt-wt', safesearch='off', max_results=5))
            
            for m in matches:
                results['match_results'].append({
                    'title': m['title'],
                    'summary': m['body'],
                    'href': m['href']
                })

            # 2. Global Headlines - News section
            logger.info("Fetching Global Headlines...")
            headlines_query = "site:espncricinfo.com/story/ OR site:cricbuzz.com/cricket-news/ news"
            headlines = list(ddgs.text(headlines_query, region='wt-wt', safesearch='off', max_results=5))
            
            for h in headlines:
                results['headlines'].append({
                    'title': h['title'],
                    'summary': h['body'],
                    'href': h['href']
                })

            # 3. Injuries
            logger.info("Fetching Injury Updates...")
            injuries_query = "site:espncricinfo.com injury update ruled out"
            injuries = list(ddgs.text(injuries_query, region='wt-wt', safesearch='off', max_results=3))
            
            for i in injuries:
                results['injuries'].append({
                    'title': i['title'],
                    'summary': i['body'],
                    'href': i['href']
                })
            
    except Exception as e:
        logger.error(f"DDGS failed: {e}")

    logger.info(f"Scraping complete. Found {len(results['headlines'])} headlines, {len(results['match_results'])} matches.")
    
    # Save to cache
    save_data(results)
    
    # Verify save
    if not os.path.exists("data/news_cache.json"):
        logger.error("Failed to save data/news_cache.json")
        import sys
        sys.exit(1)
        
    return results

if __name__ == "__main__":
    # Test the scraper
    fetch_cricket_news(time_window=None)
