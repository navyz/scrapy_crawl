import pymongo
from bs4 import BeautifulSoup

# Use the SoupBeauti library to clean up the html
# - reformat the html page
# - Remove unnessary content (scrip, error message, ...)
class CleaningPipeline(object):

    def __init__(self):
        pass

    def process_item(self, item, spider):
        print ("------------------------------------------ CleaningPipeline")
        return item