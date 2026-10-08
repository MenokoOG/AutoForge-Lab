from bs4 import BeautifulSoup

from app.extractors.base import BaseExtractor
from app.schemas.crawl import CrawlRecordIn


class WikipediaExtractor(BaseExtractor):
    def extract(self, *, source: str, url: str, html: str) -> list[CrawlRecordIn]:
        soup = BeautifulSoup(html, "lxml")
        title = soup.title.get_text(strip=True) if soup.title else "Untitled"
        return [
            CrawlRecordIn(
                source=source,
                title=title,
                url=url,
                tags=["wikipedia", "education"],
            )
        ]