"""
    Provides a base abstract class for scraped data classes for every site
"""

# Local imports
from app.scraper.models import ArticleHeadline

# Python imports
import dataclasses
import datetime
from typing import List, Any

@dataclasses.dataclass
class BaseScrapedData:
    """
        Base class for scraped data schems
    """
    title : str 
    date : str
    excerpt : str 
    image : Any 
    scraped_date : datetime.datetime
    source = str
    url : str
    categories : List[str] = dataclasses.field(default_factory=list)

    @property
    def as_headline(self) -> ArticleHeadline:
        """
            Convert this scraped data into a canonical model
        """
        return ArticleHeadline(
                    title=self.title,
                    date=self.date,
                    excerpt=self.excerpt,
                    image=self.image,
                    scraped_date=self.scraped_date,
                    url=self.url,
                    source=self.source,
                    categories=self.categories
                )

