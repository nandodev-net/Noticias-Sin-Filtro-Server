"""
    Data scheme for La Patilla
    https://www.lapatilla.com
"""

from app.scraper.scrapers.base_scraped_data import BaseScrapedData

class LaPatillaScrapedData(BaseScrapedData):
    """
        Scrapable data from la patilla
    """

    # I know it's empty, this is intended to be used when you 
    # can get more data from the site than the specified in 
    # ArticleHeadline model. You can safely scrape it without breaking anything