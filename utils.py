#!/usr/bin/env python3
"""
Utility functions for AI Competitor Tracker
"""

import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse

logger = logging.getLogger(__name__)


def ensure_directories():
    """Ensure all required directories exist"""
    directories = [
        'data',
        'data/raw',
        'reports',
        'logs',
        'tests'
    ]

    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)

    logger.info("All required directories created/verified")


def clean_old_data(days: int = 30, data_dir: str = "data/raw"):
    """Clean data files older than specified days"""
    data_path = Path(data_dir)
    cutoff_date = datetime.now() - timedelta(days=days)

    deleted_count = 0
    for file in data_path.glob("*.json"):
        file_time = datetime.fromtimestamp(file.stat().st_mtime)
        if file_time < cutoff_date:
            file.unlink()
            deleted_count += 1

    logger.info(f"Cleaned {deleted_count} old data files")
    return deleted_count


def validate_url(url: str) -> bool:
    """Validate if a string is a valid URL"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False


def load_json_file(filepath: str) -> Optional[Dict]:
    """Safely load JSON file"""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading JSON file {filepath}: {e}")
        return None


def save_json_file(data: Dict, filepath: str) -> bool:
    """Safely save data to JSON file"""
    try:
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        return True
    except Exception as e:
        logger.error(f"Error saving JSON file {filepath}: {e}")
        return False


def extract_domain(url: str) -> str:
    """Extract domain from URL"""
    try:
        parsed = urlparse(url)
        return parsed.netloc.replace('www.', '')
    except:
        return ""


def format_date(date_str: str) -> str:
    """Format date string to consistent format"""
    try:
        # Try parsing various date formats
        for fmt in ['%Y-%m-%d', '%Y-%m-%dT%H:%M:%S', '%Y-%m-%d %H:%M:%S']:
            try:
                date_obj = datetime.strptime(date_str[:19], fmt)
                return date_obj.strftime('%Y-%m-%d')
            except:
                continue
    except:
        pass

    return date_str


def truncate_text(text: str, max_length: int = 500) -> str:
    """Truncate text to specified length with ellipsis"""
    if not text:
        return ""

    if len(text) <= max_length:
        return text

    return text[:max_length - 3] + "..."


def get_recent_files(directory: str, hours: int = 24) -> List[Path]:
    """Get files modified within the last N hours"""
    dir_path = Path(directory)
    cutoff_time = datetime.now() - timedelta(hours=hours)

    recent_files = []
    for file in dir_path.glob("*"):
        if file.is_file():
            file_time = datetime.fromtimestamp(file.stat().st_mtime)
            if file_time > cutoff_time:
                recent_files.append(file)

    return sorted(recent_files, key=lambda x: x.stat().st_mtime, reverse=True)


def merge_competitor_data(data_list: List[Dict]) -> Dict:
    """Merge multiple data entries for the same competitor"""
    merged = {
        'articles': [],
        'timestamps': [],
        'errors': []
    }

    for data in data_list:
        merged['articles'].extend(data.get('articles', []))
        merged['timestamps'].append(data.get('timestamp'))
        if 'error' in data:
            merged['errors'].append(data['error'])

    # Remove duplicate articles based on title
    seen_titles = set()
    unique_articles = []
    for article in merged['articles']:
        title = article.get('title')
        if title and title not in seen_titles:
            seen_titles.add(title)
            unique_articles.append(article)

    merged['articles'] = unique_articles
    return merged


def calculate_statistics(data_dir: str = "data/raw") -> Dict:
    """Calculate statistics from scraped data"""
    stats = {
        'total_files': 0,
        'total_articles': 0,
        'competitors': {},
        'date_range': {
            'start': None,
            'end': None
        }
    }

    data_path = Path(data_dir)
    json_files = list(data_path.glob("*.json"))

    stats['total_files'] = len(json_files)

    for file in json_files:
        data = load_json_file(file)
        if data:
            competitor = data.get('competitor', 'Unknown')
            articles = data.get('articles', [])

            if competitor not in stats['competitors']:
                stats['competitors'][competitor] = {
                    'file_count': 0,
                    'article_count': 0,
                    'error_count': 0
                }

            stats['competitors'][competitor]['file_count'] += 1
            stats['competitors'][competitor]['article_count'] += len(articles)
            if 'error' in data:
                stats['competitors'][competitor]['error_count'] += 1

            stats['total_articles'] += len(articles)

            # Update date range
            timestamp = data.get('timestamp')
            if timestamp:
                if not stats['date_range']['start'] or timestamp < stats['date_range']['start']:
                    stats['date_range']['start'] = timestamp
                if not stats['date_range']['end'] or timestamp > stats['date_range']['end']:
                    stats['date_range']['end'] = timestamp

    return stats


def main():
    """Test utility functions"""
    print("Testing utility functions...")

    # Ensure directories exist
    ensure_directories()
    print("✓ Directories created/verified")

    # Test URL validation
    test_urls = [
        "https://openai.com/blog",
        "not-a-url",
        "http://example.com"
    ]
    for url in test_urls:
        print(f"URL '{url}' valid: {validate_url(url)}")

    # Calculate statistics
    stats = calculate_statistics()
    print(f"\nStatistics: {json.dumps(stats, indent=2)}")


if __name__ == "__main__":
    main()