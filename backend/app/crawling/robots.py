import time
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser


class RobotsClient:
    """
    Caches robots.txt per host for TTL seconds.
    """
    def __init__(self, user_agent: str, ttl_seconds: int = 3600):
        self.user_agent = user_agent
        self.ttl_seconds = ttl_seconds
        self._cache: dict[str, tuple[float, RobotFileParser]] = {}

    def can_fetch(self, url: str) -> bool:
        parsed = urlparse(url)
        base = f"{parsed.scheme}://{parsed.netloc}"
        rp = self._get_parser(base)
        return rp.can_fetch(self.user_agent, url)

    def _get_parser(self, base: str) -> RobotFileParser:
        now = time.time()
        cached = self._cache.get(base)
        if cached and (now - cached[0]) < self.ttl_seconds:
            return cached[1]

        rp = RobotFileParser()
        rp.set_url(f"{base}/robots.txt")
        try:
            rp.read()
        except Exception:
            # If robots.txt fetch fails, default to "allowed" for MVP.
            # (You can flip this to "deny" if you want stricter behavior.)
            rp.parse([])
        self._cache[base] = (now, rp)
        return rp