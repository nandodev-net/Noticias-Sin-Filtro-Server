"""
    This files contains definitions for async process
"""
# Local imports

# Third party imports
from celery import shared_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@shared_task
def scraper_task():
    from app.scraper.scraper import Scraper
    from app.scraper.models import ArticleHeadline

    # Write by hand currently active scrapers
    scrapers_to_run = [ArticleHeadline.Source.LA_PATILLA.value]
    scraper = Scraper()

    logger.info(f"Starting to run scraping process for scrapers: {', '.join(scrapers_to_run)}") # type: ignore
    process = scraper.scrape(scrapers_to_run) # type: ignore
    
    logger.info(f"Currently active scraping process: {process}")
