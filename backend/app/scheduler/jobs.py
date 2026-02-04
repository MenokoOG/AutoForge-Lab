import logging
import uuid
from datetime import datetime, timezone

from app.core.config import settings
from app.crawling.robots import RobotsClient
from app.crawling.throttle import HostThrottle
from app.crawling.collector import HttpCollector
from app.db.session import SessionLocal
from app.extractors.wikipedia import WikipediaExtractor
from app.extractors.hackernews import HackerNewsExtractor
from app.extractors.arxiv import ArxivExtractor
from app.services.crawl_pipeline import CrawlPipeline

logger = logging.getLogger("scheduler.jobs")


USER_AGENT = "m3n0ko0g-learning-lounge-bot/0.1 (+education)"


def run_crawl_sampler() -> None:
    job_id = "crawl_sampler"
    run_id = uuid.uuid4().hex
    now = datetime.now(timezone.utc).isoformat()

    logger.info("job_start", extra={"job_id": job_id, "run_id": run_id, "ts": now})

    robots = RobotsClient(user_agent=USER_AGENT, ttl_seconds=3600)
    throttle = HostThrottle(min_delay_seconds=1.0)
    collector = HttpCollector(user_agent=USER_AGENT, robots=robots, throttle=throttle)

    targets = [
        ("python_docs", "https://docs.python.org/3/", WikipediaExtractor()),

        ("hackernews", "https://news.ycombinator.com/", HackerNewsExtractor()),
        ("arxiv", "https://arxiv.org/list/cs.AI/recent", ArxivExtractor()),
    ]

    with SessionLocal() as db:
        for source, url, extractor in targets:
            pipeline = CrawlPipeline(db=db, collector=collector, extractor=extractor)
            result = pipeline.run(job_id=job_id, run_id=run_id, source=source, start_url=url)
            logger.info("job_target_result", extra={"job_id": job_id, "run_id": run_id, "source": source, "url": url, "result": result})

    finished = datetime.now(timezone.utc).isoformat()
    logger.info("job_end", extra={"job_id": job_id, "run_id": run_id, "ts": finished})