import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    TARGET_URL = os.getenv("TARGET_URL", "https://example.com/jobs")
    SCHEDULE_CRON = os.getenv("SCHEDULE_CRON", "*/30 * * * *")
    DB_URL = os.getenv("DB_URL", "sqlite+aiosqlite:///./data/parser.db")
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
    SMTP_HOST = os.getenv("SMTP_HOST")
    SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
    SMTP_USER = os.getenv("SMTP_USER")
    SMTP_PASS = os.getenv("SMTP_PASS")
    NOTIFY_EMAIL = os.getenv("NOTIFY_EMAIL")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    MAX_PAGES = int(os.getenv("MAX_PAGES", 5))