from bs4 import BeautifulSoup
from app.schemas.crawl import CrawlRecordIn
from app.extractors.base import BaseExtractor


class HackerNewsExtractor(BaseExtractor):
    def extract(self, *, source: str, url: str, html: str) -> list[CrawlRecordIn]:
        soup = BeautifulSoup(html, "lxml")

        # HN markup can change; keep extraction tolerant
        items: list[CrawlRecordIn] = []
        for a in soup.select("span.titleline > a"):
            href = a.get("href") or ""
            title = a.get_text(strip=True) or "Untitled"
            if href.startswith("item?id="):
                href = f"https://news.ycombinator.com/{href}"
            if href.startswith("http"):
                items.append(
                    CrawlRecordIn(
                        source=source,
                        title=title[:512],
                        url=href[:2048],
                        tags=["hackernews", "tech"],
                    )
                )

        # If parsing fails, at least store the page title
        if not items:
            page_title = soup.title.get_text(strip=True) if soup.title else "Hacker News"
            items.append(CrawlRecordIn(source=source, title=page_title, url=url, tags=["hackernews"]))

        return items