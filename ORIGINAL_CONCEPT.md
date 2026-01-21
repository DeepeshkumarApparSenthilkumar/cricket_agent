# Cricket News Reporting Agent - Original Concept

## Executive Summary
An autonomous agent that monitors global and domestic cricket news, summarizes it in the style of The Hindu sports section, and delivers it via Gmail.

## Project Goal
Develop an autonomous Python-based system that:
1.  **Scrapes**: Uses the Antigravity Browser Tool to find global/domestic cricket news from the last 7 days.
2.  **Analyzes**: Uses Gemini 3 Pro to summarize news into four specific sections, mimicking The Hindu style.
3.  **Delivers**: Uses the Gmail MCP Server to send a weekly formatted Markdown email.
4.  **Automates**: Triggers every Sunday at 1 PM.
