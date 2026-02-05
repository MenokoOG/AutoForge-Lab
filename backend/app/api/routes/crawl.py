from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional, Union

from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import SessionLocal, get_db
from app.models.crawl import CrawlRecord, JobRun
from app.schemas.crawl import CrawlRecordOut

router = APIRouter(prefix="/crawl", tags=["crawl"])


@router.get("/records", response_model=list[CrawlRecordOut])
def list_records(limit: int = 100, db: Session = Depends(get_db)):
    limit = max(1, min(int(limit), 500))
    rows = db.scalars(select(CrawlRecord).order_by(CrawlRecord.id.desc()).limit(limit)).all()

    out: list[CrawlRecordOut] = []
    for r in rows:
        out.append(
            CrawlRecordOut(
                id=r.id,
                source=r.source,
                title=r.title,
                url=r.url,
                tags=[t for t in (r.tags or "").split(",") if t],
                fetched_at=r.fetched_at,
                content_hash=r.content_hash,
            )
        )
    return out


def _run_job_in_background(job_id: int) -> None:
    db = SessionLocal()
    try:
        job = db.get(JobRun, job_id)
        if not job:
            return

        job.status = "running"
        job.started_at = datetime.now(timezone.utc)
        db.commit()

        from app.scheduler.jobs import run_crawl_sampler  # noqa: WPS433

        try:
            run_crawl_sampler()
            job.status = "success"
            job.message = "completed"
        except Exception as e:  # noqa: BLE001
            job.status = "error"
            job.message = f"{type(e).__name__}: {e}"

        job.finished_at = datetime.now(timezone.utc)
        db.commit()
    finally:
        db.close()


@router.post("/run")
def run_crawl_now(background: BackgroundTasks):
    db = SessionLocal()
    try:
        job = JobRun(
            name="manual_crawl",
            status="queued",
            message="queued",
            created_at=datetime.now(timezone.utc),
        )
        db.add(job)
        db.commit()
        db.refresh(job)

        background.add_task(_run_job_in_background, job.id)
        return {"ok": True, "job_id": job.id}
    finally:
        db.close()


def _iso(dt: Optional[Union[datetime, str]]) -> Optional[str]:
    """
    Normalize datetime-ish values to ISO-8601 strings.
    Some DB drivers / mappings can return strings for timestamp fields.
    """
    if dt is None:
        return None

    if isinstance(dt, str):
        # Assume it's already ISO-ish; return as-is.
        # (If you want strict parsing later, we can add it.)
        return dt

    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.isoformat()


@router.get("/jobs")
def list_jobs(limit: int = 20, db: Session = Depends(get_db)):
    limit = max(1, min(int(limit), 100))
    rows = db.scalars(select(JobRun).order_by(JobRun.id.desc()).limit(limit)).all()

    return [
        {
            "id": r.id,
            "name": getattr(r, "name", "crawl"),
            "status": r.status,
            "message": getattr(r, "message", None),
            "created_at": _iso(getattr(r, "created_at", None)),
            "started_at": _iso(getattr(r, "started_at", None)),
            "finished_at": _iso(getattr(r, "finished_at", None)),
        }
        for r in rows
    ]
