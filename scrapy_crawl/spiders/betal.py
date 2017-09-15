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

class BetalSpider(CrawlSpider):
	name = "betal"

	mongo_collection = "betal2"
	custom_settings = {
		'SOME_SETTING': 'some value',
		'MONGO_COLLECTION': "betal",
		'ITEM_PIPELINES': {
			'scrapy_crawl.cleaning_pipeline.CleaningPipeline': 10,
			'scrapy_crawl.mongo_pipeline.MongoPipeline': 20,
			'scrapy_crawl.images_pipelines.MyImagePipeline': 30
		},
		'IMAGES_STORE': '/exdata/download/comic/betal/',
		'JOBDIR': '/exdata/download/comic/betal/_job/',
		'IM_MODULE': 'scrapy_crawl.images_pipelines.MyImagePipeline',
		'IMAGES_MIN_HEIGHT': 300,
		'IMAGES_MIN_WIDTH': 200
	}

	allowed_domains = ['www.hentailx.com']
	start_urls = ['http://www.hentailx.com']
	rules = (
	    Rule(LinkExtractor(allow=('.',), deny=('returnUrl','.*cap-nhat-chuong.*'), unique=True), callback='parse_item', follow=True),
	)


	def parse_item(self, response):
		loader = ItemLoader(item = ImageItem(), response = response)
		
		loader.add_xpath('image_urls', '//img/@src[string-length( text()) < 1000]') 
		story_name = response.xpath('//*[@id="chapter-detail"]/div/ol/li[2]/a/text()').extract_first()

		if (not story_name):
			story_name = response.xpath('//*[@id="manga-detail"]/div[2]/h1/text()').extract_first()

			if story_name:
				story_name = story_name.strip().strip(' <>')

		chapter_name = response.xpath('//*[@id="chapter-detail"]/div/ol/li[3]/a/text()').extract_first()
		author_name = response.xpath('//*[@id="manga-detail"]/div[2]/div[1]/a/text()').extract_first()
		translator_name = response.xpath('//*[@id="manga-detail"]/div[2]/div[2]/a/text()').extract_first()
		category = response.xpath('//*[@id="manga-detail"]/div[2]/div[4]/a[position()>0]/text()').extract()
		summary = None

		print ("==========================================")
		print(author_name, translator_name, category)


		if category:
			soup = BeautifulSoup(', '.join(category), 'html.parser')
			category = soup.get_text()
			category = re.sub('\n', ',', category).strip()

		print (response.url)

		if story_name:
			
			print (story_name)

			u = Utility()
			story_id = u.convertStringToId(story_name)

			loader.add_value('url', response.url) 
			loader.add_value('story_name', story_name) 
			loader.add_value('story_id', story_id) 


			if chapter_name:
				chapter_name = chapter_name.strip()
				chapter_id = u.convertStringToId(chapter_name)
				chapter_index = int(float(response.xpath('count(//*[@id="ddl_listchap"]/option[@selected]/preceding-sibling::option)').extract_first()))
				chapter_total = int(float(response.xpath('count(//*[@id="ddl_listchap"]/option)').extract_first()))
				loader.add_value('chapter_name', chapter_name) 
				loader.add_value('chapter_index', chapter_index)
				loader.add_value('chapter_total', chapter_total) 

			if author_name:
				author_name = author_name.strip()
				loader.add_value('author_name', author_name) 

			if category:
				category = category.strip()
				loader.add_value('category', category) 

			if translator_name:
				translator_name = translator_name.strip()
				loader.add_value('translator_name', translator_name) 

			if summary:
				loader.add_value('summary', summary) 

			return loader.load_item() 

