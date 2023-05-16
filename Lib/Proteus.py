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

class Proteus(object):
	
	def __init__(self):
		self.entree = ""
		self.code = ""
		self.pile = ""
		self.nombre = 2
		self.verb = False
		self.pileres = []
		self.tolerant = False
		
	tokens = (
		'NUMBER',
		'AJOUT',
		'EMPILE',
		'DEPILE',
		'EFFACE_EXPLICITE',
		'EFFACE',
		'VIDE',
		'REMPLI',
		'SUPPRIME'
		)

	# enleve un caractere a droite du mot et l'ajoute a la pile
	def t_EMPILE(self,t):
		r'P(\|.\|)?'
		if re.search('|',t.value):
			res = t.value[2:-1]
		else:
			res = ''
		self.pileres.append(['P',res,self.nombre])
		self.nombre = 2
		
	# clone le dernier caractere du mot
	def t_CLONE(self,t):
		r'C'
		self.pileres.append(['C'])
		
	# depile un caractere et l'ajoute a la droite du mot	
	def t_DEPILE(self,t):
		r'D'
		self.pileres.append(['D',self.nombre])
		self.nombre = 2
		
	# efface du mot des caracteres 	(attention cette commande est assimile a un empilement suivi d'un effacement
	# dans la pile) (pour effacer "bonjour" faire "/ruojnob/")
	def t_EFFACE_EXPLICITE(self,t): 
		r'\\([^/\\]|\\/|\\\\)*\\'
		self.pileres.append(['E',re.sub(r"\\\\","\\\\",t.value[1:-1]),self.nombre])
		self.nombre = 2	
		
	# efface un caractere du mot
	def t_EFFACE(self,t): 
		r'E'
		self.pileres.append(['E','.',self.nombre])
		self.nombre = 2	
		
	# depile toute la pile
	def t_VIDE(self,t): 
		r'\[|V'
		self.pileres.append(['['])
	
	# identifie un nombre entier
	def t_NUMBER(self,t):
		r'\d+'
		self.nombre = int(t.value) + 1 
	
	# ajoute au mot des caracteres
	def t_AJOUT(self,t):
		r'/([^/\\]|\\/|\\\\)*/'
		self.pileres.append(['A',re.sub(r"\\\\","\\\\",re.sub("\\\/","/",t.value[1:-1]))])
	
	# met tout le mot dans la pile
	def t_REMPLI(self,t):
		r'\]|R'
		self.pileres.append([']'])
		
	# supprime toute la pile
	def t_SUPPRIME(self,t):
		r'S'
		self.pileres.append(['S'])
		
	# A string containing ignored characters (spaces and tabs)
	t_ignore  = ' \t'

	# Error handling rule
	def t_error(self,t):
		print ("Illegal character '"+t.value[0]+"' dans '"+self.code+"'" )
		t.lexer.skip(1)

	# Build the lexer
	def build(self,**kwargs): 
		self.lexer = lex.lex(object=self, **kwargs)


