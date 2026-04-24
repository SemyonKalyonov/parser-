import asyncio
from playwright.async_api import async_playwright
from loguru import logger
from src.config import Config
from src.utils import get_random_ua, random_delay, check_robots, compute_hash
from src.models import JobItem
from src.db import upsert_job
import pandas as pd

async def scrape_and_save():
    if not check_robots(Config.TARGET_URL):
        logger.warning("🚫 robots.txt запрещает парсинг. Остановка.")
        return 0, 0

    logger.info("🚀 Запуск парсера...")
    new_count = 0
    errors = 0

    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent=get_random_ua(),
            viewport={"width": 1280, "height": 720}
        )
        page = await context.new_page()
        await page.set_extra_http_headers({"Accept-Language": "ru-RU,ru;q=0.9"})

        await page.goto(Config.TARGET_URL, wait_until="domcontentloaded")
        await asyncio.sleep(2)

        # Пример бесконечного скролла / пагинации
        for _ in range(Config.MAX_PAGES):
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            random_delay(1.0, 2.5)
            # Если есть кнопка "Показать ещё"
            try:
                load_more = page.locator("button:has-text('Показать ещё')")
                if await load_more.count() > 0:
                    await load_more.click()
                    await page.wait_for_timeout(1500)
            except Exception:
                pass

        items = await page.locator(".job-card, .listing-item").all()
        logger.info(f"📦 Найдено элементов: {len(items)}")

        for item in items:
            try:
                title = (await item.locator(".title").inner_text()).strip()
                company = (await item.locator(".company").inner_text()).strip()
                url = await item.locator("a").get_attribute("href")
                location = (await item.locator(".location").inner_text()).strip() or "Remote"
                salary = (await item.locator(".salary").inner_text()).strip() or "Не указана"

                if not url.startswith("http"):
                    url = f"https://example.com{url}"

                meta_hash = compute_hash(title, url, company)
                job = JobItem(
                    title=title, company=company, url=url,
                    location=location, salary=salary, meta_hash=meta_hash
                )

                inserted = await upsert_job(job.model_dump())
                if inserted:
                    new_count += 1
            except Exception as e:
                errors += 1
                logger.error(f"❌ Ошибка парсинга элемента: {e}")

        await browser.close()

    logger.info(f"✅ Завершено. Новых: {new_count}, Ошибок: {errors}")
    return new_count, errors