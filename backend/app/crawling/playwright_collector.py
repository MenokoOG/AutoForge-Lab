"""
PlaywrightCollector

Pro Tip:
Use browser collectors when:
- content is JS-rendered
- API endpoints are hidden
- DOM mutations occur after load

This collector is optional and lazy-imports Playwright so the
core stack works without browser deps installed.
"""

from __future__ import annotations

from typing import Optional

from app.crawling.base import CollectorResult, BaseCollector


class PlaywrightCollector(BaseCollector):
    name = "playwright"

    async def collect(self, url: str) -> CollectorResult:
        try:
            from playwright.async_api import async_playwright
        except ImportError as e:
            raise RuntimeError(
                "Playwright not installed. Install with: pip install '.[browser]'"
            ) from e

        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()

            # Pro Tip: always set timeouts for automation
            await page.goto(url, timeout=30_000)
            content = await page.content()

            status = page.response.status if page.response else 200

            await browser.close()

        return CollectorResult(
            url=url,
            status_code=status,
            content=content,
            headers={},
        )