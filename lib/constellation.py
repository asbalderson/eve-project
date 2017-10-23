#!/usr/bin/python3

import os
import yaml

import regional
import solarsystem

class Constellation(regional.Regional):
	"""docstring for Constellation"""
	def __init__(self, path_to_constellation):
		regional.Regional.__init__(self,path_to_constellation)
		self.name_id = self._content['nameID']
		self.id = self._content['constellationID']
		self._populate_solarystems()


	def _populate_solarystems(self):
		self.solarsystems = []
		for root, directorys, _ in os.walk(self._path):
			for d in directorys:
				path = os.path.join(root, d)
				self.solarsystems.append(solarsystem.Solarsystem(path))


	def has_solarsystem(self, name):
		for solar in self.solarsystems:
			if solar.name.lower() == name.lower():
				return True
		return False


	def get_solarsystem(self, name):
		for solar in self.solarsystems:
			if solar.name.lower() == name.lower():
				return solar
		return None


if __name__ == '__main__':
	import config
	constellation = os.path.join(config.SDE_PATH, 'fsd/universe/eve/BlackRise/Aokinen')
	test_system = Constellation(constellation)
	print(test_system.name)
	print(test_system.name_id)
	print(test_system.has_solarsystem('false'))
	print(test_system.has_solarsystem('tsuruma'))
	print(test_system.get_solarsystem('astoh').name)