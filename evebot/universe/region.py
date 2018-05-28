#!/usr/bin/python3

import glob
import os
import pprint

from . import constellation
from . import regional

class Region(regional.Regional):

	def __init__(self, path_to_region):
		regional.Regional.__init__(self, path_to_region)
		self.name_id = self._content['nameID']
		self.id = self._content['regionID']
		self._populate_constellations()


	def _populate_constellations(self):
		self.constellations = {}
		for directory in glob.glob(os.path.join(self._path, '*/')):
			path = os.path.join(self._path, directory)
			temp = constellation.Constellation(path)
			self.constellations[temp.name] = temp


	def has_solarsystem(self, name):
		for const in self.constellations.keys():
			temp = self.constellations[const].has_solarsystem(name)
			if temp:
				return temp


if __name__ == '__main__':
	from . import config
	region = os.path.join(config.SDE_PATH, 'fsd/universe/eve/BlackRise')
	test = Region(region)
	print(test.name)
	print(test.id)
	print(test.name_id)
	print(test.has_solarsystem('astoh').name)
	pprint.pprint(test.to_dict())
