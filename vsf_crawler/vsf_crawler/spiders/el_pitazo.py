"""
    Spider to scrape data from the main feed from el pitazo
    https://elpitazo.net
"""
# Local imports
from asyncio.log import logger
from typing import Iterable

from requests import head
from vsf_crawler.data_schemes.el_pitazo_scraped_data import ElPitazoScrapedData
from app.scraper.models import MediaSite

# Third party imports
from scrapy import Spider
from scrapy.http import Response

# Python imports
import logging
import datetime
from pytz import utc
import bs4

# DEBUG ONLY ------------
import logging
handler = logging.FileHandler("somefile.txt")
logger = logging.getLogger()
logger.addHandler(handler)
# -----------------------

class ElPitazoSpider(Spider):
    name = MediaSite.Scrapers.EL_PITAZO.value #type: ignore
    allowed_domains = ['elpitazo.net']
    start_urls = ['https://elpitazo.net/feed']

    def parse(self, response : Response) -> Iterable[ElPitazoScrapedData]:
        """
            Specifically made to parse "la patilla" main page
        """
        logger.info(f"IM STARTING TO PARSE RESPONSE {response}")
        assert self.name, "Spider missconfigured"
        posts = response.xpath("//channel/item")
        for item in posts: # type: ignore

            try: # type: ignore
                descript = item.xpath('description//text()').extract_first()
                descript_soup = bs4.BeautifulSoup(descript)
                excerpt = descript_soup.find("p").getText() # type: ignore
                # img = descript_soup.find("img") # type: ignore
                title  = item.xpath('title//text()').extract_first(),
                url = item.xpath('link//text()').extract_first(),
                date  = item.xpath('pubDate//text()').extract_first(),
                author  = item.xpath('creator//text()').extract_first(),
                categories  = list(item.xpath('category//text()').extract())

                print(excerpt)
                print(title[0])
                print(url[0])
                print(date[0])
                print(author[0])
                print(categories)

                item = ElPitazoScrapedData(
                    title=title[0], 
                    excerpt=excerpt, 
                    url=url[0],
                    date=date[0],
                    scraped_date=datetime.datetime.now(tz=utc),
                    categories=categories, 
                    img = None, #type: ignore
                    scraper=self.name, #type: ignore
                    relevance = False
                    )
                logger.info(f"Saving item: {item}")
            except Exception as e:
                logging.error(f"Error creating new item from response: {str(e)}")
            yield item        

    def start_requests(self):

        headers = {
            "Accept": "text/html, */*; q=0.01",
            "Referer" : None,
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36 OPR/84.0.4316.31"
        }
        for r in super().start_requests():
            for (k, v) in headers.items():
                r.headers[k] = v            
            yield r