#!/usr/bin/python3

import glob
import os
import yaml

import constellation
import regional

class Region(regional.Regional):

	def __init__(self, path_to_region):
		regional.Regional.__init__(self, path_to_region)
		self.name_id = self._content['nameID']
		self.id = self._content['regionID']
		self._populate_constellations()


	def _populate_constellations(self):
		self.constellations = []
		for directory in glob.glob(os.path.join(self._path, '*/')):
			path = os.path.join(self._path, directory)
			self.constellations.append(constellation.Constellation(path))


	def has_solarsystem(self, system):
		for con in self.constellations:
			if con.has_solarsystem(system):
				return True
		return False


	def get_solarsystem(self, system):
		for con in self.constellations:
			if con.has_solarsystem(system):
				return con.get_solarsystem(system)
		return None


	def has_constellation(self, name):
		for con in self.constellations:
			if con.name.lower() == name.lower():
				return True
		return False


	def get_constellation(self, name):
		for con in self.constellations:
			if con.name.lower() == name.lower():
				return con
		return None


	def __str__(self):
		#dump to json/dictionary
		pass


if __name__ == '__main__':
	import config
	region = os.path.join(config.SDE_PATH, 'fsd/universe/eve/BlackRise')
	test = Region(region)
	print(test.name)
	print(test.id)
	print(test.name_id)
	print(test.has_solarsystem('astoh'))
	print(test.get_solarsystem('astoh').name)
	print(test.has_constellation('aokinen'))
	print(test.get_constellation('aokinen').name)