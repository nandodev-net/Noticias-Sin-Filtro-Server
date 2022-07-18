"""
    Spider to scrape data from the main feed from el pitazo
    https://elpitazo.net
"""
# Local imports
from asyncio.log import logger
from typing import Iterable
from vsf_crawler.data_schemes.la_patilla_scraped_data import LaPatillaScrapedData
from app.scraper.models import MediaSite

# Third party imports
from scrapy import Spider
from scrapy.http import Response

# Python imports
import logging
import datetime
from pytz import utc

# DEBUG ONLY ------------
# import logging
# handler = logging.FileHandler("somefile.txt")
# logger = logging.getLogger()
# logger.addHandler(handler)
# -----------------------

class ElPitazoSpider(Spider):
    name = MediaSite.Scrapers.EL_PITAZO.value #type: ignore
    allowed_domains = ['https://elpitazo.net']
    start_urls = ['https://elpitazo.net/feed/']


    def parse(self, response : Response) -> Iterable[LaPatillaScrapedData]:
        """
            Specifically made to parse "la patilla" main page
        """
        assert self.name, "Spider missconfigured"
        thumbnails = response.css(".homenews-container > .row > div")

        for thumbnail in thumbnails: # type: ignore
            try: # type: ignore
                category = thumbnail.css("div > .cat-name-time > .cat-name ::text").get()
                date = thumbnail.css("div > .cat-name-time > .post-date ::text").get().strip()
                title = thumbnail.css("div > .post-title > a > h4 ::text").get()
                excerpt = thumbnail.css("div > .home-post-excerpt ::text").get().strip()
                
                # Parse url
                url = thumbnail.css("div > .post-img-sec > a::attr(href)").extract()
                url = url[0] if url else url

                # Parse img url
                img = thumbnail.css("div > .post-img-sec > .post-thumbnail > img::attr(src)").extract()
                img = img[0] if img else img

                item = LaPatillaScrapedData(
                    title=title, 
                    excerpt=excerpt, 
                    url=url,
                    date=date,
                    scraped_date=datetime.datetime.now(tz=utc),
                    categories=[category],
                    img = img, 
                    scraper=self.name, #type: ignore
                    relevance = category == 'Destacados'
                    )
            except Exception as e:
                logging.error(f"Error creating new item from response: {str(e)}")
            yield item        
