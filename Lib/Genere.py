#!/usr/bin/python3

##
# LDI 2008
# Fabrice Issac
# Classe Genere
##
# generation de flexions

import re
import sys
import string
from LectureTable import LectureTable
from ProteusGen import ProteusGen

class Genere(object):
	def __init__(self,reptable):
		lt = LectureTable(reptable)
		lt.lectureTable()
		self.listeTable = lt.listeTable
		self.pg = ProteusGen()
		self.pg.build()
	
	def flex(self,ident,mot):
		res = []
		msg = 'mot='+mot+' code='+ident+'\n'
		for elt in self.listeTable:
			if re.search(ident,elt.getIdent()):
				forme = self.pg.transforme(elt.getCode(),mot)
				res.append([forme,elt.getName(),elt.getIdent()]) # hack pour supprimer \ufeff au début
		return res

if __name__ == '__main__':
	g = Genere(sys.argv[1])
	fic = open(sys.argv[2])
	fout = sys.stdout
	for l in fic:
		try:
			ligne = l.rstrip()
			if ligne != "":
				if ligne[0] != "#":
					[lemme,code] = ligne.split('\t')
					fout.write("\t".join([lemme,lemme,code,"Pr"])+"\n")
					for elt in g.flex(code,lemme):
						fout.write("\t".join([elt[0],lemme,elt[1],"Pr"])+"\n")
		except:
			raise
			break
	
	
