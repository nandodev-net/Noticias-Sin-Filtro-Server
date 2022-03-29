"""
    Scraped data specific for efecto cocuyo
"""
# Python imports
from typing import List

# Local imports
from vsf_crawler.data_schemes.base_scraped_data import BaseDataScheme

class EfectoCocuyoScrapedData(BaseDataScheme):
    """
        Data scheme for la patilla
    """
    
    def _map_categories(self, categories: List[str]) -> List[str]:

        to_lowecase = lambda s: ' '.join([sub.capitalize() for sub in s.lower().split() if sub])
        return [to_lowecase(cat) for cat in categories]
