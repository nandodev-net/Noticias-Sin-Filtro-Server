"""
    Viewsets for the killswitch
"""

# Local imports 
from noticias_sin_filtro_server.versioning.killswitch import KillSwtich

# Thirs party imports
from rest_framework.viewsets import ViewSet
from rest_framework.request import Request
from rest_framework.response import Response

class KillSwitchViewSet(ViewSet):
    """
        Manage views for the killswitch. The api for this endpoint should not change by any mean
    """

    permission_classes = []

    def get(self, request : Request) ->  Response:
        """
            Checks if the provided version and platforms are valid
        """
        version = request.query_params.get("version")
        platform = request.query_params.get("platform")

        if not version:
            return Response(status=400, data={"error" : "Missing 'version' argument"})
        
        if not platform:
            return Response(status=400, data={"error" : "Missing 'platform' argument"})

        try:
            return Response(data={"compatibility" : KillSwtich.compatibility(version, platform).value}) # type: ignore
        except ValueError as e:
            return Response(status=400, data={"error" : str(e)})


