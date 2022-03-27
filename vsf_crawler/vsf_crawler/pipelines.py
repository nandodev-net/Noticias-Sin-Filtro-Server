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

        # Create article object
        try:
            article, categories_objects = item.as_headline()
            self.items.append({"headline" : article, "categories" : categories_objects})
        except Exception as e:
            logging.error(f"Error creating ArticleHeadline object: {str(e)}")

        return item

    def close_spider(self, spider : Spider):
        # If no item gathered, just end
        if not self.items:
            return

        # Save newly acquaired items
        headlines = [item.get("headline") for item in self.items]
        categories= [item.get("categories") for item in self.items]
        self.items = []

        headlines_created = []
        try:
            # Create new articles
            headlines_created = ArticleHeadline.objects.bulk_create(headlines, ignore_conflicts=True)
        except Exception as e:
            logging.error(f"Could not create article headline objects. Error: {str(e)}")

        # Set up categories
        created_index = 0
        for (headline, category_list) in zip(headlines, categories):

            assert headline
            assert category_list != None

            if headlines_created[created_index].url == headline.url:
                headline = headlines_created[created_index]
                created_index += 1
            else:
                continue

            # Do nothing if no category list
            if not category_list: continue

            try:
                headline.categories.set(category_list)
            except Exception as e:
                logging.error(f"Could not set category list. Error: {e}")

