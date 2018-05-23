#!/usr/bin/python3

import glob
import os

from . import region


class Universe(object):

	def __init__(self, path_to_universe):
		self.regions = {}
		for directory in sorted(glob.glob(os.path.join(path_to_universe, '*/'))):
			path = os.path.join(path_to_universe, directory)
			print(path)
			temp = region.Region(path)
			self.regions[temp.name] = temp


	def to_dict(self):
		temp = {}
		for key in self.regions.keys():
			temp[key] = self.regions[key].to_dict()
		return temp


if __name__ == '__main__':
	from . import config
	eve_universe = os.path.join(config.SDE_PATH, 'fsd/universe/eve')
	test = Universe(eve_universe)
