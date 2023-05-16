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
from Proteus import Proteus

class ProteusGen(Proteus):
	
	# methodes de manipulation
	
	def empile(self,sep,nb):
		if self.verb: print ("EMPILE ")	
		for i in range(1,nb):
			if sep != '':
				try:
					while self.entree[-1] != sep:
						self.pile = self.entree[-1] + self.pile
						self.entree = self.entree[:-1]
				except:
						pass	
			self.pile = self.entree[-1] + self.pile
			self.entree = self.entree[:-1]

	def depile(self,nb):
		if self.verb: print ("DEPILE ")
		#print("pile="+str(self.pile),self.entree)
		for i in range(1,nb):
			self.entree = self.entree + self.pile[0]
			self.pile = self.pile[1:]

	# efface le nombre de caractere correpondant a la longueur de la chaine "chaine"
	def efface(self,chaine,nb):
		if self.verb: print ("EFFACE ("+chaine+","+str(nb)+")")
		for j in range(1,nb):
			for i in range(1,len(chaine)+1):
				self.entree = self.entree[:-1]

	def vide(self):
		if self.verb: print ("VIDE ")
		self.entree = self.entree + self.pile
		self.pile = ""

	def ajout(self,chaine):
		if self.verb: print ("AJOUT ")
		self.entree = self.entree + chaine
		
	def rempli(self):
		if self.verb: print ("REMPLI")
		self.pile = self.entree + self.pile
		self.entree = ""
		
	def supprime(self):
		if self.verb: print ("SUPPRIME")
		self.pile = ""
		
	def clone(self):
		if self.verb: print ("CLONE")
		self.entree = self.entree + self.entree[-1]
		
	# appel des methodes

	def action(self):
		for elt in self.pileres:
			if elt[0] == 'P': self.empile(elt[1],elt[2])
			elif elt[0] == 'D': self.depile(elt[1])
			elif elt[0] == 'E': self.efface(elt[1],elt[2])
			elif elt[0] == '[': self.vide()
			elif elt[0] == 'A': self.ajout(elt[1])
			elif elt[0] == ']': self.rempli()
			elif elt[0] == 'S': self.supprime()
			elif elt[0] == 'C': self.clone()
			if self.verb: print (self.entree+ " <> "+ self.pile)

	# Test it output
	def transforme(self,code,entree):
		self.entree = entree
		self.pile = ""
		self.pileres = []
		#print("Transforme="+code+" "+entree)
		self.lexer.input(code)
		while 1:
			tok = self.lexer.token()
			if not tok: break
			print (tok)
		self.action()
		return self.entree
		
if __name__ == '__main__':
	pg = ProteusGen()
	pg.build()
	pg.transforme("]/\\c\\/D/ç/[","\c\/ons/")
