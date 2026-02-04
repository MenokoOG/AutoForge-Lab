from sqlalchemy import String, Text, DateTime, Integer, func, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class CrawlRecord(Base):
    __tablename__ = "crawl_records"
    __table_args__ = (UniqueConstraint("content_hash", name="uq_crawl_records_content_hash"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    source: Mapped[str] = mapped_column(String(64), index=True)
    title: Mapped[str] = mapped_column(String(512))
    url: Mapped[str] = mapped_column(String(2048))
    tags: Mapped[str] = mapped_column(String(512), default="")  # comma-separated for MVP
    content_hash: Mapped[str] = mapped_column(String(64), index=True)

    fetched_at: Mapped[str] = mapped_column(String(64))  # ISO timestamp (simple MVP)
    created_at: Mapped[str] = mapped_column(String(64), default="")  # optional


class CrawlRequestLog(Base):
    __tablename__ = "crawl_requests"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    job_id: Mapped[str] = mapped_column(String(64), index=True)
    run_id: Mapped[str] = mapped_column(String(64), index=True)

    method: Mapped[str] = mapped_column(String(16))
    url: Mapped[str] = mapped_column(String(2048))
    host: Mapped[str] = mapped_column(String(255), index=True)

    robots_allowed: Mapped[str] = mapped_column(String(8))  # "true"/"false"
    status_code: Mapped[int] = mapped_column(Integer, default=0)
    duration_ms: Mapped[int] = mapped_column(Integer, default=0)

    error_type: Mapped[str] = mapped_column(String(128), default="")
    error_message: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[str] = mapped_column(String(64), default="")


class JobRun(Base):
    __tablename__ = "job_runs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    job_id: Mapped[str] = mapped_column(String(64), index=True)
    run_id: Mapped[str] = mapped_column(String(64), index=True)

    status: Mapped[str] = mapped_column(String(32))  # "started"|"success"|"failed"
    started_at: Mapped[str] = mapped_column(String(64))
    finished_at: Mapped[str] = mapped_column(String(64), default="")
    message: Mapped[str] = mapped_column(Text, default="")