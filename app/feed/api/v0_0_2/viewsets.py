"""
    Endpoint logic for the feed module
"""

# Local imports
from app.feed.feed import Feed
from app.feed.api.v0_0_2.serializers import FeedContentSerializer

# Third party imports
from rest_framework.viewsets import ViewSet, GenericViewSet
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
import  rest_framework.permissions as permissions

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
                Defaults to no feed, delivered headlines might not be interesting for the user
                - amount_featured : `int` = (optional) amount of featured / special news to show up as the first section. Defaults to 3
                - instance_per_section : `int` = (optional) how many headlines to deliver per section. Defaults to 4
                - categories_sections : `List[str]`  = (optional) categories to show up in the feed as sections. Defaults to editor's choice
        """
        # Possible error message
        err_msg = ""

        # Parse arguments
        data = request.data
        feedback = data.get("feedback") or {}                               # type: ignore
        amount_featured = int(data.get("amount_featured") or 3)                  # type: ignore
        instance_per_section = int(data.get("instance_per_section") or 4)        # type: ignore
        categories_sections = data.getlist("categories_sections") or None   # type: ignore

        # Feed client: use it to create the retrieved data
        feed = Feed()
        content = feed.home(amount_featured, instance_per_section, categories_sections, feedback)


        return Response(data=FeedContentSerializer(content).data)

    