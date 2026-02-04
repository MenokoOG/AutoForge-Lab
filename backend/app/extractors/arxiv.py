from bs4 import BeautifulSoup
from app.schemas.crawl import CrawlRecordIn
from app.extractors.base import BaseExtractor


class ArxivExtractor(BaseExtractor):
    def extract(self, *, source: str, url: str, html: str) -> list[CrawlRecordIn]:
        soup = BeautifulSoup(html, "lxml")
        items: list[CrawlRecordIn] = []

        # arXiv listings vary; keep MVP tolerant
        for dt in soup.select("dl > dt"):
            a = dt.select_one('a[href^="/abs/"]')
            if not a:
                continue
            href = a.get("href") or ""
            abs_url = f"https://arxiv.org{href}"
            title_el = dt.find_next("dd")
            title_text = ""
            if title_el:
                t = title_el.get_text(" ", strip=True)
                title_text = t[:512] if t else ""
            if not title_text:
                title_text = abs_url
            items.append(CrawlRecordIn(source=source, title=title_text, url=abs_url, tags=["arxiv", "research"]))

        if not items:
            page_title = soup.title.get_text(strip=True) if soup.title else "arXiv"
            items.append(CrawlRecordIn(source=source, title=page_title, url=url, tags=["arxiv"]))

        return items