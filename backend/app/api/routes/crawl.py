from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.db.session import get_db
from app.models.crawl import CrawlRecord
from app.schemas.crawl import CrawlRecordOut

router = APIRouter(prefix="/crawl", tags=["crawl"])

@router.get("/records", response_model=list[CrawlRecordOut])
def list_records(db: Session = Depends(get_db)):
    rows = db.scalars(select(CrawlRecord).order_by(CrawlRecord.id.desc()).limit(50)).all()
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
