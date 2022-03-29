"""
    Spider to scrape  efecto cocuyo: https://efectococuyo.com
"""
# Local imports
from typing import Iterable
from vsf_crawler.data_schemes.efecto_cocuyo_scraped_data import EfectoCocuyoScrapedData
from app.scraper.models import ArticleHeadline

# Third party imports
from scrapy import Spider
from scrapy.http import Response

# Python imports
import logging
import datetime
from pytz import utc

class EfectoCocuyoSpider(Spider):
    name = ArticleHeadline.Source.EFECTO_COCUYO.value #type: ignore
    allowed_domains = ['https://efectococuyo.com']
    start_urls = ['https://efectococuyo.com']

    def parse(self, response : Response) -> Iterable[EfectoCocuyoScrapedData]:
        """
            Specifically made to parse "efecto cocuyo" main page
        """
        assert self.name, "Spider missconfigured"
        thumbnails = response.css(".box1")

        
        for thumbnail in thumbnails: # type: ignore
            try: # type: ignore
                category = thumbnail.css(".contentbox > h3 > .green ::text").get()
                date = thumbnail.css(".contentbox > h3  ").get().partition('·')[2].partition("<span")[0].strip()
                title = thumbnail.css(".contentbox > a > p ::text").get()
                excerpt = None
                
                # Parse url
                url = thumbnail.css(".contentbox > a::attr(href)").extract()
                url = url[0] if url else url

                # Parse img url
                img = thumbnail.css("::attr(style)").extract()
                if img:
                    img = img[0].partition("url('")[2].partition("');")[0]

                item = EfectoCocuyoScrapedData(
                    title=title, 
                    excerpt=excerpt, #type: ignore
                    url=url,
                    date=date,
                    scraped_date=datetime.datetime.now(tz=utc),
                    categories=[category],
                    img = img, 
                    source=self.name, #type: ignore
                    relevance = False
                    )
            except Exception as e:
                print(f"Error creating new item from response: {str(e)}")
                logging.error(f"Error creating new item from response: {str(e)}")
            yield item        
