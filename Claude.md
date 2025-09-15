# AI Competitor Tracker

## Project Overview
A web scraping application that monitors AI companies and generates daily competitive intelligence reports.

## Goal
Track competitors like OpenAI, Google AI, Microsoft AI, Anthropic, Cohere, and others to understand:
- Product announcements and launches
- Pricing changes and model updates
- New features and capabilities
- Market positioning and strategy shifts
- Research publications and breakthroughs
- Partnership announcements

## Technical Stack
- Python 3.8+ for web scraping
- Beautiful Soup 4 for HTML parsing
- Requests library for HTTP requests
- JSON for configuration and data storage
- Markdown for report generation
- Schedule library for automation
- Pandas for data analysis

## Key Features Needed
1. Web scraper that visits competitor websites and blogs
2. Intelligent data extraction from news/blog sections
3. Change detection for pricing and features
4. Daily report generation in markdown format
5. Simple scheduling system for automation
6. Error handling and retry logic
7. Rate limiting to avoid being blocked

## File Structure
```
├── scraper.py           # Main scraping logic
├── report_generator.py  # Report creation module
├── config.json         # Website URLs and selectors
├── scheduler.py        # Automation scheduling
├── utils.py           # Helper functions
├── reports/           # Generated daily reports
├── data/             # Scraped data storage
│   └── raw/         # Raw JSON data
├── tests/           # Test files
└── requirements.txt # Python dependencies
```

## Development Approach
1. Start with a simple scraper for one website (OpenAI)
2. Abstract the scraping logic to work with multiple sites
3. Add intelligent parsing for different page structures
4. Implement change detection and comparison
5. Create markdown report generation
6. Add scheduling for daily runs
7. Implement error handling and logging

## Scraping Targets
- OpenAI Blog: https://openai.com/blog
- Google AI Blog: https://ai.google/research/pubs
- Microsoft AI: https://blogs.microsoft.com/ai/
- Anthropic News: https://www.anthropic.com/news
- Cohere Blog: https://cohere.com/blog

## Report Format
Daily reports should include:
- Executive summary of key developments
- Product/feature updates by company
- Pricing changes
- Research publications
- Market trends and insights
- Competitive positioning analysis

## Important Considerations
- Respect robots.txt and rate limits
- Handle dynamic content (JavaScript-rendered pages)
- Store historical data for trend analysis
- Make the system extensible for new competitors
- Keep reports concise and actionable

## Success Criteria
- Successfully scrapes at least 5 competitor sites daily
- Generates readable, insightful reports
- Runs automatically without manual intervention
- Handles errors gracefully
- Provides actionable competitive intelligence