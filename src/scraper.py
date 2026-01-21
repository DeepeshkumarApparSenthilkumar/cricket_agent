import logging
from duckduckgo_search import DDGS
from datetime import datetime
from src.utils import setup_logging, save_data

logger = setup_logging()

import requests
from bs4 import BeautifulSoup

def fetch_from_bbc():
    logger.info("Attempting fallback scrape from BBC Cricket...")
    url = "https://www.bbc.com/sport/cricket"
    results = {
        "headlines": [],
        "match_results": [],
        "injuries": []
    }
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract headlines (BBC structure changes, this is a generic attempt)
            # Looking for main promo or top stories
            articles = soup.find_all('div', {'type': 'article'})
            for art in articles[:5]:
                text = art.get_text(strip=True)
                link = art.find('a')['href'] if art.find('a') else ''
                if link and not link.startswith('http'):
                    link = f"https://www.bbc.com{link}"
                results['headlines'].append({'title': text, 'href': link})
            
            logger.info(f"BBC Scrape: Found {len(results['headlines'])} headlines.")
        else:
            logger.error(f"BBC Scrape failed with status: {response.status_code}")
    except Exception as e:
        logger.error(f"BBC Scrape error: {e}")
    
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
        fallback_data = fetch_from_bbc()
        results['headlines'].extend(fallback_data['headlines'])
        # BBC scrape is limited, but better than nothing

    logger.info(f"Scraping complete. Found {len(results['headlines'])} headlines, {len(results['match_results'])} matches, {len(results['injuries'])} injury updates.")
    
    # Save to cache
    save_data(results)
    return results

if __name__ == "__main__":
    # Test the scraper
    fetch_cricket_news(time_window=None)
