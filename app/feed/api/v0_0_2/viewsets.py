"""
    Endpoint logic for the feed module
"""
# Python imports
import json

from requests import JSONDecodeError

# Local imports
from app.feed.feed import Feed, Feedback
from app.feed.api.v0_0_2.serializers import FeedContentSerializer

# Third party imports
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from app.scraper.models import ArticleCategory, MediaSite

class FeedView(APIView):
    """
        Deliver the feed to the api
    """
    permission_classes = []
    pagination_class = None

    def post(self, request : Request, *args, **kwargs):
        """
            Use this method to get a stream  of news for the feed.

            # Parameters
                - feedback : `Object` = (optional) Data from the user useful to populate the feed according to her preferences. 
                        Expected format:      
                            ```
                            {
                                prefered_categories : [str] = List of category names
                                prefered_media : [str] = List of media site names
                            }
                            ```

                Defaults to no feed, delivered headlines might not be interesting for the user
                - amount_featured : `int` = (optional) amount of featured / special news to show up as the first section. Defaults to 3
                - instance_per_section : `int` = (optional) how many headlines to deliver per section. Defaults to 4
                - categories_sections : `List[str]`  = (optional) categories to show up in the feed as sections. Defaults to editor's choice
        """
        # Parse arguments
        data = request.data

        # Parse feedback
        feedback = data.dict().get("feedback") or {"prefered_categories" : [],"prefered_media" : [] }                               # type: ignore

        if isinstance(feedback, str):
            try:
                feedback = json.loads(feedback)
            except JSONDecodeError:
                return Response(data={"error" : "feedback object is not dict-like."}, status=400)
                 

        if not isinstance(feedback, dict):
            return Response(data={"error" : "feedback object is not dict-like."}, status=400) 

        

        # Check prefered categories
        if (prefered_categories := feedback.get("prefered_categories")) is None:
            return Response(data={"error" : "'prefered_categories' field missing in feedback object"}, status=400)
        elif not isinstance(prefered_categories, list):
            return Response(data={"error" : "'prefered_categories' field in feedback object is not a list"}, status=400)
        elif any(not isinstance(x, str) for x in prefered_categories):
            return Response(data={"error" : "'prefered_categories' field in feedback object is not a list of string"}, status=400)

        # Check prefered categories
        if (prefered_media := feedback.get("prefered_media")) is None:
            return Response(data={"error" : "'prefered_media' field missing in feedback object"}, status=400)
        elif not isinstance(prefered_media, list):
            return Response(data={"error" : "'prefered_media' field in feedback object is not a list"}, status=400)
        elif any(not isinstance(x, str) for x in prefered_media):
            return Response(data={"error" : "'prefered_media' field in feedback object is not a list of string"}, status=400)

        # Check if they're ints
        try:
            amount_featured = int(data.get("amount_featured") or 3)                  # type: ignore
        except (TypeError, ValueError) as e:
            return Response(data={"error" : "'amount_features' field not a valid int"}, status=400)

        try:
            instance_per_section = int(data.get("instance_per_section") or 4)        # type: ignore
        except (TypeError, ValueError):
            return Response(data={"error" : "'instance_per_section' field not a valid int"}, status=400)
        
        categories_sections = data.getlist("categories_sections") or []   # type: ignore
        if categories_sections and any(not isinstance(x, str) for x in categories_sections):
            return Response(data={"error" : "'categories_sections' is not a list of string"}, status=400)

        # Get the actual data 
        prefered_categories = list(ArticleCategory.objects.all().filter(name__in=prefered_categories))
        prefered_media = list(MediaSite.objects.all().filter(name__in = prefered_media))

        categories_sections = list(ArticleCategory.objects.all().filter(name__in=categories_sections))

        # Feed client: use it to create the retrieved data
        feed = Feed(Feedback(prefered_categories, prefered_media))
        content = feed.home(amount_featured, instance_per_section, categories_sections=categories_sections)


        return Response(data=FeedContentSerializer(content).data)

    