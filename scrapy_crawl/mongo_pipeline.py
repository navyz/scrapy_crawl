import pymongo
from pymongo import MongoClient
from .chapter_item import ChapterItem
from .image_item import ImageItem

class MongoPipeline(object):

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        print ("------------------------------------------ MongoPipeline")
        chapter_item = ChapterItem()

        chapter_item["url"] = item["url"]
        if 'story_name' in item:
            
            chapter_item["story_name"] = item["story_name"]            
            chapter_item["story_id"] = item["story_id"]

            if 'chapter_name' in item:
                chapter_item["chapter_name"] = item["chapter_name"]

            if 'chapter_index' in item:
                chapter_item["chapter_index"] = item["chapter_index"]
                
            if 'chapter_total' in item:
                chapter_item["chapter_total"] = item["chapter_total"]
            
            if 'author_name' in item:
                chapter_item["author_name"] = item["author_name"]
            
            if 'translator_name' in item:
                chapter_item["translator_name"] = item["translator_name"]
            
            if 'category' in item:
                chapter_item["category"] = item["category"]

            if 'summary' in item:
                chapter_item["summary"] = item["summary"]

            comic_chapter_id = self.db[spider.mongo_collection].insert_one(dict(chapter_item))

        return item