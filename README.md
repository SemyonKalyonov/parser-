# Dynamic Parser & Notification Pipeline

[![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)](https://www.python.org/)
[![Playwright](https://img.shields.io/badge/Playwright-1.40+-green?logo=playwright)](https://playwright.dev/)
[![Pydantic](https://img.shields.io/badge/Pydantic-v2-orange?logo=pydantic)](https://docs.pydantic.dev/)
[![Docker](https://img.shields.io/badge/Docker-Compose-blue?logo=docker)](https://docs.docker.com/compose/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

Асинхронный парсер динамического контента с встроенной валидацией, дедупликацией, планировщиком и системой уведомлений. Проект реализует устойчивый пайплайн сбора публичных данных в условиях JS-рендеринга, пагинации и базовой анти-бот защиты.

## Основные возможности

| Категория | Реализация |
|-----------|------------|
| Динамический контент | Обход бесконечного скролла, пагинации, ожидание рендеринга JS-элементов |
| Дедупликация | SHA-256 хеш + `ON CONFLICT DO NOTHING` на уровне БД |
| Валидация данных | Pydantic v2 с строгой типизацией перед записью |
| Расписание | APScheduler (CRON-триггеры, асинхронный режим) |
| Уведомления | Telegram Bot API + SMTP (email) |
| Анти-детект | Ротация User-Agent, рандомные задержки, проверка `robots.txt` |
| Изоляция среды | `docker-compose` (Parser + SQLite/PostgreSQL) |
| Метрики и логи | Фиксация времени выполнения, количества записей, ошибок, статуса валидации |

## Стек технологий
`Python 3.11+` | `Playwright (async)` | `Pydantic v2` | `SQLAlchemy 2.0` | `APScheduler 3.10+` | `aiohttp` | `SQLite/PostgreSQL` | `Docker Compose` | `Loguru`

## Архитектура и поток данных
Playwright (JS-рендеринг)
↓
Сырые данные из DOM
↓
JobItem(**data) → Валидация через Pydantic (типы, URL, значения по умолчанию)
↓
SQLAlchemy (async) → UPSERT в БД (дедупликация по meta_hash)
↓
APScheduler → Выполнение по расписанию
↓
Notifier → Отправка уведомлений в Telegram / Email при появлении новых записей
↓
Loguru → Структурированные логи + сбор метрик

## Быстрый старт

### 1. Клонирование и подготовка

git clone https://github.com/your-username/dynamic-parser.git
cd dynamic-parser
cp .env.example .env
TARGET_URL=https://example.com/jobs TELEGRAM_BOT_TOKEN=123456:ABC-DEF... TELEGRAM_CHAT_ID=123456789 SMTP_HOST=smtp.gmail.com SMTP_PORT=587 SMTP_USER=your@email.com SMTP_PASS=app_password NOTIFY_EMAIL=recipient@email.com SCHEDULE_CRON=*/30 * * * *

Логи и метрики
Логи сохраняются в директории logs/ с ротацией по размеру (10 МБ) и хранением в течение 30 дней.
Пример вывода
2024-05-12 14:30:01 | INFO | Starting parser...
2024-05-12 14:30:05 | INFO | Found elements: 42
2024-05-12 14:30:12 | INFO | Completed. New: 7, Errors: 1
2024-05-12 14:30:12 | INFO | Time: 11.42s | Records: 7 | Errors: 1 | Total in DB: 154

# Добавить в конец функции scrape_and_save():
pd.DataFrame(jobs_list).to_csv("data/export_latest.csv", index=False)

# Структура проекта
.
├── docker-compose.yml      # конфиг для запуска парсера и БД в контейнерах
├── Dockerfile              # образ с chromium и зависимостями
├── requirements.txt        # список пакетов
├── .env.example            # шаблон переменных (свой .env в гит не класть)
├── .gitignore              # исключаем секреты, логи и файлы БД
├── src/
│   ├── config.py           # чтение переменных из окружения
│   ├── models.py           # pydantic-схемы, валидация перед записью в БД
│   ├── db.py               # подключение к SQLite/Postgres, создание таблиц, UPSERT
│   ├── scraper.py          # основная логика: скролл, парсинг DOM, обработка элементов
│   ├── notifier.py         # отправка отчётов в Telegram или на email
│   ├── scheduler.py        # cron-расписание для периодического запуска
│   ├── utils.py            # вспомогательные функции: задержки, смена UA, robots.txt, хеши
│   └── main.py             # точка входа: инициализация логов и запуск шедулера
└── README.md               # описание проекта