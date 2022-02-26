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
    name = models.CharField(verbose_name="Category name", null=False, unique=True, max_length=30)

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
        UNKNOWN  = ("unknown", "unknown")

    # Article title
    title = models.TextField(verbose_name="Title", null=False, max_length=200)

    # Publication date
    date = models.DateTimeField(verbose_name="Publication name", null=True)

    # Possible categories
    categories = models.ManyToManyField(to=ArticleCategory)

    # Possible summary for the new provided by the site
    excerpt = models.TextField(default="Excerpt", null=True, max_length=300)

    # Main image for this headline
    image = models.ImageField(verbose_name="Header image")

    # Scraped date
    scraped_date = models.DateTimeField(verbose_name="Scraped date", null=False, auto_created=True, auto_now_add=True)

    # Where did this heading come from
    source = models.CharField(max_length=30, choices=Source.choices, default=Source.UNKNOWN)