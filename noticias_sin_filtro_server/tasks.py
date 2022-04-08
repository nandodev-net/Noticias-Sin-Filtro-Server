"""
    This files contains definitions for async process
"""
# Python imports
import datetime
import pytz

# Third party imports
from celery import shared_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@shared_task
def scraper_task():
    from app.scraper.scraper import Scraper
    from app.scraper.models import MediaSite


    now = datetime.datetime.now(tz=pytz.utc)
    # Collect scrapers to process
    scrapers_to_run = [x for x in MediaSite.objects.all() if x.scraping_active and (now - x.last_scraped).seconds > x.scraping_frequency_mins]
    if not scrapers_to_run:
        logger.info(f"No scrapers pending to run right now") # type: ignore
        return

    scraper = Scraper()

    scraper_names = [x.scraper for x in scrapers_to_run]
    logger.info(f"Starting to run scraping process for scrapers: {', '.join(scraper_names)}") # type: ignore
    process = scraper.scrape(scraper_names) # type: ignore   
    logger.info(f"Currently active scraping process: {process}")

    # Update last scraping time 
    for scraper in scrapers_to_run:
        scraper.last_scraped = now
        scraper.save()
    
