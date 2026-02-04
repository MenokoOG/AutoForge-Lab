import pytest
from app.schemas.crawl import CrawlRecordIn


def test_tag_validation_kebab_case():
    with pytest.raises(ValueError):
        CrawlRecordIn(source="x", title="t", url="https://example.com", tags=["BadTag"])


def test_url_validation():
    with pytest.raises(ValueError):
        CrawlRecordIn(source="x", title="t", url="ftp://example.com", tags=["ok"])