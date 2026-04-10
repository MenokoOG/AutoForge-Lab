"""
Pandas crawl analytics helpers.

Pro Tip:
Keep analytics separate from ingestion pipeline.
Pipelines should be deterministic — analytics can be exploratory.
"""

from __future__ import annotations

import pandas as pd
from sqlalchemy.orm import Session

from app.models.crawl import CrawlRecord


def records_to_dataframe(db: Session) -> pd.DataFrame:
    rows = db.query(CrawlRecord).all()

    data = [
        {
            "id": r.id,
            "source": r.source,
            "title": r.title,
            "url": r.url,
            "tags": r.tags,
            "fetched_at": r.fetched_at,
        }
        for r in rows
    ]

    return pd.DataFrame(data)


def count_by_source(df: pd.DataFrame) -> pd.Series:
    return df.groupby("source").size().sort_values(ascending=False)


def recent_activity(df: pd.DataFrame, hours: int = 24) -> pd.DataFrame:
    cutoff = pd.Timestamp.utcnow() - pd.Timedelta(hours=hours)
    return df[df["fetched_at"] >= cutoff]