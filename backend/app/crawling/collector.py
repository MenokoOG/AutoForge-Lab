from dataclasses import dataclass
from urllib.parse import urlparse
import time
import httpx

from app.crawling.robots import RobotsClient
from app.crawling.throttle import HostThrottle


class CrawlBlockedByRobots(Exception):
    pass


@dataclass
class FetchResult:
    url: str
    host: str
    status_code: int
    duration_ms: int
    robots_allowed: bool
    text: str


class BaseCollector:
    def fetch(self, url: str) -> FetchResult:
        raise NotImplementedError


class HttpCollector(BaseCollector):
    def __init__(
        self,
        *,
        user_agent: str,
        robots: RobotsClient,
        throttle: HostThrottle,
        timeout_seconds: float = 15.0,
    ):
        self.user_agent = user_agent
        self.robots = robots
        self.throttle = throttle
        self.timeout_seconds = timeout_seconds
        self._client = httpx.Client(timeout=timeout_seconds, follow_redirects=True)

    def fetch(self, url: str) -> FetchResult:
        self.throttle.wait(url)

        allowed = self.robots.can_fetch(url)
        host = urlparse(url).netloc
        if not allowed:
            raise CrawlBlockedByRobots(f"Blocked by robots.txt: {url}")

        start = time.perf_counter()
        r = self._client.get(url, headers={"User-Agent": self.user_agent})
        duration_ms = int((time.perf_counter() - start) * 1000)

        return FetchResult(
            url=url,
            host=host,
            status_code=r.status_code,
            duration_ms=duration_ms,
            robots_allowed=True,
            text=r.text,
        )