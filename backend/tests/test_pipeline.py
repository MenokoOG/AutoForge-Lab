from app.crawling.validators import normalize_title


def test_title_normalization():
    raw = "   Example   Title   "
    clean = normalize_title(raw)
    assert clean == "Example Title"