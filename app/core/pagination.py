"""
    Define pagination objects used for django rest framework api calls
"""

# Third party imports
from rest_framework.pagination import PageNumberPagination


class VIPagination(PageNumberPagination):
    """
    Base class for this project's pagination (VI stands for VeInteligente)
    """

    page_size = 50
    page_size_query_param = "page_size"
    max_page_size = 1000

    def get_paginated_response(self, data):
        response = super().get_paginated_response(data)
        response.data["total_pages"] = self.page.paginator.num_pages  # type: ignore
        return response
