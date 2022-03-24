"""
    Scraped data specific for la patilla
"""
# Python imports
from typing import List, Tuple

# Local imports
from vsf_crawler.data_schemes.base_scraped_data import BaseDataScheme
from app.scraper.models import ArticleHeadline, ArticleCategory

class LaPatillaScrapedData(BaseDataScheme):
    """
        Data scheme for la patilla
    """
    
    