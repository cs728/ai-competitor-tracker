#!/usr/bin/env python3
"""
Example usage script for AI Competitor Tracker
Demonstrates how to use the scraper and report generator
"""

import json
import sys
from datetime import datetime
from pathlib import Path

# Ensure required directories exist
from utils import ensure_directories, calculate_statistics

def run_example():
    """Run example demonstration of the AI Competitor Tracker"""
    print("=" * 70)
    print("AI COMPETITOR TRACKER - EXAMPLE USAGE")
    print("=" * 70)
    print()

    # Step 1: Setup
    print("📁 Step 1: Setting up directories...")
    ensure_directories()
    print("   ✓ All directories created/verified")
    print()

    # Step 2: Import modules
    print("📦 Step 2: Importing modules...")
    try:
        from scraper import CompetitorScraper
        from report_generator import ReportGenerator
        print("   ✓ Modules imported successfully")
    except ImportError as e:
        print(f"   ❌ Error importing modules: {e}")
        print("   Please run: pip install -r requirements.txt")
        return
    print()

    # Step 3: Initialize components
    print("🔧 Step 3: Initializing components...")
    scraper = CompetitorScraper()
    generator = ReportGenerator()
    print("   ✓ Scraper and report generator initialized")
    print()

    # Step 4: Run scraping (with user confirmation)
    print("🌐 Step 4: Web Scraping")
    print("   This will scrape competitor websites defined in config.json")
    response = input("   Do you want to proceed with scraping? (y/n): ")

    if response.lower() == 'y':
        print("   Starting web scraping...")
        print("   " + "-" * 50)

        results = scraper.scrape_all()

        print("   " + "-" * 50)
        print(f"   ✓ Scraped {len(results)} competitor websites")

        # Show summary of results
        for result in results:
            status = "✓" if 'error' not in result else "✗"
            count = result.get('article_count', 0)
            print(f"   {status} {result['competitor']}: {count} articles")
    else:
        print("   ⏭️  Skipping scraping step")
        # Create sample data for demonstration
        sample_data = {
            'competitor': 'Sample Company',
            'url': 'https://example.com',
            'timestamp': datetime.now().isoformat(),
            'articles': [
                {
                    'title': 'Sample Article Title',
                    'date': datetime.now().isoformat(),
                    'content_preview': 'This is a sample article for demonstration purposes.',
                    'link': 'https://example.com/article'
                }
            ],
            'article_count': 1
        }
        # Save sample data
        sample_file = Path("data/raw") / f"sample_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(sample_file, 'w') as f:
            json.dump(sample_data, f, indent=2)
        print(f"   Created sample data at: {sample_file}")
    print()

    # Step 5: Generate report
    print("📊 Step 5: Generating Report")
    print("   Creating competitive intelligence report...")

    try:
        report, report_file = generator.create_daily_report()
        print(f"   ✓ Report generated: {report_file}")
        print()

        # Show report preview
        print("   Report Preview (first 500 characters):")
        print("   " + "=" * 50)
        print(report[:500] + "..." if len(report) > 500 else report)
        print("   " + "=" * 50)
    except Exception as e:
        print(f"   ❌ Error generating report: {e}")
    print()

    # Step 6: Show statistics
    print("📈 Step 6: Data Statistics")
    stats = calculate_statistics()
    print(f"   Total files: {stats['total_files']}")
    print(f"   Total articles: {stats['total_articles']}")
    print(f"   Competitors tracked: {len(stats['competitors'])}")
    print()

    # Step 7: Next steps
    print("🚀 Next Steps:")
    print("   1. Review the generated report in the 'reports' directory")
    print("   2. Customize config.json to add more competitors")
    print("   3. Run 'python scheduler.py' to enable daily automation")
    print("   4. Use 'python scraper.py' for manual scraping")
    print("   5. Use 'python report_generator.py' to generate reports")
    print()

    print("=" * 70)
    print("Example complete! Check the 'reports' folder for your report.")
    print("=" * 70)


def main():
    """Main entry point"""
    print("\n🤖 Welcome to AI Competitor Tracker!\n")

    # Check Python version
    if sys.version_info < (3, 8):
        print("⚠️  Warning: Python 3.8+ is recommended")

    try:
        run_example()
    except KeyboardInterrupt:
        print("\n\n⛔ Example interrupted by user")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()