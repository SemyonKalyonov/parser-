from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, String, DateTime, Text, UniqueConstraint
from src.config import Config
import asyncpg  # опционально для Postgres

Base = declarative_base()

class JobRecord(Base):
    __tablename__ = "jobs"
    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    company = Column(String)
    url = Column(Text, unique=True)
    location = Column(String)
    salary = Column(String)
    published_at = Column(DateTime)
    meta_hash = Column(String, unique=True)

engine = create_async_engine(Config.DB_URL, echo=False)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def upsert_job(data: dict):
    async with async_session() as session:
        stmt = """
            INSERT INTO jobs (id, title, company, url, location, salary, published_at, meta_hash)
            VALUES (:id, :title, :company, :url, :location, :salary, :published_at, :meta_hash)
            ON CONFLICT(meta_hash) DO NOTHING
        """
        try:
            await session.execute(stmt, data)
            await session.commit()
            return True
        except Exception:
            await session.rollback()
            return False

async def get_new_count() -> int:
    async with async_session() as session:
        result = await session.execute("SELECT COUNT(*) FROM jobs")
        return result.scalar()