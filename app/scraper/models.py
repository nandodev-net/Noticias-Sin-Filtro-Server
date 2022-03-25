"""
    This models.py file will contain the canonical data that will be actually stored in DB. 
    Every site scraper should produce an item that can be mapped to an object instance of 
    this model.
"""

# Django imports
from django.db import models


class ArticleCategory(models.Model):
    """
    A category to classify articles
    """

    # Category actual value
    name = models.CharField(
        verbose_name="Category name", null=False, unique=True, max_length=200
    )

    def __str__(self) -> str:
        return self.name


class ArticleHeadline(models.Model):
    """
    Represents a "headline" in the main feed for a news page
    """

    class Source(models.TextChoices):
        """
        Possible sources of information, such like lapatilla, efectococuyo
        """

        LA_PATILLA = ("la_patilla", "La Patilla")
        EFECTO_COCUYO = ("efecto_cocuyo", "Efecto cocuyo")
        UNKNOWN = ("unknown", "unknown")

    # Article title
    title = models.TextField(verbose_name="Title", null=False, max_length=200)

    # Publication date
    datetime = models.DateTimeField(verbose_name="Publication name", null=True)

    # Possible categories
    categories = models.ManyToManyField(to=ArticleCategory)

    # Possible summary for the new provided by the site
    excerpt = models.TextField(default="Excerpt", null=True, max_length=300)

    # Main image for this headline
    image_url = models.URLField(verbose_name="Image source", max_length=300)

    # Scraped date
    scraped_date = models.DateTimeField(
        verbose_name="Scraped date", null=False, auto_created=True, auto_now_add=True
    )

    # Where did this heading come from
    source = models.CharField(
        max_length=100, choices=Source.choices, default=Source.UNKNOWN
    )

    # Url to the actual article
    url = models.URLField(verbose_name="Full article url", max_length=300, unique=True)

    # If this article was relevant in its original site
    relevance = models.BooleanField(verbose_name="Relevance", default=None, null=True)

    @property
    def as_dict(self):
        """
        Easily convert to dict
        """
        return {
            "title": self.title,
            "date": self.datetime,
            "categories": self.categories,
            "excerpt": self.excerpt,
            "image": self.image_url,
            "scraped_date": self.scraped_date,
            "source": self.source,
        }

    def __str__(self) -> str:
        return f"Article(title = {self.title}, source = {self.source}, scraped_date = {self.scraped_date})"
