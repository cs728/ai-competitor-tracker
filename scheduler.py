#!/usr/bin/env python3
"""
Scheduler for AI Competitor Tracker
Automates daily scraping and report generation
"""

import json
import logging
import time
from datetime import datetime
from pathlib import Path

import schedule

from scraper import CompetitorScraper
from report_generator import ReportGenerator

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class CompetitorTrackerScheduler:
    """Scheduler for automated competitive intelligence gathering"""

    def __init__(self, config_path: str = "config.json"):
        """Initialize scheduler with configuration"""
        self.config = self._load_config(config_path)
        self.scraper = CompetitorScraper(config_path)
        self.report_generator = ReportGenerator()

    def _load_config(self, config_path: str) -> dict:
        """Load configuration from JSON file"""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(f"Config file {config_path} not found")
            return {}

    def run_daily_task(self):
        """Execute daily scraping and report generation"""
        logger.info("=" * 60)
        logger.info("Starting daily competitive intelligence gathering")
        logger.info(f"Time: {datetime.now()}")
        logger.info("=" * 60)

        try:
            # Step 1: Scrape competitor websites
            logger.info("Step 1: Scraping competitor websites...")
            scraping_results = self.scraper.scrape_all()
            logger.info(f"Scraped {len(scraping_results)} websites")

            # Step 2: Generate report
            logger.info("Step 2: Generating competitive intelligence report...")
            report, report_file = self.report_generator.create_daily_report()
            logger.info(f"Report saved to: {report_file}")

            # Step 3: Send notifications (if configured)
            if self.config.get('notifications', {}).get('enabled'):
                self._send_notifications(report_file)

            logger.info("Daily task completed successfully!")

        except Exception as e:
            logger.error(f"Error in daily task: {e}")
            raise

    def _send_notifications(self, report_file: Path):
        """Send notifications about new report (placeholder)"""
        logger.info(f"Notifications would be sent for report: {report_file}")

    def schedule_daily_scraping(self):
        """Schedule daily scraping based on configuration"""
        schedule_config = self.config.get('schedule', {})

        if not schedule_config.get('enabled', True):
            logger.info("Scheduling is disabled in configuration")
            return

        scheduled_time = schedule_config.get('time', '09:00')

        # Schedule the daily task
        schedule.every().day.at(scheduled_time).do(self.run_daily_task)

        logger.info(f"Daily scraping scheduled for {scheduled_time}")
        logger.info("Scheduler is running. Press Ctrl+C to stop.")

        # Keep the scheduler running
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute

    def run_once(self):
        """Run the scraping and report generation once"""
        self.run_daily_task()


def schedule_daily_scrape(hour: int = 9, minute: int = 0):
    """Convenience function to schedule daily scraping"""
    scheduler = CompetitorTrackerScheduler()

    time_str = f"{hour:02d}:{minute:02d}"
    schedule.every().day.at(time_str).do(scheduler.run_daily_task)

    logger.info(f"Scheduled daily scraping at {time_str}")

    while True:
        schedule.run_pending()
        time.sleep(60)


def main():
    """Main execution function"""
    import argparse

    parser = argparse.ArgumentParser(description='AI Competitor Tracker Scheduler')
    parser.add_argument(
        '--once',
        action='store_true',
        help='Run once instead of scheduling'
    )
    parser.add_argument(
        '--time',
        default='09:00',
        help='Time to run daily (HH:MM format)'
    )

    args = parser.parse_args()

    scheduler = CompetitorTrackerScheduler()

    if args.once:
        print("Running competitive intelligence gathering once...")
        scheduler.run_once()
    else:
        print(f"Starting scheduler for daily runs at {args.time}...")
        # Update config with command line time if provided
        scheduler.config['schedule'] = scheduler.config.get('schedule', {})
        scheduler.config['schedule']['time'] = args.time
        scheduler.schedule_daily_scraping()


if __name__ == "__main__":
    main()