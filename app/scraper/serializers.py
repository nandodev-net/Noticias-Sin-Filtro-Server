"""
    Serializers to map from headline model into json, this is required
    by the django restframework library to deliver model-based api calls
"""
# Local imports
from app.scraper.models import ArticleCategory, ArticleHeadline
from app.core.pagination import VIPagination

# Third party imports 
from rest_framework import serializers, viewsets, permissions, status
from rest_framework.response import Response

# -- < Headlines > ------------------------------------------------
class CategoryFieldSmall(serializers.RelatedField):
    """
        This field for categories is required only inside headline serializer to convert 
        from headline model object to list of strings
    """

    def to_representation(self, instance : ArticleCategory):
        return instance.name

    class Meta:
        model = ArticleCategory
        fields = ['name']

class HeadlineSerializer(serializers.HyperlinkedModelSerializer):
    """
        Serializer to transform ArticleHeadline objects into json
    """

    categories = CategoryFieldSmall(read_only = True, many = True)
    media_site = serializers.CharField(read_only=True, source='source')

    class Meta:
        model = ArticleHeadline
        fields = ['title', 'datetime', 'categories' ,'excerpt', 'image_url', 'scraped_date', 'media_site', 'url', 'relevance']


class HeadlineViewSet(viewsets.ModelViewSet):
    """
        To manage querys over instances
    """
    queryset = ArticleHeadline.objects.all()
    serializer_class = HeadlineSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = VIPagination

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_403_FORBIDDEN)

    def create(self, request, *args, **kwargs):
        return Response(status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_403_FORBIDDEN)


# -- < Categories > --------------------------------------------------

class CategorySerializer(serializers.ModelSerializer):
    """
        Return a category as just its name
    """
    def to_representation(self, instance : ArticleCategory):
        return instance.name
    class Meta:
        model = ArticleCategory
        fields = ['name']

class CategoryViewSet(viewsets.ModelViewSet):
    """
        Represents a query for categories
    """

    queryset = ArticleCategory.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = None

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_403_FORBIDDEN)

    def create(self, request, *args, **kwargs):
        return Response(status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_403_FORBIDDEN)

# -- < Media Sites > -----------------------------------

class MediaSiteViewSet(viewsets.ViewSet):
    """
        Simple viewset to deliver all current sites
    """
    permission_classes = []
    pagination_class = None
    serializer_class = None

    def list(self, request):
        return Response(ArticleHeadline.Source.values)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_403_FORBIDDEN)

    def create(self, request, *args, **kwargs):
        return Response(status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_403_FORBIDDEN)