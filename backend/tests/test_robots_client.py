from app.crawling.robots import RobotsClient


def test_robots_client_can_fetch_returns_bool():
    rc = RobotsClient(user_agent="test-bot", ttl_seconds=1)
    # We don't rely on network correctness in tests; just ensure type + no crash
    ok = rc.can_fetch("https://example.com/")
    assert isinstance(ok, bool)