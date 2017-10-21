#!/usr/bin/python3

import os
import yaml

import regional
import solarsystem

class Constellation(regional.Regional):
	"""docstring for Constellation"""
	def __init__(self, path_to_constellation):
		regional.Regional.__init__(self,path_to_constellation)
		self._path = path_to_constellation
		self.name_id = self._content['nameID']
		self._populate_solarystems()

	def _populate_solarystems()
		self.solarsystems = []
		for root, directory, _ in os.path.walk(self._path):
			pass
			#for every dir make a solar system and add it to the list of solars

	def has_solarsystem(name):
		for solar in solarsystems:
			if solar.name == name:
				return True
		return False