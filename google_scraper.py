#!/usr/bin/env python3
"""
Google AI Blog Scraper Module
Specialized scraper for Google AI and DeepMind blogs
"""

import json
import logging
import re
from datetime import datetime
from typing import Dict, List, Optional
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class GoogleAIScraper:
    """Specialized scraper for Google AI blog and related content"""

    def __init__(self):
        """Initialize Google AI scraper"""
        self.base_urls = {
            'google_ai_blog': 'https://blog.google/technology/ai/',
            'deepmind': 'https://deepmind.google/discover/blog/',
            'google_research': 'https://research.google/blog/'
        }
        self.session = self._create_session()

    def _create_session(self) -> requests.Session:
        """Create requests session with appropriate headers"""
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
        return session

    def scrape_google_ai_blog(self) -> Dict:
        """Scrape the main Google AI blog"""
        url = self.base_urls['google_ai_blog']
        logger.info(f"Scraping Google AI Blog: {url}")

        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')
            articles = []

            # Multiple possible article selectors for Google's blog
            article_selectors = [
                'article',
                'div.glue-grid__col',
                'div[class*="article"]',
                'div[class*="post"]',
                'div.uni-article-card',
                'a[href*="/technology/ai/"]'
            ]

            for selector in article_selectors:
                elements = soup.select(selector)
                if elements:
                    logger.info(f"Found {len(elements)} elements with selector: {selector}")
                    for element in elements[:15]:  # Get more articles
                        article_data = self._extract_google_article(element, url)
                        if article_data and article_data not in articles:
                            articles.append(article_data)

            # Also try to find articles by looking for links
            if len(articles) < 5:
                links = soup.find_all('a', href=re.compile(r'/technology/ai/.*'))
                for link in links[:10]:
                    article_data = self._extract_from_link(link, url)
                    if article_data and article_data not in articles:
                        articles.append(article_data)

            # Remove duplicates based on title
            unique_articles = []
            seen_titles = set()
            for article in articles:
                if article['title'] not in seen_titles:
                    seen_titles.add(article['title'])
                    unique_articles.append(article)

            result = {
                'competitor': 'Google AI',
                'source': 'Google AI Blog',
                'url': url,
                'timestamp': datetime.now().isoformat(),
                'articles': unique_articles[:10],  # Limit to 10 most relevant
                'article_count': len(unique_articles)
            }

            logger.info(f"Successfully scraped {len(unique_articles)} unique articles from Google AI Blog")
            return result

        except Exception as e:
            logger.error(f"Error scraping Google AI Blog: {e}")
            return {
                'competitor': 'Google AI',
                'source': 'Google AI Blog',
                'url': url,
                'timestamp': datetime.now().isoformat(),
                'error': str(e),
                'articles': []
            }

    def scrape_deepmind(self) -> Dict:
        """Scrape DeepMind blog"""
        url = self.base_urls['deepmind']
        logger.info(f"Scraping DeepMind: {url}")

        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')
            articles = []

            # DeepMind specific selectors
            article_selectors = [
                'article',
                'div[class*="post"]',
                'div[class*="blog"]',
                'a[href*="/blog/"]'
            ]

            for selector in article_selectors:
                elements = soup.select(selector)
                for element in elements[:10]:
                    article_data = self._extract_deepmind_article(element, url)
                    if article_data:
                        articles.append(article_data)

            # Remove duplicates
            unique_articles = self._remove_duplicates(articles)

            result = {
                'competitor': 'Google AI',
                'source': 'DeepMind',
                'url': url,
                'timestamp': datetime.now().isoformat(),
                'articles': unique_articles[:10],
                'article_count': len(unique_articles)
            }

            logger.info(f"Successfully scraped {len(unique_articles)} articles from DeepMind")
            return result

        except Exception as e:
            logger.error(f"Error scraping DeepMind: {e}")
            return {
                'competitor': 'Google AI',
                'source': 'DeepMind',
                'url': url,
                'timestamp': datetime.now().isoformat(),
                'error': str(e),
                'articles': []
            }

    def _extract_google_article(self, element, base_url: str) -> Optional[Dict]:
        """Extract article data from Google AI blog element"""
        try:
            # Try multiple ways to extract title
            title = None
            title_selectors = ['h2', 'h3', 'h4', '.headline', '[class*="title"]', 'a']
            for selector in title_selectors:
                title_elem = element.select_one(selector)
                if title_elem:
                    title = title_elem.get_text(strip=True)
                    if title and len(title) > 10:  # Filter out navigation links
                        break

            if not title:
                return None

            # Extract link
            link = None
            link_elem = element.select_one('a[href]')
            if link_elem:
                link = link_elem.get('href')
                if link and not link.startswith('http'):
                    link = urljoin(base_url, link)

            # Extract date
            date = None
            date_selectors = ['time', '[datetime]', '[class*="date"]', '[class*="time"]']
            for selector in date_selectors:
                date_elem = element.select_one(selector)
                if date_elem:
                    date = date_elem.get('datetime') or date_elem.get_text(strip=True)
                    break

            # Extract content preview
            content = None
            content_selectors = ['p', '[class*="excerpt"]', '[class*="summary"]', '[class*="description"]']
            for selector in content_selectors:
                content_elem = element.select_one(selector)
                if content_elem:
                    content = content_elem.get_text(strip=True)
                    if content:
                        break

            # Extract category/tags
            category = None
            category_elem = element.select_one('[class*="category"], [class*="tag"]')
            if category_elem:
                category = category_elem.get_text(strip=True)

            return {
                'title': title,
                'link': link,
                'date': date,
                'content_preview': content[:500] if content else None,
                'category': category,
                'source': 'Google AI Blog'
            }

        except Exception as e:
            logger.debug(f"Error extracting Google article: {e}")
            return None

    def _extract_deepmind_article(self, element, base_url: str) -> Optional[Dict]:
        """Extract article data from DeepMind blog element"""
        try:
            # Similar extraction logic adapted for DeepMind's structure
            title_elem = element.select_one('h2, h3, a[href*="/blog/"]')
            title = title_elem.get_text(strip=True) if title_elem else None

            if not title or len(title) < 10:
                return None

            link_elem = element.select_one('a[href]')
            link = link_elem.get('href') if link_elem else None
            if link and not link.startswith('http'):
                link = urljoin(base_url, link)

            date_elem = element.select_one('time, [class*="date"]')
            date = date_elem.get_text(strip=True) if date_elem else None

            content_elem = element.select_one('p, [class*="summary"]')
            content = content_elem.get_text(strip=True) if content_elem else None

            return {
                'title': title,
                'link': link,
                'date': date,
                'content_preview': content[:500] if content else None,
                'source': 'DeepMind'
            }

        except Exception as e:
            logger.debug(f"Error extracting DeepMind article: {e}")
            return None

    def _extract_from_link(self, link_element, base_url: str) -> Optional[Dict]:
        """Extract article data from a link element"""
        try:
            title = link_element.get_text(strip=True)
            if not title or len(title) < 10:
                return None

            href = link_element.get('href')
            if href and not href.startswith('http'):
                href = urljoin(base_url, href)

            # Try to find parent element for more context
            parent = link_element.parent
            content = None
            date = None

            if parent:
                content_elem = parent.select_one('p')
                if content_elem:
                    content = content_elem.get_text(strip=True)

                date_elem = parent.select_one('time, [class*="date"]')
                if date_elem:
                    date = date_elem.get_text(strip=True)

            return {
                'title': title,
                'link': href,
                'date': date,
                'content_preview': content[:500] if content else None,
                'source': 'Google AI'
            }

        except Exception as e:
            logger.debug(f"Error extracting from link: {e}")
            return None

    def _remove_duplicates(self, articles: List[Dict]) -> List[Dict]:
        """Remove duplicate articles based on title"""
        seen = set()
        unique = []
        for article in articles:
            if article['title'] not in seen:
                seen.add(article['title'])
                unique.append(article)
        return unique

    def scrape_all_google_sources(self) -> List[Dict]:
        """Scrape all Google AI sources"""
        results = []

        # Scrape Google AI Blog
        google_ai_result = self.scrape_google_ai_blog()
        if google_ai_result:
            results.append(google_ai_result)

        # Scrape DeepMind
        deepmind_result = self.scrape_deepmind()
        if deepmind_result:
            results.append(deepmind_result)

        return results


def main():
    """Test the Google AI scraper"""
    logging.basicConfig(level=logging.INFO)

    print("=" * 60)
    print("Google AI Scraper Test")
    print("=" * 60)

    scraper = GoogleAIScraper()

    # Test Google AI Blog
    print("\nScraping Google AI Blog...")
    google_result = scraper.scrape_google_ai_blog()
    print(f"Found {google_result.get('article_count', 0)} articles")
    if google_result.get('articles'):
        print("\nLatest articles:")
        for article in google_result['articles'][:3]:
            print(f"  - {article['title']}")
            if article.get('date'):
                print(f"    Date: {article['date']}")
            if article.get('link'):
                print(f"    Link: {article['link']}")

    # Test DeepMind
    print("\n" + "-" * 40)
    print("Scraping DeepMind...")
    deepmind_result = scraper.scrape_deepmind()
    print(f"Found {deepmind_result.get('article_count', 0)} articles")
    if deepmind_result.get('articles'):
        print("\nLatest articles:")
        for article in deepmind_result['articles'][:3]:
            print(f"  - {article['title']}")

    print("\n" + "=" * 60)
    print("Test complete!")


if __name__ == "__main__":
    main()