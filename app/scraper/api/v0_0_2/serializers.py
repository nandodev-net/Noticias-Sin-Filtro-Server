"""
    Serializers to map from headline model into json, this is required
    by the django restframework library to deliver model-based api calls
"""
# Local imports
from app.scraper.models import ArticleCategory, ArticleHeadline, MediaSite

# Third party imports
from rest_framework import serializers


# -- < Headlines > ------------------------------------------------
class CategoryFieldSmall(serializers.RelatedField):
    """
    This field for categories is required only inside headline serializer to convert
    from headline model object to list of strings
    """

    def to_representation(self, instance: ArticleCategory):
        return instance.name

    class Meta:
        model = ArticleCategory
        fields = ["name"]


class HeadlineSerializer(serializers.ModelSerializer):
    """
        Serializer to transform ArticleHeadline objects into json
    """

    categories = CategoryFieldSmall(read_only=True, many=True)
    media_site = serializers.CharField(read_only=True, source="source__name")

    class Meta:
        model = ArticleHeadline
        fields = [
            "title",
            "datetime",
            "categories",
            "excerpt",
            "image_url",
            "scraped_date",
            "media_site",
            "url",
            "relevance",
            "media_site"
        ]

class MediaSiteSerializer(serializers.ModelSerializer):
    """
        Serializer to transform a MediaSite object into json
    """

    site_name = serializers.CharField(read_only=True, source='human_name')
    site_lookable_name = serializers.CharField(read_only=True, source = 'name')

    class Meta:
        model = MediaSite
        fields = [
            "site_url",
            "site_url_image",
            "site_lookable_name",
            "site_name"
        ]


# -- < Categories > --------------------------------------------------


class CategorySerializer(serializers.ModelSerializer):
    """
    Return a category as just its name
    """

    def to_representation(self, instance: ArticleCategory):
        return {"category_name" : instance.name, "category_lookable_name" : instance.name, "category_color" : instance.color}

    class Meta:
        model = ArticleCategory
        fields = ["name", "color"]
