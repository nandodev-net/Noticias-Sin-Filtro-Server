"""
    Serializers for the feed API
"""

# Third party imports
from dataclasses import dataclass
from unicodedata import category
from rest_framework import serializers
from rest_framework import fields
from rest_framework_dataclasses.serializers import DataclassSerializer

# Local imports
from app.feed.feed import Feed, FeedContent, Section
from app.scraper.api.v0_0_2.serializers import HeadlineSerializer, CategorySerializer

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