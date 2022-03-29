# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# Python imports
from typing import Dict, List, Any
import logging

# Local imports
from app.scraper.models import ArticleHeadline, ArticleCategory
from vsf_crawler.data_schemes.base_scraped_data import BaseDataScheme

# Third party imports
from scrapy.crawler import Crawler, Spider
from scrapy.item import Item


class VsfCrawlerPipeline:
    def __init__(self, source : str, *args, **kwargs):
        self.items : List[Dict[str, Any]] = []
        self.source = source


    @classmethod
    def from_crawler(cls, crawler : Crawler):
        return cls(source=crawler.settings.get("source")) #type: ignore

    def process_item(self, item : BaseDataScheme, spider : Spider):

        assert isinstance(item, BaseDataScheme), \
                f"Programming error. An object of type '{type(item)}' should not make it up to the process item function"

        # Check if already exists
        url = item.url
        if ArticleHeadline.objects.filter(url=url).exists():
            return item

        # Create article object if not exists
        try:
            article, categories_objects = item.as_headline()
            article.save()
            article.categories.set(categories_objects)
        except Exception as e:
            logging.error(f"Error creating ArticleHeadline object: {str(e)}")

        return item


