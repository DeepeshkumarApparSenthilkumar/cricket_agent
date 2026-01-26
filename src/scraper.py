import logging
from duckduckgo_search import DDGS
from datetime import datetime
from src.utils import setup_logging, save_data

logger = setup_logging()

import requests
import os
from bs4 import BeautifulSoup

def fetch_rss_news():
    logger.info("Fetching news from RSS feeds...")
    feeds = [
        "https://feeds.bbci.co.uk/sport/cricket/rss.xml",
        "https://www.espncricinfo.com/rss/content/story/feeds/0.xml"
    ]
    
    results = {
        "headlines": [],
        "match_results": [],
        "injuries": []
    }
    
    for url in feeds:
        try:
            response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
            if response.status_code == 200:
                # Use xml parser
                soup = BeautifulSoup(response.content, 'xml')
                items = soup.find_all('item')
                
                for item in items[:5]: # Top 5 from each
                    title = item.title.text.strip()
                    description = item.description.text.strip() if item.description else ""
                    link = item.link.text.strip() if item.link else ""
                    
                    # Clean up description (sometimes contains HTML)
                    if '<' in description:
                        description = BeautifulSoup(description, 'html.parser').get_text()
                    
                    news_item = {
                        'title': title,
                        'summary': description,
                        'href': link,
                        'source': 'BBC' if 'bbc' in url else 'Cricinfo'
                    }
                    
                    # Simple categorization
                    lower_title = title.lower()
                    if 'win' in lower_title or 'beat' in lower_title or 'score' in lower_title:
                        results['match_results'].append(news_item)
                    elif 'injury' in lower_title or 'ruled out' in lower_title or 'squad' in lower_title:
                        results['injuries'].append(news_item)
                    else:
                        results['headlines'].append(news_item)
                        
            logger.info(f"Fetched from {url}")
        except Exception as e:
            logger.error(f"Error fetching RSS {url}: {e}")
            
    return results

def fetch_cricket_news(time_window=None):
    """
    Fetches cricket news using DuckDuckGo Search.
    time_window: 'd' for day, 'w' for week, 'm' for month, None for no limit.
    """
    logger.info(f"Starting news scrape for time window: {time_window}")
    
    results = {
        "timestamp": datetime.now().isoformat(),
        "headlines": [],
        "match_results": [],
        "injuries": []
    }

    # Try DDGS first
    try:
        with DDGS() as ddgs:
            # 1. Global Headlines
            logger.info("Fetching Global Headlines...")
            headlines_query = "cricket news global headlines"
            headlines = list(ddgs.text(headlines_query, region='in-en', safesearch='off', timelimit=time_window, max_results=10))
            logger.info(f"Raw headlines count: {len(headlines)}")
            results['headlines'] = headlines

            # 2. Match Results
            logger.info("Fetching Match Results...")
            matches_query = "latest cricket match results scores"
            matches = list(ddgs.text(matches_query, region='in-en', safesearch='off', timelimit=time_window, max_results=10))
            logger.info(f"Raw matches count: {len(matches)}")
            results['match_results'] = matches

            # 3. Injuries
            logger.info("Fetching Injury Updates...")
            injuries_query = "cricket player injuries updates"
            injuries = list(ddgs.text(injuries_query, region='in-en', safesearch='off', timelimit=time_window, max_results=5))
            logger.info(f"Raw injuries count: {len(injuries)}")
            results['injuries'] = injuries
            
    except Exception as e:
        logger.error(f"DDGS failed: {e}")

    # Fallback if empty
    if not results['headlines'] and not results['match_results']:
        logger.info("DDGS returned empty. Switching to fallback...")
        fallback_data = fetch_rss_news()
        results['headlines'].extend(fallback_data['headlines'])
        results['match_results'].extend(fallback_data['match_results'])
        results['injuries'].extend(fallback_data['injuries'])
        # BBC scrape is limited, but better than nothing

    logger.info(f"Scraping complete. Found {len(results['headlines'])} headlines, {len(results['match_results'])} matches, {len(results['injuries'])} injury updates.")
    
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
