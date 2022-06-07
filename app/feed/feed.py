"""
    Manage feed building
"""

# Local imports 
from audioop import add
from app.scraper.models import ArticleHeadline, ArticleCategory, MediaSite

# Python imports 
from typing import Dict, List, Optional, Any
import dataclasses
import datetime

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

        # Parameters
        - recent_limit : `int` = (optional) how many days to consider a new "recent". Defaults to 3 days ago.
        - feedback : `FeedBack` = (optional) extra information to deliver better recomendations
    """

    def __init__(self, feedback : Feedback, recent_limit : int = 3):
        assert recent_limit > 0, "Recent limit should be a positive number"
        self._recent_limit = recent_limit
        self._feedback = feedback

    @property
    def feedback(self) -> Feedback:
        """
            Additional information to deliver better recomendations
        """
        return self._feedback

    @property
    def recent_limit(self) -> int:
        """
            How many days in the past is considered "recent" for a new
        """
        return self._recent_limit

    def home(self, amount_featured : int = 3, instance_per_section : int = 4, amount_sections : int = 6, categories_sections : Optional[List[ArticleCategory]] = None, feedback : Optional[Feedback] = None) -> FeedContent:
        """
            Create home feed
        """

        return FeedContent(
            self.select_featured(amount_featured), 
            self.select_sections(amount_sections, categories_sections, feedback, instance_per_section)
        )

    def select_featured(self, amount_featured : int, feedback : Optional[Feedback] = None) -> List[ArticleHeadline]:
        """
            Return main featured headlines according to the rules 
        """
        feedback = feedback or self.feedback

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
        return query
        
    def select_sections(self, desired_sections : int, mandatory_categories : Optional[List[ArticleCategory]] = None, feedback : Optional[Feedback] = None, instance_per_section : int = 4) -> List[Section]:
        """
            Return the sections corresponding to the specified categories
        """

        # Get categories related to the sections
        categories = self.get_best_categories(desired_sections, mandatory_categories or [], feedback)
        
        # Construct sections based on categories
        return [self.select_section(x, max_headlines = instance_per_section, feedback=feedback) for x in categories]

    def select_section(self, section_category : ArticleCategory, max_headlines : int = 4, feedback : Optional[Feedback] = None) -> Section:
        """
            Return a section with the content of the specified category
        """
        feedback = feedback or self.feedback
        few_days_ago = datetime.datetime.now() - datetime.timedelta(days=self.recent_limit)


        # consider first headline
        headlines = list(
                ArticleHeadline.objects
                .all()
                .filter(
                    categories__in = [section_category], 
                    editors_choice=True,
                    datetime__gt = few_days_ago
                    )
                .order_by('-datetime')
            )[:max_headlines]

        added = len(headlines)

        # If not enough, fill it with non editors choice, but relevant
        if added < max_headlines:
            headlines.extend(list(
                    ArticleHeadline.objects
                    .all()
                    .filter(
                        categories__in = [section_category], 
                        relevance=True,
                        datetime__gt = few_days_ago
                    )
                    .exclude(id__in=[x.id for x in headlines])
                    .order_by('-datetime')
                )[:max_headlines - added]
            )

            added = len(headlines)
        
        # If not enough, fill it with regular news
        if added < max_headlines:
            headlines.extend(list(
                    ArticleHeadline.objects
                    .all()
                    .filter(
                        categories__in = [section_category],
                        )
                    .exclude(id__in=[x.id for x in headlines])
                    .order_by('-datetime')
                )[:max_headlines - added]
            )

            added = len(headlines)
        
        return Section(section_category.name, section_category, headlines)

    def get_best_categories(self, limit : int, mandatory_categories : List[ArticleCategory] = [], feedback : Optional[Feedback] = None) -> List[ArticleCategory]:
        """
            Select relevant categories based on feedback and other rules
            # Parameters
                - limit : `int` = How many categories to retrieve
                - mandatory_categories : `List[ArticleCategory]` = (optional) Categories that must be included
                - feedback : `Optional[Feedback]` = Possible feedback object used to retrieve the most interesting categories, provide it to override 
                        instance version.
            
            # Return 
                List of desired article category objects

        """
        assert limit > 0, "limit should be positive"

        feedback = feedback or self.feedback

        # Start by adding desired categories
        categories = mandatory_categories[:limit]
        categories.extend(feedback.prefered_categories[:limit - len(categories)])


        added = len(categories)

        # If not enough, add featured categories
        if added < limit:
            categories.extend(
                list(
                    ArticleCategory.objects
                    .all()
                    .filter(
                        editors_choice = True
                    )
                    .exclude(id__in = [x.id for x in categories]) # type: ignore
                    [:limit - added]
                )
            )

            added = len(categories)
        
        # If not enough, add any category
        if added < limit:
            categories.extend(
                list(
                    ArticleCategory.objects
                    .all()
                    .exclude(id__in = [x.id for x in categories]) # type: ignore
                )
            )


        return categories