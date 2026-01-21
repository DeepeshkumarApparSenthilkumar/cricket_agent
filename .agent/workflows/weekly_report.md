---
description: Run the weekly cricket news report workflow
---
# Weekly Cricket News Report Workflow

This workflow automates the scraping, analysis, and delivery of the weekly cricket news report.

1.  **Install Dependencies** (Optional, but good for safety)
    ```bash
    pip install -r requirements.txt
    ```

2.  **Scrape News**
    Fetches the latest cricket news from the last 7 days.
    ```bash
    python -m src.scraper
    ```

3.  **Analyze & Format**
    Processes the scraped data and generates a Markdown report.
    ```bash
    python -m src.analyzer
    ```

4.  **Send Email**
    Converts the report to HTML and sends it via Gmail (MCP/SMTP).
    ```bash
    python -m src.mailer
    ```

// turbo-all
