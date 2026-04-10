"""
SeleniumCollector

Pro Tip:
Selenium is heavier but useful when:
- you need real browser profiles
- anti-bot measures block headless fetch
"""

from __future__ import annotations

from app.crawling.base import CollectorResult, BaseCollector


class SeleniumCollector(BaseCollector):
    name = "selenium"

    def collect(self, url: str) -> CollectorResult:
        try:
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options
        except ImportError as e:
            raise RuntimeError(
                "Selenium not installed. Install with: pip install '.[browser]'"
            ) from e

        opts = Options()
        opts.add_argument("--headless=new")

        driver = webdriver.Chrome(options=opts)

        try:
            driver.get(url)
            html = driver.page_source
        finally:
            driver.quit()

        return CollectorResult(
            url=url,
            status_code=200,
            content=html,
            headers={},
        )