"""
    Some monitoring views that might be used to manually trigger a scraping or check the scraping status
"""
# Local imports
from app.scraper.scraper import Scraper, scrapyd

# Django imports
from django.forms import ValidationError
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.core.validators import URLValidator
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


@method_decorator(csrf_exempt, name="dispatch")  # TODO debug only, delete later
class ScrapingManagerView(View):
    """
    View to manage a scraping process, allowing you to check
    the scraper status and trigger a new scraping process
    """

    def post(self, request: HttpRequest) -> HttpResponse:

        # Get scraper to trigger
        scraper = request.POST.get("scraper", None)
        print(request.POST.dict())
        if not scraper:
            return JsonResponse({"error": "missing 'scraper' argument"})

        # Create scraper
        scraper_client = Scraper()

        # Scrape and retrieve tasks ids
        try:
            task_ids = scraper_client.scrape([scraper])
        except ValueError as e:  # If couldn't scrape, maybe we're using the wrong scraper type
            import logging
            logging.error("Could not start scraping")
            return JsonResponse({"status": "error", "msg": str(e)})

        return JsonResponse({"status": "started", "ids": task_ids})

    def get(self, request: HttpRequest) -> HttpResponse:
        # Check status for some scraper process
        task_id = request.GET.get("task_id", None)

        # Check if task_id was provided
        if not task_id:
            return JsonResponse({"error": "missing task_id argument"})

        # Check current status
        status = scrapyd.job_status("default", task_id)

        return JsonResponse({"status": status})


def _is_valid_url(url: str) -> bool:
    """
    Check if the given url is a valid one
    """

    validate = URLValidator()

    try:
        validate(url)
    except ValidationError:
        return False

    return True
