#!/usr/bin/python3

##
# Fabrice Issac
# Classe Proteus
##

class AnaError(Exception):
	def __init__(self, value):
		self.value = value

	def __str__(self):
		return repr(self.value)
		


