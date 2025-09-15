# AI Competitor Tracker

A web-scraping competitive intelligence application that monitors AI companies and generates daily reports about the competitive landscape.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the scraper
python scraper.py

# Generate a report
python report_generator.py
```

## Tutorial: Building Your First Web-Scraping App (60 minutes)

### Prerequisites
- Python 3.8+
- Claude Code installed
- VS Code installed
- GitHub account

### Step 1: Set Up GitHub Repository (10 min)

1. **Create a new repository on GitHub:**
   - Go to github.com and click "New repository"
   - Name it: `ai-competitor-tracker`
   - Initialize with README
   - Click "Create repository"

2. **Clone locally:**
   ```bash
   git clone https://github.com/[your-username]/ai-competitor-tracker
   cd ai-competitor-tracker
   ```

### Step 2: Open in VS Code (5 min)

```bash
code .
```
Or: File → Open Folder → Select `ai-competitor-tracker`

### Step 3: Create Claude.md File (10 min)

Create a `Claude.md` file to give Claude Code context about your project. This file helps Claude understand your goals and technical stack.

### Step 4: Launch Claude Code (5 min)

In VS Code terminal:
```bash
claude-code
```

Claude Code will read your project structure and be ready to help.

### Step 5: Build the Application (20 min)

Use Claude Code slash commands:
- `/start` - Initialize project
- `/files` - View project structure
- `/run` - Execute code
- `/explain` - Get code explanations
- `/fix` - Debug issues

Ask Claude Code to:
1. "Create the basic web scraper structure"
2. "Add competitor website configurations"
3. "Build the report generator"
4. "Add scheduling functionality"

### Step 6: Test Your Scraper (5 min)

```bash
# Test the scraper
python scraper.py --test

# Generate a sample report
python report_generator.py
```

### Step 7: Commit Changes (5 min)

```bash
git add .
git commit -m "Initial web scraper implementation"
git push origin main
```

### Step 8: Create Pull Requests (Bonus)

```bash
# Create feature branch
git checkout -b feature/add-new-competitor

# Make changes, then:
git add .
git commit -m "Add new competitor tracking"
git push origin feature/add-new-competitor
```

Go to GitHub and create a pull request.

## Project Structure

```
ai-competitor-tracker/
├── README.md              # This file
├── Claude.md             # Claude Code context
├── scraper.py           # Main scraping logic
├── report_generator.py  # Report creation
├── config.json          # Website configurations
├── requirements.txt     # Python dependencies
├── reports/            # Generated reports directory
│   └── YYYY-MM-DD.md   # Daily reports
├── data/              # Scraped data storage
│   └── raw/          # Raw scraped data
└── tests/            # Test files
    └── test_scraper.py
```

## Features

- **Multi-Source Scraping**: Monitors multiple AI company websites
- **Intelligent Extraction**: Parses news, blogs, and product updates
- **Daily Reports**: Automated markdown report generation
- **Change Detection**: Tracks pricing and feature changes
- **Error Handling**: Robust error recovery and logging
- **Scheduling**: Automated daily runs

## Configuration

Edit `config.json` to add or modify tracked websites:

```json
{
  "competitors": [
    {
      "name": "OpenAI",
      "url": "https://openai.com/blog",
      "selector": ".blog-post"
    },
    {
      "name": "Google AI",
      "url": "https://ai.google/research/pubs",
      "selector": ".publication-card"
    }
  ],
  "report_format": "markdown",
  "schedule": "daily"
}
```

## Key Components

### 1. Web Scraper (`scraper.py`)
- Fetches content from competitor websites
- Parses HTML using BeautifulSoup
- Extracts relevant information
- Handles rate limiting and errors

### 2. Report Generator (`report_generator.py`)
- Aggregates scraped data
- Identifies key insights
- Formats into readable markdown
- Highlights important changes

### 3. Configuration (`config.json`)
- Defines target websites
- Sets scraping parameters
- Configures report preferences

## Usage Examples

### Basic Scraping
```python
from scraper import CompetitorScraper

scraper = CompetitorScraper()
data = scraper.scrape_all()
print(data)
```

### Generate Report
```python
from report_generator import ReportGenerator

generator = ReportGenerator()
report = generator.create_daily_report()
generator.save_report(report)
```

### Schedule Daily Runs
```python
from scheduler import schedule_daily_scrape

schedule_daily_scrape(hour=9, minute=0)  # Run at 9:00 AM daily
```

## Development Workflow

1. **Make changes in feature branch**
2. **Test locally using `/run` in Claude Code**
3. **Commit with descriptive messages**
4. **Push to GitHub**
5. **Create pull request for review**

## Claude Code Tips

- **Use slash commands** for quick actions
- **Ask specific questions** for better assistance
- **Keep Claude.md updated** with project context
- **Use hooks** for automated workflows
- **Test frequently** with `/run` command

## Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| Rate limiting | Add delays between requests |
| SSL errors | Use `verify=False` cautiously |
| Parsing fails | Update CSS selectors |
| No data found | Check if website structure changed |

## Dependencies

- `requests` - HTTP requests
- `beautifulsoup4` - HTML parsing
- `pandas` - Data manipulation
- `schedule` - Task scheduling
- `python-dotenv` - Environment variables

## Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Add tests
5. Submit pull request

## License

MIT License - See LICENSE file for details

## Next Steps

- [ ] Add more competitor sources
- [ ] Implement sentiment analysis
- [ ] Create web dashboard
- [ ] Add email notifications
- [ ] Build API endpoints
- [ ] Add machine learning insights

## Glossary

- **Web Scraping**: Automatically extracting data from websites
- **Repository**: Project folder tracked by Git
- **Pull Request**: Proposed changes for review
- **Commit**: Saved snapshot of code changes
- **Branch**: Isolated development environment
- **Hook**: Automated action triggered by events
- **Dependency**: External library your code needs

## Support

For issues or questions:
1. Check the documentation
2. Use `/explain` in Claude Code
3. Create an issue on GitHub
4. Ask in discussions

---

Built with Claude Code 🤖 | Tutorial Time: ~60 minutes
