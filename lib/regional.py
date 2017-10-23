#!/usr/bin/python3

import os
import yaml

class Regional(object):
	"""docstring for Regional"""
	def __init__(self, path):
		self.name = os.path.basename(os.path.normpath(path))
		self._path = path
		for file in os.listdir(path):
			if file.endswith('.staticdata'):
				content_file = os.path.join(path, file)
				self._content = yaml.load(open(content_file))
				break



