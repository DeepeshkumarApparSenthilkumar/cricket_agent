import os
import logging
import json
from dotenv import load_dotenv
from src.utils import setup_logging, load_data

load_dotenv()

logger = setup_logging()

def generate_fallback_report(headlines, matches, injuries):
    """
    Simple rule-based formatter if LLM is unavailable.
    """
    report = []
    
    if matches:
        report.append("# 🏏 HEADLINE MATCH SUMMARY")
        for m in matches[:3]: # Top 3
            title = m.get('title', 'Match')
            summary = m.get('summary', '')
            link = m.get('href', '')
            report.append(f"### {title}")
            if summary:
                report.append(f"{summary}")
            if link:
                report.append(f"[Read full story]({link})")
            report.append("")
    
    if headlines:
        report.append("# 📰 GLOBAL CRICKET BULLETIN")
        for h in headlines[:5]:
            title = h.get('title', '')
            summary = h.get('summary', '')
            link = h.get('href', '')
            report.append(f"**{title}**")
            if summary:
                report.append(f"> {summary}")
            if link:
                report.append(f"[Read more]({link})")
            report.append("")

    if matches:
        report.append("# 📊 TODAY'S SCOREBOARD RECAP")
        report.append("| Match | Summary |")
        report.append("| :--- | :--- |")
        for m in matches:
            title = m.get('title', 'Match')
            report.append(f"| {title} | See summary above |")
        report.append("")

    if injuries:
        report.append("# 📝 INJURY & ADMIN NOTES")
        for i in injuries:
            title = i.get('title', '')
            summary = i.get('summary', '')
            report.append(f"* **{title}**: {summary}")
    
    return "\n".join(report)

def summarize_news(data_file="data/news_cache.json"):
    logger.info("Starting news analysis...")
    data = load_data(data_file)
    if not data:
        logger.error("No data found to analyze.")
        return None

    # Check if we have data
    headlines = data.get('headlines', [])
    matches = data.get('match_results', [])
    injuries = data.get('injuries', [])

    if not headlines and not matches and not injuries:
        logger.warning("Data is empty. Cannot generate report.")
        return "# Cricket News Report\n\nNo recent news found."

    # Construct the prompt context
    context = f"""
    Headlines: {json.dumps(headlines, indent=2)}
    Match Results: {json.dumps(matches, indent=2)}
    Injuries: {json.dumps(injuries, indent=2)}
    """

    report = ""
    api_key = os.getenv("GEMINI_API_KEY")
    
    if api_key:
        try:
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-2.0-flash')
            
            prompt = f"""
            You are a cricket sports editor for The Hindu. 
            Analyze the following raw data and generate a report in Markdown.
            
            Data:
            {context}

            Requirements:
            1. Use these exact headers:
               - # 🏏 HEADLINE MATCH SUMMARY
               - # 📰 GLOBAL CRICKET BULLETIN
               - # 📊 TODAY'S SCOREBOARD RECAP
               - # 📝 INJURY & ADMIN NOTES
            2. If a section has no data, omit the header.
            3. No conversational filler. Raw markdown only.
            """
            
            response = model.generate_content(prompt)
            report = response.text
            logger.info("Report generated using Gemini.")
        except Exception as e:
            logger.error(f"Failed to generate with Gemini: {e}")
            report = generate_fallback_report(headlines, matches, injuries)
    else:
        logger.warning("GEMINI_API_KEY not found. Using fallback formatter.")
        report = generate_fallback_report(headlines, matches, injuries)

    # Save report to file
    report_path = "data/report.md"
    try:
        os.makedirs(os.path.dirname(report_path), exist_ok=True)
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report)
        logger.info(f"Report saved to {report_path}")
    except Exception as e:
        logger.error(f"Failed to save report: {e}")

    return report

if __name__ == "__main__":
    summarize_news()
