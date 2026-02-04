import hashlib
import logging
from dataclasses import dataclass
from datetime import datetime, timezone
from urllib.parse import urlparse

from sqlalchemy.orm import Session

from app.crawling.collector import BaseCollector, CrawlBlockedByRobots
from app.extractors.base import BaseExtractor
from app.repositories.crawl_repo import CrawlRepository
from app.schemas.crawl import CrawlRecordIn

logger = logging.getLogger("crawl.pipeline")


def compute_hash(source: str, title: str, url: str) -> str:
    h = hashlib.sha256()
    h.update(source.encode("utf-8"))
    h.update(b"\n")
    h.update(title.strip().encode("utf-8"))
    h.update(b"\n")
    h.update(url.strip().encode("utf-8"))
    return h.hexdigest()


@dataclass
class CrawlPipeline:
    db: Session
    collector: BaseCollector
    extractor: BaseExtractor

    def run(self, *, job_id: str, run_id: str, source: str, start_url: str) -> dict:
        repo = CrawlRepository(self.db)
        now = datetime.now(timezone.utc).isoformat()

        repo.job_run_start(job_id=job_id, run_id=run_id, started_at=now)

        total_saved = 0
        total_seen = 0

        try:
            fetch = self.collector.fetch(start_url)
            repo.log_request(
                job_id=job_id,
                run_id=run_id,
                method="GET",
                url=start_url,
                host=fetch.host,
                robots_allowed=True,
                status_code=fetch.status_code,
                duration_ms=fetch.duration_ms,
                created_at=now,
            )

            records = self.extractor.extract(source=source, url=start_url, html=fetch.text)

            for r in records:
                # Validator happens here because CrawlRecordIn is Pydantic
                record: CrawlRecordIn = r
                total_seen += 1

                tags_csv = ",".join(record.tags)
                content_hash = compute_hash(record.source, record.title, record.url)

                repo.upsert_record(
                    source=record.source,
                    title=record.title,
                    url=record.url,
                    tags_csv=tags_csv,
                    fetched_at=record.fetched_at,
                    content_hash=content_hash,
                )
                total_saved += 1

            finished = datetime.now(timezone.utc).isoformat()
            repo.job_run_finish(job_id=job_id, run_id=run_id, status="success", finished_at=finished)

            logger.info(
                "crawl_success",
                extra={
                    "job_id": job_id,
                    "run_id": run_id,
                    "source": source,
                    "start_url": start_url,
                    "saved": total_saved,
                    "seen": total_seen,
                },
            )

            return {"ok": True, "saved": total_saved, "seen": total_seen}

        except CrawlBlockedByRobots as e:
            host = urlparse(start_url).netloc
            repo.log_request(
                job_id=job_id,
                run_id=run_id,
                method="GET",
                url=start_url,
                host=host,
                robots_allowed=False,
                status_code=0,
                duration_ms=0,
                error_type=type(e).__name__,
                error_message=str(e),
                created_at=now,
            )
            finished = datetime.now(timezone.utc).isoformat()
            repo.job_run_finish(job_id=job_id, run_id=run_id, status="failed", finished_at=finished, message=str(e))
            logger.warning("crawl_blocked", extra={"job_id": job_id, "run_id": run_id, "error": str(e)})
            return {"ok": False, "error": "robots_blocked"}

        except Exception as e:
            host = urlparse(start_url).netloc
            repo.log_request(
                job_id=job_id,
                run_id=run_id,
                method="GET",
                url=start_url,
                host=host,
                robots_allowed=True,
                status_code=0,
                duration_ms=0,
                error_type=type(e).__name__,
                error_message=str(e),
                created_at=now,
            )
            finished = datetime.now(timezone.utc).isoformat()
            repo.job_run_finish(job_id=job_id, run_id=run_id, status="failed", finished_at=finished, message=str(e))
            logger.exception("crawl_failed", extra={"job_id": job_id, "run_id": run_id})
            return {"ok": False, "error": "exception"}