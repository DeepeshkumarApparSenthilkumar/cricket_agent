# Cricket News Reporting Agent - Product Requirements Document (PRD)

## Technical Stack
-   **Orchestration**: Antigravity Agent Manager
-   **Search**: Antigravity Browser Tool
-   **Processing**: Gemini 3 Pro
-   **Delivery**: Gmail MCP Server

## Implementation Phases
1.  **Phase 1: Knowledge Acquisition**: Search for cricket news from the last 24 hours/7 days using the browser tool.
2.  **Phase 2: Data Processing**: Summarize news into specific sections:
    -   Headline Match
    -   Global Bulletin
    -   Scoreboard
    -   Injuries
3.  **Phase 3: Formatting**: Apply strict Markdown cleaning to remove AI "chatter".
4.  **Phase 4: Distribution**: Integrate with Gmail MCP to send the report.

## Functional Requirements

### Scraping (`scraper.py`)
-   Use Google Search tool.
-   Sources: ESPNcricinfo, Cricbuzz.
-   Timeframe: Last 24 hours (or 7 days for weekly).
-   Focus: Match Summary, Global Headlines, Player Injury updates.

### Formatting Module
-   Process raw data into these headers:
    -   `# 🏏 HEADLINE MATCH SUMMARY`
    -   `# 📰 GLOBAL CRICKET BULLETIN`
    -   `# 📊 TODAY'S SCOREBOARD RECAP`
    -   `# 📝 INJURY & ADMIN NOTES`
-   **Rule**: If a section is empty, do not include the header.

### Delivery (`mailer.py`)
-   Convert Markdown to clean HTML.
-   Send via Gmail MCP to `dk5058203@gmail.com`.

## Automation
-   Weekly trigger (Sunday 1 PM).
