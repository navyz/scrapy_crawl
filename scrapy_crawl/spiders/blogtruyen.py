# -*- coding: utf-8 -*-
# coding=UTF8
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.http.request import Request
from scrapy_crawl.image_item import ImageItem
from ..utility import Utility
import re
from bs4 import BeautifulSoup
import array
import unicodedata

class BlogSpider(CrawlSpider):
	name = 'blog'

	mongo_collection = "blogtruyen"
	custom_settings = {
		'SOME_SETTING': 'some value',
		'MONGO_COLLECTION': "blogtruyen",
		'ITEM_PIPELINES': {
			'scrapy_crawl.cleaning_pipeline.CleaningPipeline': 10,
			'scrapy_crawl.mongo_pipeline.MongoPipeline': 20,
			'scrapy_crawl.images_pipelines.MyImagePipeline': 30
		},
		'IMAGES_STORE': '/exdata/download/comic/blogtruyen/',
		'JOBDIR': '/exdata/download/comic/blogtruyen/_job/',
		'IM_MODULE': 'scrapy_crawl.images_pipelines.MyImagePipeline',
		'IMAGES_MIN_HEIGHT': 300,
		'IMAGES_MIN_WIDTH': 200
	}


	allowed_domains = ['blogtruyen.com', 'blogspot.com']
	start_urls = ['http://www.blogtruyen.com', 'http://www.blogtruyen.com/c262539/in-a-different-world-with-a-smartphone-episode-1']
	rules = (
	    Rule(LinkExtractor(allow=('.',), deny=('returnUrl','.*cap-nhat-chuong.*'), unique=True), callback='parse_item', follow=True),
	)






	def parse_item(self, response):
		loader = ItemLoader(item = ImageItem(), response = response)
		loader.add_xpath('image_urls', '//img/@src[string-length( text()) < 1000]') 

		story_name = response.xpath('//*[@id="readonline"]/header/div/a[2]/span/text()').extract_first()

		if (not story_name):
			story_name = response.xpath('//*[@id="breadcrumbs"]/span[2]/text()[2]').extract_first()
			if story_name:
				story_name = story_name.strip().strip(' <>')

		chapter_name = response.xpath('//*[@id="readonline"]/header/h1/text()').extract_first()
		author_name = response.xpath('//*[@id="wrapper"]/section[2]/div/div[1]/section/div[3]/p[1]/a/text()').extract_first()
		category = response.xpath('//*[@id="wrapper"]/section[2]/div/div[1]/section/div[3]/p[3]/span[position()>1]').extract()

		print ("==========================================")
		print (response.url)
		print(story_name, chapter_name, author_name, category)

		if story_name:
			u = Utility()
			story_id = u.convertStringToId(story_name)

			loader.add_value('url', response.url) 
			loader.add_value('story_name', story_name) 
			loader.add_value('story_id', story_id) 


			if chapter_name:
				chapter_name = chapter_name.strip()
				chapter_id = u.convertStringToId(chapter_name)
				chapter_index = int(float(response.xpath('count(//*[@id="readonline"]/section[1]/div[1]/select/option[@selected]/preceding-sibling::option)').extract_first()))
				chapter_total = int(float(response.xpath('count(//*[@id="readonline"]/section[1]/div[1]/select/option)').extract_first()))
				loader.add_value('chapter_name', chapter_name) 
				loader.add_value('chapter_index', chapter_index)
				loader.add_value('chapter_total', chapter_total) 

			if author_name:
				author_name = author_name.strip()
				loader.add_value('author_name', author_name) 

			if category:
				soup = BeautifulSoup(', '.join(category), 'html.parser')
				category = soup.get_text()
				category = re.sub('\n', ',', category).strip()
				loader.add_value('category', category) 

			return loader.load_item() 

