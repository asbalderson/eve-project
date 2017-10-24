#!/usr/bin/python3

import glob
import os

import region


class Universe(object):

	def __init__(self, path_to_universe):
		self.regions = []
		for directory in sorted(glob.glob(os.path.join(path_to_universe, '*/'))):
			path = os.path.join(path_to_universe, directory)
			print(path)
			self.regions.append(region.Region(path))


	def get_region(self, name):
		for region in regions:
			if region.name.lower() == name.lower():
				return region
		return None


	def get_constillation(self, name):
		for region in regions:
			if region.has_constellation(name):
				return region.get_constillation(name)
		return None


	def get_solarsystem(self, name):
		for region in regions:
			if region.has_solarsystem(name):
				return region.get_solarsystem(name)
		return None


	def __str__(self):
		#dump to json/dictionary
		pass


if __name__ == '__main__':
	import config
	eve_universe = os.path.join(config.SDE_PATH, 'fsd/universe/eve')
	test = Universe(eve_universe)
