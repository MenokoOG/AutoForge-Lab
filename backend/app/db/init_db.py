from app.db.base import Base
from app.db.session import engine

# Import models so metadata is populated
from app.models.crawl import CrawlRecord, CrawlRequestLog, JobRun  # noqa: F401


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
