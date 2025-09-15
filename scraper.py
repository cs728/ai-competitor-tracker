#!/usr/bin/env python3
"""
AI Competitor Tracker - Web Scraper
Monitors AI company websites for competitive intelligence
"""

import json
import logging
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class CompetitorScraper:
    """Web scraper for AI competitor websites"""

    def __init__(self, config_path: str = "config.json"):
        """Initialize scraper with configuration"""
        self.config = self._load_config(config_path)
        self.session = self._create_session()
        self.data_dir = Path("data/raw")
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from JSON file"""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning(f"Config file {config_path} not found. Using defaults.")
            return self._get_default_config()

    def _get_default_config(self) -> Dict:
        """Return default configuration"""
        return {
            "competitors": [
                {
                    "name": "OpenAI",
                    "url": "https://openai.com/blog",
                    "selector": "article",
                    "title_selector": "h2, h3",
                    "date_selector": "time",
                    "content_selector": "p"
                }
            ],
            "request_timeout": 30,
            "rate_limit_delay": 2,
            "user_agent": "AI-Competitor-Tracker/1.0"
        }

    def _create_session(self) -> requests.Session:
        """Create requests session with retry logic"""
        session = requests.Session()
        retry = Retry(
            total=3,
            read=3,
            connect=3,
            backoff_factor=0.3,
            status_forcelist=(500, 502, 504)
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        session.headers.update({
            'User-Agent': self.config.get('user_agent', 'AI-Competitor-Tracker/1.0')
        })
        return session

    def scrape_website(self, competitor: Dict) -> Optional[Dict]:
        """Scrape a single competitor website"""
        name = competitor.get('name')
        url = competitor.get('url')

        logger.info(f"Scraping {name}: {url}")

        try:
            response = self.session.get(
                url,
                timeout=self.config.get('request_timeout', 30)
            )
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract articles/posts
            articles = []
            article_elements = soup.select(competitor.get('selector', 'article'))

            for article in article_elements[:10]:  # Limit to 10 most recent
                article_data = self._extract_article_data(article, competitor)
                if article_data:
                    articles.append(article_data)

            result = {
                'competitor': name,
                'url': url,
                'timestamp': datetime.now().isoformat(),
                'articles': articles,
                'article_count': len(articles)
            }

            logger.info(f"Successfully scraped {len(articles)} articles from {name}")
            return result

        except requests.RequestException as e:
            logger.error(f"Error scraping {name}: {e}")
            return {
                'competitor': name,
                'url': url,
                'timestamp': datetime.now().isoformat(),
                'error': str(e),
                'articles': []
            }

    def _extract_article_data(self, article_element, competitor: Dict) -> Optional[Dict]:
        """Extract data from a single article element"""
        try:
            # Extract title
            title_elem = article_element.select_one(competitor.get('title_selector', 'h2, h3'))
            title = title_elem.get_text(strip=True) if title_elem else None

            # Extract date
            date_elem = article_element.select_one(competitor.get('date_selector', 'time'))
            date = date_elem.get('datetime', date_elem.get_text(strip=True)) if date_elem else None

            # Extract content preview
            content_elems = article_element.select(competitor.get('content_selector', 'p'))
            content = ' '.join([elem.get_text(strip=True) for elem in content_elems[:3]])

            # Extract link
            link_elem = article_element.select_one('a')
            link = link_elem.get('href') if link_elem else None
            if link and not link.startswith('http'):
                link = urljoin(competitor['url'], link)

            if title:  # Only return if we at least have a title
                return {
                    'title': title,
                    'date': date,
                    'content_preview': content[:500] if content else None,
                    'link': link
                }
        except Exception as e:
            logger.debug(f"Error extracting article data: {e}")

        return None

    def scrape_all(self) -> List[Dict]:
        """Scrape all configured competitor websites"""
        results = []

        for competitor in self.config.get('competitors', []):
            result = self.scrape_website(competitor)
            if result:
                results.append(result)
                # Save individual result
                self._save_result(result)
                # Rate limiting
                time.sleep(self.config.get('rate_limit_delay', 2))

        return results

    def _save_result(self, result: Dict):
        """Save scraping result to JSON file"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        competitor_name = result['competitor'].replace(' ', '_')
        filename = self.data_dir / f"{competitor_name}_{timestamp}.json"

        with open(filename, 'w') as f:
            json.dump(result, f, indent=2, default=str)

        logger.info(f"Saved result to {filename}")

    def get_latest_data(self, competitor_name: str = None) -> List[Dict]:
        """Get the latest scraped data"""
        pattern = f"{competitor_name}*" if competitor_name else "*"
        files = sorted(self.data_dir.glob(f"{pattern}.json"), key=lambda x: x.stat().st_mtime, reverse=True)

        data = []
        for file in files[:10]:  # Get last 10 files
            with open(file, 'r') as f:
                data.append(json.load(f))

        return data


def main():
    """Main execution function"""
    print("=" * 60)
    print("AI Competitor Tracker - Web Scraper")
    print("=" * 60)

    scraper = CompetitorScraper()

    print("\nStarting competitor website scraping...")
    results = scraper.scrape_all()

    print(f"\nScraped {len(results)} competitor websites")

    for result in results:
        print(f"\n{result['competitor']}:")
        print(f"  - Articles found: {result.get('article_count', 0)}")
        if 'error' in result:
            print(f"  - Error: {result['error']}")
        elif result['articles']:
            print(f"  - Latest: {result['articles'][0].get('title', 'No title')}")

    print("\n" + "=" * 60)
    print("Scraping complete! Check data/raw/ for detailed results")
    print("=" * 60)


if __name__ == "__main__":
    main()