#!/usr/bin/python3

import os
import yaml

import regional

class Solarsystem(regional.Regional):
	"""TODO"""
	def __init__(self, path_to_solarsystem):
		regional.Regional.__init__(self, path_to_solarsystem)
		self.name_id = self._content['solarSystemNameID']
		self.id = self._content['solarSystemID']
		self.security = round(self._content['security'], 1)
		# will need station data eventually \


	def __str__(self):
		#TODO dump to dictionary/json
		pass


if __name__ == '__main__':
	import config
	solarsystem = os.path.join(config.SDE_PATH, 'fsd/universe/eve/BlackRise/Aokinen/Ahtila')
	test_system = Solarsystem(solarsystem)
	print(test_system.name)
	print(test_system.name_id)
	print(test_system.id)
	print(test_system.security)
	print(test_system.to_dict())