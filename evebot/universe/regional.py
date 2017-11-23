#!/usr/bin/python3

import glob
import os
import yaml

class Regional(object):
	"""docstring for Regional"""
	def __init__(self, path):
		self.name = os.path.basename(os.path.normpath(path)).lower()
		self._path = path
		for file in glob.glob(os.path.join(path, '*')):
			if file.endswith('.staticdata'):
				content_file = os.path.join(path, file)
				with open(content_file) as data:
					self._content = yaml.load(data)
					break


	def to_dict(self):
		temp = self.__dict__
		remove_key = []
		for key in temp.keys():
			if key.startswith('_'):
				remove_key.append(key)
			elif type(temp[key]) == dict:
				for k in temp[key].keys():
					try:
						temp[key][k] = temp[key][k].to_dict()
					except:
						pass
		for key in remove_key:
			del temp[key]
		return temp
