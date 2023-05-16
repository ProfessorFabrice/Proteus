#!/usr/bin/python3

##
# LDI 2008
# Fabrice Issac
# Classe Proteus
##
# moteur de proteus

import ply.lex as lex
import codecs
import sys
import re
from Proteus import Proteus
from ProtException import *

class ProteusAna(Proteus):
	# analyseur tolérant	
	def setTolerant(self,val):
		self.tolerant = val

	# methodes de manipulation
	
	def empile(self,nb):
		if self.verb: print ("DEPILE ")	
		for i in range(1,int(nb)):
			self.entree = self.entree + self.pile[0]
			self.pile = self.pile[1:]

	def depile(self,nb):
		if self.verb: print ("EMPILE ")
		for i in range(1,nb):
			self.pile = self.entree[-1] + self.pile
			self.entree = self.entree[:-1]

	def efface(self,chaine):
		if self.verb: print ("AJOUTE ("+chaine+")")
		self.entree = self.entree+ chaine[::-1]
		#self.entree = self.entree+chaine[:-1]

	def ajout(self,chaine,succ):
		if self.verb: print ("SUPPRIME ("+chaine+")")
		if len(chaine)>0:
			if succ == '[':
				if self.entree.startswith(chaine):
					self.entree = self.entree[len(chaine):]
				else:
					if not self.tolerant:
						raise AnaError("Supp1: "+chaine)
			else:
				if self.entree.endswith(chaine):
					self.entree = self.entree[:-len(chaine)]
				else:
					if not self.tolerant:
						raise AnaError("Supp2: "+chaine)

	def vide(self):
		if self.verb: print ("VIDE ")
		self.entree = self.entree + self.pile
		self.pile = ""
		
	def rempli(self):
		if self.verb: print ("REMPLI ")
		
	def declone(self):
		if self.verb: print ("DECLONE ")
		if self.entree[-1] == self.entree[-2]:
			self.entree = self.entree[:-1]
		else:
			raise AnaError("DECLONE: "+self.entree)
		

	def action(self):
		for pos in range(len(self.pileres),0,-1):
			elt = self.pileres[pos-1]
			try:
				succ = self.pileres[pos-2][0]
			except:
				succ = ''
			if elt[0] == 'P': self.empile(elt[2])
			elif elt[0] == 'D': self.depile(elt[1])
			elif elt[0] == 'E': self.efface(elt[1])
			elif elt[0] == '[': self.vide()
			elif elt[0] == 'A':self.ajout(elt[1],succ)
			elif elt[0] == ']': self.rempli()
			elif elt[0] == 'C': self.declone()
			if self.verb: print (self.entree+ " <> "+ self.pile)
		self.vide()

	# Test it output
	def transforme(self,code,entree):
		self.entree = entree
		self.pile = ""
		self.pileres = []
		self.lexer.input(code)
		while 1:
			tok = self.lexer.token()
			if not tok: break
			print (tok)
		self.action()
		return self.entree

