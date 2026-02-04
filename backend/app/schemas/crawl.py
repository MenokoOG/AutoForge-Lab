from pydantic import BaseModel, Field, field_validator
from datetime import datetime, timezone
import re


URL_RE = re.compile(r"^https?://[^\s]+$")


class CrawlRecordIn(BaseModel):
    source: str = Field(min_length=1, max_length=64)
    title: str = Field(min_length=1, max_length=512)
    url: str = Field(min_length=8, max_length=2048)
    tags: list[str] = Field(default_factory=list)
    fetched_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    @field_validator("url")
    @classmethod
    def validate_url(cls, v: str) -> str:
        if not URL_RE.fullmatch(v):
            raise ValueError("url must be http(s)://")
        return v

    @field_validator("tags")
    @classmethod
    def validate_tags(cls, v: list[str]) -> list[str]:
        # keep tags simple + safe
        for t in v:
            if len(t) > 32:
                raise ValueError("tag too long")
            if not re.fullmatch(r"[a-z0-9][a-z0-9\-]{0,31}", t):
                raise ValueError("tag must be kebab-case")
        return v


class CrawlRecordOut(BaseModel):
    id: int
    source: str
    title: str
    url: str
    tags: list[str]
    fetched_at: str
    content_hash: str