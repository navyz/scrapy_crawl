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

class MangakSpider(CrawlSpider):
	name = "mangak"

	mongo_collection = "mangak"
	custom_settings = {
		'MONGO_COLLECTION': "mangak",
		'ITEM_PIPELINES': {
			'scrapy_crawl.cleaning_pipeline.CleaningPipeline': 10,
			'scrapy_crawl.mongo_pipeline.MongoPipeline': 20,
			'scrapy_crawl.images_pipelines.MyImagePipeline': 30
		},
		'IMAGES_STORE': '/exdata/download/comic/mangak/',
		'JOBDIR': '/exdata/download/comic/mangak/_job/',
		'IM_MODULE': 'scrapy_crawl.images_pipelines.MyImagePipeline',
		'IMAGES_MIN_HEIGHT': 300,
		'IMAGES_MIN_WIDTH': 200,
                'LOG_LEVEL': 'DEBUG'
	}

	allowed_domains = ['mangak.info']
	start_urls = ['http://mangak.info/', 'http://mangak.info/hot/']
	rules = (
	    Rule(LinkExtractor(allow=('.',), deny=('returnUrl','redirect_to', 'wordpress_social_authenticate', 'wp-login', 'replytocom'), unique=True), callback='parse_item', follow=True),
	)


	def parse_item(self, response):
		loader = ItemLoader(item = ImageItem(), response = response)
		
		loader.add_xpath('image_urls', '//img/@src[string-length( text()) < 1000]') 
		story_name = response.xpath('//h1[@class="entry-title"]/text()').extract_first()

		if (not story_name):
			story_name = response.xpath('//*[@id="trang_doc"]/div/div/div/div/p/span[5]/a/text()').extract_first()

			if story_name:
				story_name = story_name.strip().strip(' <>')

		chapter_name = response.xpath('//h1[@class="name_chapter entry-title"]/text()').extract_first()
		author_name = response.xpath('//ul[@class="truyen_info_right"]/li[2]/a/text()').extract_first()
		translator_name = response.xpath('//ul[@class="truyen_info_right"]/li[5]/a/text()').extract_first()
		category = response.xpath('//ul[@class="truyen_info_right"]/li[3]/a/text()').extract()
		summary = response.xpath('//div[@class="entry-content"]/p').extract()

		print ("==========================================")
		print(author_name, translator_name, category)


		if category:
			soup = BeautifulSoup(', '.join(category), 'html.parser')
			category = soup.get_text()
			category = re.sub('\n', ',', category).strip()

		if summary:
			soup = BeautifulSoup(', '.join(summary), 'html.parser')
			summary = soup.get_text()
			summary = re.sub('\n', ',', summary).strip()

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

				# reverse index
				chapter_index = \
					int(float(	\
						response.xpath(	\
							'count((//select)[1]/option[@value="' + response.url +'"]/preceding-sibling::option)').extract_first()))


				chapter_total = int(float(response.xpath('count((//select)[1][@class="select-chapter"]/option)').extract_first()))

				# chapter is sorted in reverted order
				chapter_index = chapter_total - chapter_index 

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

