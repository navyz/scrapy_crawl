from .vietnamese_unicode import VietnameseProcessing
import re

class Utility():
	def convertStringToId(self, text):
		if text and len(text) > 0:
			vp = VietnameseProcessing()
			print ("after normalize ", text)
			output = vp.vietnameseToLatin(text).strip().lower()
			print ("after convert vietnamese: ", output)
			output = re.sub('[^a-zA-Z0-9_]', '_', output)
			output = re.sub('_+', '_', output).strip('_')
			return output
