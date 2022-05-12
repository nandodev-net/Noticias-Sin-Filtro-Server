"""
    Views for this api endpoint
"""

# Python imports
import datetime
from ntpath import join

from django.http import QueryDict

# Local imports
from app.core.pagination import VIPagination
from app.scraper.models import ArticleHeadline, ArticleCategory, MediaSite
from app.scraper.api.v0_0_2.serializers import HeadlineSerializer, CategorySerializer, MediaSiteSerializer
from noticias_sin_filtro_server.settings import DATE_FORMAT

# Third party imports
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.request import Request

# Django imports

# -- < Headlines > ------------------------------------------------
class HeadlineViewSet(viewsets.ModelViewSet):
    """
    Use this endpoint to browse `HeadLine` objects. A **`HeadLine`** represents an actual headline
    in the main page of each news site. Usually, they provide categories, title, excerpt, a thumbnail image, 
    and the url to the article's web page itself. Results are sorted by datetime and title, 
    descending by date, ascending by title.
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
        params: QueryDict = self.request.query_params  # type: ignore

        # Filter queryset
        if (media_sites := params.getlist("media_sites[]")) not in [None, []]:
            qs = qs.filter(source__name__in=media_sites)

        if (categories := params.getlist("categories[]")) not in [None, []]:
            qs = qs.filter(categories__name__in=categories)

        if (relevance := params.get("relevance")) != None:
            relevance = relevance.to_lowercase() == "true"  # type: ignore
            qs = qs.filter(relevance=relevance)

        if (start_date := params.get("start_date")) != None:
            start_date = datetime.datetime.strptime(DATE_FORMAT, start_date)
            qs = qs.filter(datetime__gte=start_date)

        if (end_date := params.get("end_date")) != None:
            end_date = datetime.datetime.strptime(DATE_FORMAT, end_date)
            qs = qs.filter(datetime__gte=end_date)

        if (title_contains := params.get("title_contains")) != None:
            qs = qs.filter(title__icontains=title_contains)

        qs.order_by("-datetime", "title")

        return qs

    def options(self, request : Request, *args, **kwargs):
        meta = self.metadata_class() # type: ignore
        data = meta.determine_metadata(request, self)

        media_site_names = [x.name for x in MediaSite.objects.all()]
        categories_names = [x.name for x in ArticleCategory.objects.all()]
        data['actions']['GET'] = {
            "media_sites" : {
                "in" : "query",
                "type" : "array",
                "description" : "sources that should be included in this query. Defaults to all.",
                "required" : "false",
                "default" : media_site_names,
                "items" : {
                    "type" : "string",
                    "enum" : media_site_names,
                }

            },
            "categories" : {
                "in" : "query",
                "type" : "array",
                "description" : """categories that should be included in this query, it will return headlines such that they have at the least one of the categories listed here. Defaults to all.""",
                "required" : "false",
                "default" : categories_names,
                "items" : {
                    "type" : "string",
                },
            },
            "relevance" : {
                "in" : "query",
                "type" : "bool",
                "description" : """if delivered news should be all relevant (true), non relevant (false), or any (null). Defaults to null.""",
                "required" : "false",
                "default" : None
            },
            "start_date" : {
                "in" : "query",
                "type" : "datetime",
                "description" : """start date for retrieved news. Format: YYYY-mm-dd:HH:MM:ss. If not provided (or set to null), returns articles from the start of time""",
                "required" : "false",
                "default" : None
            },
            "end_date" : {
                "in" : "query",
                "type" : "datetime",
                "description" : """end date for retrieved news. Format: YYYY-mm-dd:HH:MM:ss. If not provided (or set to null), returns articles up to now""",
                "required" : "false",
                "default" : None
            },
            "title_contains" : {
                "in" : "query",
                "type" : "string",
                "description" : """a string that should be contained by the headline's title. If not provided (or set to null), any title is valid""",
                "required" : "false",
                "default" : None
            },    
            "page" : {
                "in" : "query",
                "type" : "int",
                "description" : """page to retrieve, """,
                "required" : "false",
                "default" : 1
            },    
            "page_size" : {
                "in" : "query",
                "type" : "int",
                "description" : """page size for pagination""",
                "required" : "false",
                "default" : 50
            },    
        }

        return Response(data=data, status=status.HTTP_200_OK)

# -- < Categories > --------------------------------------------------


class CategoryViewSet(viewsets.ModelViewSet):
    """
    Return a list with all categories and their color.

    # Parameters
    - `editors_choice` : `bool` = (optional) if retrieved categories should all be "editors choice" categories. 
                                    If not provided (null), return any category
    # Returns
    - `category_name` : `str` = the human-readable name 
    - `category_lookable_name` : `str` = the machine-friendly name you pass to querys.
    - `color` : `str` = the color in hex for this category
    - `editors_choice` : `bool`= if this category is editors choice or not
    """

    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = None

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_403_FORBIDDEN)

    def create(self, request, *args, **kwargs):
        return Response(status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_403_FORBIDDEN)

    def get_queryset(self):
        """
            Filter according to the specified query params
        """
        queryset = ArticleCategory.objects.all()
        params: QueryDict = self.request.query_params # type: ignore

        if (is_editors_choice := params.get("editors_choice")) is not None:
            queryset = queryset.filter(editors_choice = is_editors_choice.lower() == "true")

        return queryset


# -- < Media Sites > -----------------------------------


class MediaSiteViewSet(viewsets.ModelViewSet):
    """
    Return a list with all media sites names.

    - `site_lookable_name` is a machine-friendly string you pass to querys, 
    - `site_name` is an human friendly name. 
    - `site_url` is an url to the site's main page
    """
    queryset = MediaSite.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = MediaSiteSerializer
    pagination_class = None

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_403_FORBIDDEN)

    def create(self, request, *args, **kwargs):
        return Response(status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_403_FORBIDDEN)
