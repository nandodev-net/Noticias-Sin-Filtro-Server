"""
    Serializers for the feed API
"""

# Third party imports
from rest_framework import fields
from rest_framework_dataclasses.serializers import DataclassSerializer

# Local imports
from app.feed.feed import  FeedContent, Section, Feedback
from app.scraper.api.v0_0_2.serializers import HeadlineSerializer, CategorySerializer, MediaSiteSerializer

class SectionSerializer(DataclassSerializer):
    """
        Serialize Section objects
    """
    category = CategorySerializer()
    news = fields.ListField(child=HeadlineSerializer())

    class Meta:
        dataclass = Section


class FeedContentSerializer(DataclassSerializer):
    """
        Serialize a Feed Content object
    """
    
    featured = fields.ListField(child=HeadlineSerializer())
    sections = fields.ListField(child=SectionSerializer())

    class Meta:
        dataclass = FeedContent

class FeedbackSerializer(DataclassSerializer):
    """
        Serialize a Feedback object
    """

    prefered_categories = fields.ListField(child=CategorySerializer())
    prefered_media = fields.ListField(child=MediaSiteSerializer())

    class Meta:
        dataclass = Feedback