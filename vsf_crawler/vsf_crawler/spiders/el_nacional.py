"""
    Scraper for main feed in El Nacional:
        https://www.elnacional.com
"""

# Local imports
from typing import Iterable
from vsf_crawler.data_schemes.el_nacional_scraped_data import ElNacionalScrapedData
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

class ElNacional(Spider):
    name = MediaSite.Scrapers.EL_NACIONAL.value #type: ignore
    allowed_domains = ['www.elnacional.com']
    start_urls = ['https://www.elnacional.com/feed/']


    def parse(self, response : Response) -> Iterable[ElNacionalScrapedData]:
        """
            Specifically made to parse "la patilla" main page
        """
        assert self.name, "Spider missconfigured"
        assert False, "Scraper incompleto"
        posts = response.xpath("//channel/item")

        for item in posts: # type: ignore
            post = {
                'title' : item.xpath('title//text()').extract_first(),
                'link': item.xpath('link//text()').extract_first(),
                'pubDate' : item.xpath('pubDate//text()').extract_first(),
            }
            print(post)



        return 
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

                item = ElNacionalScrapedData(
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
