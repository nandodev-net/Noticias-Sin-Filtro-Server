"""
    Manage feed building
"""

# Local imports 
from app.scraper.models import ArticleHeadline, ArticleCategory, MediaSite

# Python imports 
from typing import List, Optional
import dataclasses

class Section:
    """
        Represents a subsection in the main fead
    """

    # Human readable name 
    name        : str 

    # A section might be a set of news dedicated to a single media site, 
    # a single category, or both
    category    : Optional[ArticleCategory]

    # Actual headlines to show in this section
    news        : List[ArticleHeadline]

    # Coming soon: link to main feed for this section
    link_to_see_more : str

@dataclasses.dataclass
class FeedContent:
    """
        Represents the content delivered as the feed
    """

    # Main news featured in the headline 
    featured : List[ArticleHeadline]

    # Additional sections 
    sections : List[Section]

@dataclasses.dataclass
class Feedback:
    """
        Information required to compute the home
    """

    prefered_categories : List[ArticleCategory]
    prefered_media : List[MediaSite]

class Feed:
    """
        Manage feed building
    """

    def __init__(self):
        pass

    def home(self, amount_featured : int = 3, instance_per_section : int = 4, categories_sections : Optional[List[ArticleCategory]] = None, feedback : Optional[Feedback] = None) -> FeedContent:
        """
            Create home feed
        """
        # TODO
        return FeedContent([], [])

    def select_featured(self, amount_featured : int, feedback : Feedback) -> List[ArticleHeadline]:
        """
            Return main featured headlines according to the rules 
        """
        # TODO
        return []
        
    def select_sections(self, categories_sections : Optional[List[ArticleCategory]] = None, feedback : Optional[Feedback] = None) -> List[Section]:
        """
            Return the sections corresponding to the specified categories
        """
        # TODO
        return []
