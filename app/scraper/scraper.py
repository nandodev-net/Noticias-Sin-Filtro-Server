"""
    The scraper module will encapsulate all the scraping pipeline
"""
# Python imports
from typing import List
from urllib.parse import urlparse

from scrapyd_api import ScrapydAPI

# Local imports
from app.scraper.models import ArticleHeadline

class Scraper:
    """
        Manage all scraping operations
    """

    scraper_to_main_page = {
        ArticleHeadline.Source.LA_PATILLA.value : "https://www.lapatilla.com",
        ArticleHeadline.Source.EFECTO_COCUYO.value : "https://efectococuyo.com"
    }

    scrapy_project_name = "default"
    scrapy_crawler_name = "la_patilla"

    def __init__(self, scrapyd : ScrapydAPI):
        self._scrapyd = scrapyd        

    def scrape(self, scraper_names : List[str]) -> List[int]:
        """
            Triger a scraping for the specified  list of scrapers
            # Parameters
                * scraper_names : `[str]` = list scrapers to trigger a scraping
        """

        # Sanity check scrapers
        invalid_names = [name for name in scraper_names if name not in self._valid_scrapers()]
        if invalid_names:
            raise ValueError(f"The following scrapers are not valid scrapers: {invalid_names}. Choices are: {self._valid_scrapers()}")

        print(self.scraper_to_main_page)

        # Get url for this scraper
        urls = [self.scraper_to_main_page[x] for x in scraper_names] # type: ignore

        # Config settings
        settings = {
            'USER_AGENT': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
        }

        # Parse domain 
        domains = [urlparse(url).netloc for url in urls]

        tasks = [
            self._scrapyd.schedule(
                self.scrapy_project_name, 
                self.scrapy_crawler_name, 
                url=url, domain=domain, 
                settings=settings)
            for (url, domain) in zip(urls, domains)
        ]

        return tasks
    
    @staticmethod
    def _valid_scrapers() -> List[str]:
        """
            Returns a list with valid scrapers names as strings
        """
        return ArticleHeadline.Source.values