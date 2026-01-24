import logging
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import markdown
from dotenv import load_dotenv
from src.utils import setup_logging

load_dotenv()
logger = setup_logging()

def send_report(report_markdown=None, recipient=None):
    """
    Sends the report via Gmail SMTP using environment variables.
    """
    if report_markdown is None:
        try:
            with open("data/report.md", "r", encoding="utf-8") as f:
                report_markdown = f.read()
        except FileNotFoundError:
            logger.error("Report file not found.")
            import sys
            sys.exit(1)

    logger.info("Preparing to send email...")
    
    if not report_markdown:
        logger.error("No report content to send.")
        import sys
        sys.exit(1)

    # Convert Markdown to HTML
    html_body = markdown.markdown(report_markdown)
    
    # Get credentials from environment
    sender_email = os.getenv("EMAIL_SENDER")
    password = os.getenv("EMAIL_PASSWORD")
    
    if not recipient:
        recipient = os.getenv("EMAIL_RECIPIENT", "dk5058203@gmail.com")

    if not sender_email or not password:
        logger.warning("EMAIL_SENDER or EMAIL_PASSWORD not set. Skipping actual email delivery (Simulation Mode).")
        logger.info(f"Generated HTML Content (preview):\n{html_body[:200]}...")
        return

    try:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient
        msg['Subject'] = "🏏 Weekly Cricket News Report"

        msg.attach(MIMEText(html_body, 'html'))

        logger.info(f"Connecting to SMTP server for {sender_email}...")
        # Gmail SMTP configuration
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, password)
            server.send_message(msg)
        
        logger.info(f"Email successfully sent to {recipient}")
    except Exception as e:
        logger.error(f"Failed to send email: {e}")
        import sys
        sys.exit(1)

if __name__ == "__main__":
    send_report()


