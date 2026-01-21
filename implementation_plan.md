# Implementation Plan - Cricket News Reporting Agent

## 1. Project Overview
The Cricket News Reporting Agent is an autonomous system designed to scrape, analyze, and deliver weekly cricket news summaries. It mimics the style of "The Hindu" sports section and ensures delivery via Gmail.

## 2. Directory Structure
```
Cricket-Agent/
├── .agent/
│   ├── rules/
│   │   └── format.md       # Enforces clean Markdown output
│   └── workflows/
│       └── weekly_report.md # Workflow for weekly automation
├── src/
│   ├── __init__.py
│   ├── scraper.py          # Handles browser tool interactions
│   ├── analyzer.py         # Processes data with Gemini 3 Pro
│   ├── mailer.py           # Handles Gmail MCP delivery
│   └── utils.py            # Helper functions (logging, config)
├── data/
│   └── news_cache.json     # Temporary storage for scraped data
├── ORIGINAL_CONCEPT.md     # Project vision
├── PRD.md                  # Technical specifications
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

## 3. Implementation Steps

### Phase 1: Foundation & Configuration
- [x] Create `ORIGINAL_CONCEPT.md` and `PRD.md`.
- [ ] Create `.agent/rules/format.md` to enforce strictly formatted output.
- [ ] Set up Python environment and `requirements.txt`.

### Phase 2: Scraping Engine (`src/scraper.py`)
- [ ] Implement `fetch_cricket_news()` using the Antigravity Browser Tool.
- [ ] Target sources: ESPNcricinfo, Cricbuzz.
- [ ] Filter for news within the last 7 days (or 24h for daily testing).
- [ ] Save raw data to `data/news_cache.json`.

### Phase 3: Analysis & Formatting (`src/analyzer.py`)
- [ ] Implement `summarize_news()` using Gemini 3 Pro.
- [ ] Define prompt templates to enforce "The Hindu" style.
- [ ] Ensure output matches the 4 required headers:
    - `HEADLINE MATCH SUMMARY`
    - `GLOBAL CRICKET BULLETIN`
    - `TODAY'S SCOREBOARD RECAP`
    - `INJURY & ADMIN NOTES`

### Phase 4: Delivery System (`src/mailer.py`)
- [ ] Integrate with Gmail MCP.
- [ ] Convert Markdown summary to HTML (optional, or send as plain text/markdown).
- [ ] Implement `send_report()` function.

### Phase 5: Automation
- [ ] Create `.agent/workflows/weekly_report.md` to orchestrate the process.
- [ ] Verify end-to-end flow.

## 4. Immediate Next Actions
1.  Initialize the `src` directory and empty script files.
2.  Attempt to create `.agent/rules/format.md` again (or verify permissions).
3.  Begin implementing `src/scraper.py`.
