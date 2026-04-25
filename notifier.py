import aiohttp
import smtplib
from email.mime.text import MIMEText
from loguru import logger
from src.config import Config

async def send_telegram(message: str):
    if not Config.TELEGRAM_BOT_TOKEN or not Config.TELEGRAM_CHAT_ID:
        return
    url = f"https://api.telegram.org/bot{Config.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": Config.TELEGRAM_CHAT_ID, "text": message, "parse_mode": "HTML"}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as resp:
            if resp.status == 200:
                logger.info("📩 Telegram уведомление отправлено")
            else:
                logger.error(f"❌ Telegram ошибка: {resp.status}")

def send_email(subject: str, body: str):
    if not all([Config.SMTP_HOST, Config.SMTP_USER, Config.NOTIFY_EMAIL]):
        return
    msg = MIMEText(body, "html")
    msg["Subject"] = subject
    msg["From"] = Config.SMTP_USER
    msg["To"] = Config.NOTIFY_EMAIL
    try:
        with smtplib.SMTP(Config.SMTP_HOST, Config.SMTP_PORT) as server:
            server.starttls()
            server.login(Config.SMTP_USER, Config.SMTP_PASS)
            server.send_message(msg)
        logger.info("📧 Email уведомление отправлено")
    except Exception as e:
        logger.error(f"❌ SMTP ошибка: {e}")