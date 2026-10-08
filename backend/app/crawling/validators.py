"""Pure validators. They transform or reject; they never fetch data."""


def normalize_title(raw: str) -> str:
    """Collapse runs of whitespace and trim the ends."""
    return " ".join(raw.split())
