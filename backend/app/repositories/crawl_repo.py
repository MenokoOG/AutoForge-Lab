from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.crawl import CrawlRecord, CrawlRequestLog, JobRun


class CrawlRepository:
    def __init__(self, db: Session):
        self.db = db

    def upsert_record(
        self,
        *,
        source: str,
        title: str,
        url: str,
        tags_csv: str,
        fetched_at: str,
        content_hash: str,
    ) -> CrawlRecord:
        existing = self.db.scalar(select(CrawlRecord).where(CrawlRecord.content_hash == content_hash))
        if existing:
            # update minimal fields (optional)
            existing.title = title
            existing.url = url
            existing.tags = tags_csv
            existing.fetched_at = fetched_at
            self.db.commit()
            self.db.refresh(existing)
            return existing

        rec = CrawlRecord(
            source=source,
            title=title,
            url=url,
            tags=tags_csv,
            fetched_at=fetched_at,
            content_hash=content_hash,
            created_at=fetched_at,
        )
        self.db.add(rec)
        self.db.commit()
        self.db.refresh(rec)
        return rec

    def log_request(
        self,
        *,
        job_id: str,
        run_id: str,
        method: str,
        url: str,
        host: str,
        robots_allowed: bool,
        status_code: int,
        duration_ms: int,
        error_type: str = "",
        error_message: str = "",
        created_at: str,
    ) -> None:
        row = CrawlRequestLog(
            job_id=job_id,
            run_id=run_id,
            method=method,
            url=url,
            host=host,
            robots_allowed="true" if robots_allowed else "false",
            status_code=status_code,
            duration_ms=duration_ms,
            error_type=error_type,
            error_message=error_message,
            created_at=created_at,
        )
        self.db.add(row)
        self.db.commit()

    def job_run_start(self, *, job_id: str, run_id: str, started_at: str) -> None:
        row = JobRun(job_id=job_id, run_id=run_id, status="started", started_at=started_at)
        self.db.add(row)
        self.db.commit()

    def job_run_finish(self, *, job_id: str, run_id: str, status: str, finished_at: str, message: str = "") -> None:
        row = self.db.scalar(select(JobRun).where(JobRun.job_id == job_id, JobRun.run_id == run_id))
        if not row:
            return
        row.status = status
        row.finished_at = finished_at
        row.message = message
        self.db.commit()