#!/usr/bin/python3

import os
import yaml

import regional

class Solarsystem(regional.Regional):
	"""docstring for Solarsystem"""
	def __init__(self, path_to_solarsystem):
		regional.Regional.__init__(self, path_to_solarsystem)
		self.name_id = self._content['solarSystemNameID']


if __name__ == '__main__':
	import config
	solarsystem = os.path.join(config.SDE_PATH, 'fsd/universe/eve/BlackRise/Aokinen/Ahtila')
	test_system = Solarsystem(solarsystem)
	print(test_system.name)
	print(test_system.name_id)
