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

class TttSpider(CrawlSpider):

	name = "ttt"

	mongo_collection = "ttt"
	custom_settings = {
		'SOME_SETTING': 'some value',
		'MONGO_COLLECTION': "ttt",
		'ITEM_PIPELINES': {
			'scrapy_crawl.cleaning_pipeline.CleaningPipeline': 10,
			'scrapy_crawl.mongo_pipeline.MongoPipeline': 20,
			'scrapy_crawl.images_pipelines.MyImagePipeline': 30
		},
		'IMAGES_STORE': '/exdata/download/comic/ttt/',
		'JOBDIR': '/exdata/download/comic/ttt/_job/',
		'IM_MODULE': 'scrapy_crawl.images_pipelines.MyImagePipeline',
		'IMAGES_MIN_HEIGHT': 300,
		'IMAGES_MIN_WIDTH': 200
	}

	allowed_domains = ['truyentranhtuan.com']
	start_urls = ['http://truyentranhtuan.com/', "http://truyentranhtuan.com/rurouni-kenshin-hokkai-arc/"]

	rules = (
	    Rule(LinkExtractor(allow=('.',), deny=('returnUrl','.*cap-nhat-chuong.*'), unique=True), callback='parse_item', follow=True),
	)






	# Parse each request and extract information + image_urls
	def parse_item(self, response):
		loader = ItemLoader(item = ImageItem(), response = response)
		

		story_name = response.xpath('//*[@id="chapter-detail"]/div/ol/li[2]/a/text()').extract_first()

		if (not story_name):
			story_name = response.xpath('//*[@id="read-title"]/p/a/text()').extract_first()
		if (not story_name):
			story_name = response.xpath('//*[@id="infor-box"]/div[2]/h1/text()').extract_first()
		if story_name:
			story_name = story_name.strip()

		chapter_name = response.xpath('//*[@id="read-title"]/p/text()[2]').extract_first()
		author_name = response.xpath('//*[@id="manga-detail"]/div[2]/div[1]/a/text()').extract_first()
		translator_name = response.xpath('//*[@id="manga-detail"]/div[2]/div[2]/a/text()').extract_first()
		category = response.xpath('//*[@id="infor-box"]/div[2]/div/p[3]/a/text()').extract()
		summary = response.xpath('//*[@id="manga-summary"]/p').extract()
		chapter_total = int(float(response.xpath('count(//*[@id="manga-chapter"]/span)').extract_first()))


		if chapter_name: chapter_name = chapter_name.strip()
		if author_name and len(author_name) > 0: author_name = author_name.strip()
		if translator_name: translator_name = translator_name.strip()
		if not chapter_total: chapter_total = 0

		print ("==========================================")
		print(author_name, translator_name)


		if category:
			soup = BeautifulSoup(''.join(category), 'html.parser')
			category = soup.get_text()
			category = re.sub('\n', ',', category).strip()
			category = re.sub('\s+', ' ', category).strip()
			category = re.sub('\s+,', ',', category).strip(',').strip()
			print (category)

		if summary:
			soup = BeautifulSoup(', '.join(summary), 'html.parser')
			summary = soup.get_text()
			summary = re.sub('\n', ',', summary).strip()


		print (response.url)
		print (summary)
		print (story_name)
		print (chapter_name)
		print (category)
		print (author_name)

		if (story_name or chapter_name or category and author_name or summary):

			print ("==========================================zzzz 5")
			u = Utility()
			story_id = u.convertStringToId(story_name)

			loader.add_value('url', response.url) 
			loader.add_value('story_name', story_name) 
			loader.add_value('story_id', story_id) 

			if chapter_name:
				chapter_name = chapter_name.strip().strip('>').strip()
				chapter_id = u.convertStringToId(chapter_name)
				chapter_index = int(float(response.xpath('count(//*[@id="select-chapter-top"]/option)').extract_first()))
				loader.add_value('chapter_name', chapter_name) 
				loader.add_value('chapter_index', chapter_index)

			loader.add_value('chapter_total', chapter_total) 

			if chapter_total and chapter_total > 0:
				author_name = chapter_total

			if author_name:
				loader.add_value('author_name', author_name) 

			if category:
				category = category.strip()
				loader.add_value('category', category) 

			if translator_name:
				translator_name = translator_name.strip()
				loader.add_value('translator_name', translator_name) 


			if summary:
				loader.add_value('summary', summary) 

			urls = response.xpath('(//script/text())').re("var slides_page_url_path[^\]]+\]")
			if urls and len(urls) > 0:
				urls = urls[0].replace("var slides_page_url_path = ", "")

				urlArr = urls.split(",")
				urlArr2 = []
				for url in urlArr:
					url = url.strip('[];"\'').strip()
					urlArr2.append(url)
					
				loader. add_value('image_urls', urlArr2)

			else:
				print ("----------------------------------------------------------------------------")


			return loader.load_item() 

