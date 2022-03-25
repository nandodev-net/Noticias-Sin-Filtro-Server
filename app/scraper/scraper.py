"""
    The scraper module will encapsulate all the scraping pipeline
"""
# Python imports
from typing import List
from urllib.parse import urlparse

from scrapyd_api import ScrapydAPI

# Local imports
from app.scraper.models import ArticleHeadline
import noticias_sin_filtro_server.settings as settings

scrapyd = ScrapydAPI(
    f"http://{settings.SCRAPY_HOST}:{settings.SCRAPY_PORT}"
)  # TODO move to environment variable


class Scraper:
    """
    Manage all scraping operations
    """

    scraper_to_main_page = {
        ArticleHeadline.Source.LA_PATILLA.value: "https://www.lapatilla.com",
        ArticleHeadline.Source.EFECTO_COCUYO.value: "https://efectococuyo.com",
    }

    scrapy_project_name = "default"

    def __init__(self, scrapyd: ScrapydAPI = scrapyd):
        self._scrapyd = scrapyd

    def scrape(self, scraper_names: List[str]) -> List[int]:
        """
        Triger a scraping for the specified  list of scrapers
        # Parameters
            * scraper_names : `[str]` = list scrapers to trigger a scraping
        """

        # If nothing to do, just end
        if not scraper_names:
            return []

        # Sanity check scrapers
        invalid_names = [
            name for name in scraper_names if name not in self._valid_scrapers()
        ]
        if invalid_names:
            raise ValueError(
                f"The following scrapers are not valid scrapers: {invalid_names}. Choices are: {self._valid_scrapers()}"
            )

        # Config settings
        settings = {
            "USER_AGENT": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
        }

        # Parse domain
        tasks = []
        for scraper_name in scraper_names:
            url = self.scraper_to_main_page[scraper_name]  # type: ignore
            domain = urlparse(url).netloc

            settings["source"] = scraper_name

            tasks.append(
                self._scrapyd.schedule(
                    self.scrapy_project_name,
                    scraper_name,
                    url=url,
                    domain=domain,
                    settings=settings,
                )
            )

        return tasks

    @staticmethod
    def _valid_scrapers() -> List[str]:
        """
        Returns a list with valid scrapers names as strings
        """
        return ArticleHeadline.Source.values
