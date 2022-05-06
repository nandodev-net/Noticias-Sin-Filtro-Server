"""
    Manage feed building
"""

# Local imports 
from app.scraper.models import ArticleHeadline, ArticleCategory, MediaSite

# Python imports 
from typing import Dict, List, Optional, Any
import dataclasses

@dataclasses.dataclass
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

    @property
    def as_dict(self) -> Dict[str, Any]:
        """
            return a dict representation for this object
        """
        return dataclasses.asdict(self)

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
        return FeedContent(self.select_featured(amount_featured, feedback or Feedback([], [])), [])

    def select_featured(self, amount_featured : int, feedback : Feedback) -> List[ArticleHeadline]:
        """
            Return main featured headlines according to the rules 
        """

        # First level of relevance: Editors choice and relevance
        query = list(ArticleHeadline.objects.all().order_by('-editors_choice',  '-datetime')[:amount_featured])

        # Count currently added instances
        added = len(query)
        if added < amount_featured:
            # If no enough querys yet, fill with headlines with featured categories
            featured_categories = ArticleCategory.objects.all().filter(editors_choice=True)
            query.extend(
                list(
                    ArticleHeadline.objects.all()
                    .filter(category__in=featured_categories)
                    .exclude(id__in=[x.id for x in query])
                    .order_by('-datetime')
                    [:amount_featured - added]
                    )
                )

            added = len(query)
        
        # If not enough, fill with prefered categories
        if added < amount_featured:
            query.extend(
                list(
                    ArticleHeadline.objects.all()
                    .filter(category__in=feedback.prefered_categories)
                    .exclude(id__in=[x.id for x in query])
                    .order_by('-datetime')
                    [:amount_featured - added]
                    )
                )
            added = len(query)
        
        # If not enough, fill with prefered media sites
        if added < amount_featured:
            query.extend(
                list(
                    ArticleHeadline.objects.all()
                    .filter(source__in=feedback.prefered_media)
                    .exclude(id__in=[x.id for x in query])
                    .order_by('-datetime')
                    [:amount_featured - added]
                    )
                )
            added = len(query)

        # If not enough, add any
        if added < amount_featured:
            query.extend(
                list(
                    ArticleHeadline.objects.all()
                    .exclude(id__in=[x.id for x in query])
                    .order_by('-datetime')
                    [:amount_featured - added]
                    )
                )
        # TODO complete query when it requires more headlines
        return query
        
    def select_sections(self, categories_sections : Optional[List[ArticleCategory]] = None, feedback : Optional[Feedback] = None) -> List[Section]:
        """
            Return the sections corresponding to the specified categories
        """
        # TODO
        return []
