import hashlib
import time
import random
import urllib.robotparser
from loguru import logger

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0"
]

def get_random_ua():
    return random.choice(USER_AGENTS)

def random_delay(min_sec=1.5, max_sec=4.0):
    delay = random.uniform(min_sec, max_sec)
    logger.debug(f"⏱ Задержка: {delay:.2f} сек")
    time.sleep(delay)

def check_robots(url: str) -> bool:
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(f"{url.split('/')[0]}//{url.split('/')[2]}/robots.txt")
    try:
        rp.read()
        return rp.can_fetch("*", url)
    except Exception as e:
        logger.warning(f"⚠️ Не удалось прочитать robots.txt: {e}")
        return True

def compute_hash(title: str, url: str, company: str) -> str:
    payload = f"{title}|{url}|{company}"
    return hashlib.sha256(payload.encode()).hexdigest()