# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


from scrapy.pipelines.images import ImagesPipeline, ImageException
from scrapy.http import Request
from io import BytesIO
import hashlib
from scrapy.conf import settings
import re
import scrapy
from scrapy.conf import settings
from scrapy.exceptions import DropItem
from urllib.parse import urljoin

class MyImagePipeline(ImagesPipeline):

	def get_media_requests(self, item, info):

		# If this is the main page, contain no image, then just ignore
		if ('image_urls' in item) and ('chapter_name' in item):
			item['image_urls'] = [ urljoin(item["url"], u) for u in item['image_urls'] ]

			print ("------------------------------------------ get_media_requests")
			image_folder = item["story_id"] + "/" + str(item["chapter_index"]).zfill(6) + "/"
			file_no = 1
			for image_url in item['image_urls']:
				print (image_url)
				if len(image_url) < 1000:
					yield Request(image_url, meta=dict(folder=image_folder, file_no=file_no))
					file_no += 1

	    
	def item_completed(self, results, item, info):
		print ("------------------------------------------ item_completed")
		image_paths = [x['path'] for ok, x in results if ok]
		if not image_paths:
		    raise DropItem("Item contains no images")
		#print (image_paths)
		#item['image_paths'] = image_paths
		return item

	# Override the convert_image method to disable image conversion    
	def convert_image(self, image, size=None):
		buf = BytesIO()        
		try:
			image.save(buf, image.format)
		except Exception as ex:
			raise ImageException("Cannot process image. Error: %s" % ex)

		return image, buf    
	
	def file_path(self, request, response=None, info=None):
		#print ("===============================")

		full_path = request.meta['folder'] + str(request.meta['file_no']).zfill(6) + '.jpg'
		print (full_path)
		return  full_path
	
