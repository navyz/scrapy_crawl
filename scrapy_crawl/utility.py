from .vietnamese_unicode import VietnameseProcessing
import re

class Utility():
	def convertStringToId(self, text):
		if text and len(text) > 0:
			vp = VietnameseProcessing()
			output = vp.vietnameseToLatin(text).strip().lower()
			output = re.sub('[^a-zA-Z0-9_]', '_', output)
			output = re.sub('_+', '_', output).strip('_')
			return output
