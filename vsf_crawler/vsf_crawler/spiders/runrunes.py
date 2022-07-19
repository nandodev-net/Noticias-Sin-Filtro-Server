"""
    Scraper for runrun.es:
    https://runrun.es
"""
# Local imports
from typing import Iterable
from vsf_crawler.data_schemes.runrunes_scraped_data import RunRunesScrapedData
from app.scraper.models import MediaSite

# Third party imports
from scrapy import Spider
from scrapy.http import Response
import bs4

# Python imports
import logging
import datetime
from pytz import utc

# DEBUG ONLY ------------
import logging
handler = logging.FileHandler("somefile.txt")
logger = logging.getLogger()
logger.addHandler(handler)
# -----------------------

class RunRunes(Spider):
    name = MediaSite.Scrapers.RUNRUNES.value #type: ignore
    allowed_domains = ['runrun.es']
    start_urls = ['https://runrun.es/feed/']

    def parse(self, response : Response) -> Iterable[RunRunesScrapedData]:
        """
            Specifically made to parse "runrunes" rss feed
        """
        assert self.name, "Spider missconfigured"

        posts = response.xpath("//channel/item")
        for item in posts: # type: ignore

            try: # type: ignore
                descript = item.xpath('description//text()').extract_first()
                descript_soup = bs4.BeautifulSoup(descript)
                excerpt = descript_soup.find("p").getText() # type: ignore
                # img = descript_soup.find("img")['src'] # type: ignore
                title  = item.xpath('title//text()').extract_first(),
                url = item.xpath('link//text()').extract_first(),
                date  = item.xpath('pubDate//text()').extract_first(),
                author  = item.xpath('creator//text()').extract_first(),
                categories  = item.xpath('category//text()').extract()

                print(excerpt)
                print(title)
                print(url)
                print(date)
                print(author)
                print(categories)

                item = RunRunesScrapedData(
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
            except Exception as e:
                logging.error(f"Error creating new item from response: {str(e)}")
            yield item        
