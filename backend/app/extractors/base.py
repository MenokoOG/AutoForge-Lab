from app.schemas.crawl import CrawlRecordIn


class BaseExtractor:
    def extract(self, *, source: str, url: str, html: str) -> list[CrawlRecordIn]:
        raise NotImplementedError