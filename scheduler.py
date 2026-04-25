from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from loguru import logger
from src.config import Config
from src.scraper import scrape_and_save
from src.notifier import send_telegram, send_email

async def run_job():
    new, errs = await scrape_and_save()
    if new > 0:
        msg = f"🔍 Обнаружено <b>{new}</b> новых вакансий/записей.\n❌ Ошибок: {errs}"
        await send_telegram(msg)
        send_email("📊 Новые данные парсера", f"Новых записей: {new}<br>Ошибок: {errs}")

def start_scheduler():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(run_job, CronTrigger.from_crontab(Config.SCHEDULE_CRON))
    scheduler.start()
    logger.info(f"⏰ Планировщик запущен. CRON: {Config.SCHEDULE_CRON}")
    return scheduler