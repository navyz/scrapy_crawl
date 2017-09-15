# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst

from scrapy.item import Item, Field

class ImageItem(Item):
	# Mandatory for image downloading
	url = scrapy.Field(output_processor=TakeFirst())
	images = Field()
	image_urls = Field()
	image_paths = Field()

	story_name = scrapy.Field(output_processor=TakeFirst())
	story_id = scrapy.Field(output_processor=TakeFirst())
	chapter_name = scrapy.Field(output_processor=TakeFirst())
	chapter_index = scrapy.Field(output_processor=TakeFirst())
	chapter_total = scrapy.Field(output_processor=TakeFirst())
	image_no = scrapy.Field(output_processor=TakeFirst())

	author_name = scrapy.Field(output_processor=TakeFirst())
	translator_name = scrapy.Field(output_processor=TakeFirst())
	category = scrapy.Field(output_processor=TakeFirst())

	summary = scrapy.Field(output_processor=TakeFirst())
