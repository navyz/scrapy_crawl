# -*- coding: utf-8 -*-

# Scrapy settings for betal project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'scrapy_crawl'

SPIDER_MODULES = ['scrapy_crawl.spiders']
NEWSPIDER_MODULE = 'scrapy_crawl.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'betal (+http://www.yourdomain.com)'

# Obey robots.txt rules

COOKIES_ENABLED = False
ROBOTSTXT_OBEY = True
MONGO_URI = "mongodb://127.0.0.1"
MONGO_DATABASE = "comic"

LOG_LEVEL='INFO'

USER_AGENT = "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36"

#JOBDIR = '/download/comic/betal/_job'


# Random interval between 0.5 and 1.5 * DOWNLOAD_DELAY
DOWNLOAD_DELAY = 0.2

# USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

# Where we store the images, in this case they will be stored 
# Specify the min height and width of the image to download

IMAGES_EXPIRES = 1
MEDIA_ALLOW_REDIRECTS = True

IMAGES_URLS_FIELD = 'image_urls'
FEED_EXPORT_ENCODING = 'utf-8'

DOWNLOAD_FAIL_ON_DATALOSS = False

DNS_TIMEOUT = 2
DOWNLOAD_TIMEOUT = 4

RETRY_ENABLED = False

