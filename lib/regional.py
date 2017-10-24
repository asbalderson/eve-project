#!/usr/bin/python3

import glob
import os
import yaml

class Regional(object):
	"""docstring for Regional"""
	def __init__(self, path):
		self.name = os.path.basename(os.path.normpath(path))
		self._path = path
		for file in glob.glob(os.path.join(path, '*')):
			if file.endswith('.staticdata'):
				content_file = os.path.join(path, file)
				with open(content_file) as data:
					self._content = yaml.load(data)
					break



