import time
from urllib.parse import urlparse


class HostThrottle:
    """
    Simple per-host throttle: minimum delay between requests to same host.
    """

    def __init__(self, min_delay_seconds: float = 1.0):
        self.min_delay_seconds = float(min_delay_seconds)
        self._last_request: dict[str, float] = {}

    def wait(self, url: str) -> None:
        host = urlparse(url).netloc
        now = time.time()
        last = self._last_request.get(host, 0.0)
        elapsed = now - last

        if elapsed < self.min_delay_seconds:
            time.sleep(self.min_delay_seconds - elapsed)

        self._last_request[host] = time.time()
