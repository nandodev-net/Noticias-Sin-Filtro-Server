"""
    This models.py file will contain the canonical data that will be actually stored in DB. 
    Every site scraper should produce an item that can be mapped to an object instance of 
    this model.
"""

# python imports
import datetime
import pytz

# Django imports
from email.policy import default
from django.db import models

# Third party imports
from colorfield.fields import ColorField

class ArticleCategory(models.Model):
    """
    A category to classify articles
    """

    # Category actual value
    name = models.CharField(
        verbose_name="Category name", null=False, unique=True, max_length=200
    )

    # Category color 
    color = ColorField(default = '#808080', verbose_name = "Color")

    def __str__(self) -> str:
        return self.name

class MediaSite(models.Model):
    """
        Represents a media site information
    """
    class Scrapers(models.TextChoices):
        """
        Possible sources of information, such like lapatilla, efectococuyo
        """
        LA_PATILLA = ("la_patilla", "La Patilla")
        EFECTO_COCUYO = ("efecto_cocuyo", "Efecto cocuyo")
        EL_NACIONAL = ("el_nacional", "El Nacional")
        CRONICA_UNO = ("cronica_uno", "Crónica Uno")
        

    human_name = models.TextField(verbose_name='Site name (human readable)', null=False, max_length=100)
    scraper = models.CharField(
                    verbose_name='Scraper (its identifier)', 
                    choices=Scrapers.choices, 
                    null=False, 
                    max_length=100, 
                )
    site_url = models.URLField(verbose_name="Site url", null=False, max_length=300)
    name = models.TextField(verbose_name="Site name", null=False, max_length=100, unique=True)
    site_url_image = models.URLField(verbose_name="Site image", null=True, max_length=300)

    # If this scraper is currently active
    scraping_active = models.BooleanField(verbose_name="Scraping active", null=False, default=True)

    # how often we scrape
    scraping_frequency_mins = models.IntegerField(verbose_name="Scraping frequency (minutes)", default=5, null=False)

    # Last time this site was scraped
    last_scraped = models.DateTimeField(verbose_name="Last time scraped", default=datetime.datetime(1970, 1, 1, 0, 0, tzinfo=pytz.utc))

    def __str__(self) -> str:
        return self.human_name

class ArticleHeadline(models.Model):
    """
    Represents a "headline" in the main feed for a news page
    """

    class Source(models.TextChoices):
        """
        Possible sources of information, such like la patilla, efecto cocuyo
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
    source = models.ForeignKey(to=MediaSite, on_delete=models.SET_NULL, null=True)

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
            "source": self.source.human_name, # type: ignore
        }

    def __str__(self) -> str:
        return f"Article(title = {self.title}, source = {self.source}, scraped_date = {self.scraped_date})"
