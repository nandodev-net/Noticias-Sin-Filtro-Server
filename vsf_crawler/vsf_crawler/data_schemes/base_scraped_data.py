"""
    Base class for scraped data schemes. Every scheme should inherit this class
"""

# Local imports 
from sre_parse import CATEGORIES
from app.scraper.models import ArticleCategory, ArticleHeadline

# Python imports
import dataclasses
from typing import List, Tuple
import datetime

# Note that the use of dataclasses here is not optional since 
# scrapy requires to have an Item-like interface, which is provided 
# by using dataclasses: https://docs.scrapy.org/en/latest/topics/items.html#dataclass-objects
@dataclasses.dataclass
class BaseDataScheme:
    """
        Every data scheme should inherit this class 
        and implement the corresponding function to map to the canonical
        data type, the `as_headline` function
    """
    title : str 
    excerpt : str
    url : str
    date : str
    # image url
    img : str
    source : str
    scraped_date : datetime.datetime
    categories : List[str] = dataclasses.field(default_factory=list)

    def as_headline(self) -> Tuple[ArticleHeadline, List[ArticleCategory]]:
        """
            Convert from this specific data scheme to an article headline object
            # Returns
                An `ArticleHeadline` object correctly mapped. For example, if there's a canonical 
                category called 'Nacionales' but such category is called 'nacional' for this site,
                then the resulting object will have the category correctly named as 'Nacionales'. 
                The same applies to every data field.
        """
        categories = [
                ArticleCategory.objects.get_or_create(name=category_name)[0]
                for category_name in self._map_categories(self.categories) 
            ]
            
        headline = ArticleHeadline(
            title   = self.title,
            excerpt = self.excerpt,
            url     = self.url,
            date    = None, # TODO Still don't know how to map dates in this site 
            scraped_date = self.scraped_date,
            source  = self.source 
        )
        
        return headline, categories
    
    def _map_categories(self, categories : List[str]) -> List[str]:
        """
            Override this function to modify how categories are mapped in your specific site
        """

        return categories