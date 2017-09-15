# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field

class ChapterItem(scrapy.Item):
	# define the fields for your item here like:
	url = scrapy.Field()
	story_name = scrapy.Field()
	story_id = scrapy.Field()
	chapter_name = scrapy.Field()
	chapter_index = scrapy.Field()
	chapter_total = scrapy.Field()
	image_no = scrapy.Field()
	image_urls = scrapy.Field()

	author_name = scrapy.Field()
	category = scrapy.Field()
	translator_name = scrapy.Field()
	summary = scrapy.Field()

