"""
    Views for this api endpoint
"""

# Python imports
from typing import Dict
import datetime

from django.http import QueryDict

# Local imports 
from app.core.pagination import VIPagination
from app.scraper.models import ArticleHeadline, ArticleCategory
from app.scraper.api.v0_0_1.serializers import HeadlineSerializer, CategorySerializer
from noticias_sin_filtro_server.settings import DATE_FORMAT

# Third party imports
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

# Django imports
from django.db.models import Prefetch

# -- < Headlines > ------------------------------------------------
class HeadlineViewSet(viewsets.ModelViewSet):
    """
        To manage querys over instances
    """
    serializer_class = HeadlineSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = VIPagination
    
    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_403_FORBIDDEN)

    def create(self, request, *args, **kwargs):
        return Response(status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_403_FORBIDDEN)

    def get_queryset(self):
        """
            Filter response by:
                + media_sites: [str] = sources that should be included in this query. Defaults to all.
                + categories: [str] = categories that should be included in this query, it will
                                      return headlines such that they have at the least one of the categories listed
                                      here. Defaults to all.
                + relevance: Optional[bool] = if delivered news should be all relevant (true), 
                    non relevant (false), or any (None). Defaults to None.
                + start_date: datetime = start date for retrieved news. Format: YYYY-mm-dd:HH:MM:ss
                + end_date: datetime = end date for retrieved news. Format: YYYY-mm-dd:HH:MM:ss
                + title_contains: str = a string that should be contained by the headline's title
                + page: int = page to retrieve
                + page_size: int = page size for pagination
        """
        
        # Initial queryset
        qs = ArticleHeadline.objects.all()
        params : QueryDict = self.request.query_params # type: ignore


        # Filter queryset
        if (media_sites := params.getlist("media_sites[]")) not in [None, []]:
            print(media_sites)
            qs = qs.filter(source__in = media_sites)

        if (categories := params.getlist("categories[]")) not in [None, []]: 
            # TODO hacer esta query
            qs = qs.filter(categories__name__in = categories)

        if (relevance := params.get("relevance")) != None:
            relevance = relevance.to_lowercase() == 'true' # type: ignore
            qs = qs.filter(relevance=relevance)

        if (start_date := params.get("start_date")) != None:
            start_date = datetime.datetime.strptime(DATE_FORMAT, start_date)
            qs = qs.filter(datetime__gte = start_date)

        if (end_date := params.get("end_date")) != None:
            end_date = datetime.datetime.strptime(DATE_FORMAT, end_date)
            qs = qs.filter(datetime__gte = end_date)

        if (title_contains := params.get("title_contains")) != None:
            qs = qs.filter(title__icontains=title_contains)

        qs.order_by('datetime', 'title')
        
        return qs

# -- < Categories > --------------------------------------------------

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