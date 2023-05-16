#!/usr/bin/python3

##
# LDI 2008
# Fabrice Issac
# Classe Analyse
##
#

import re
import sys
import xml.dom.minidom
import glob

from LectureTable import LectureTable
from ProteusAna import ProteusAna
from ProteusGen import ProteusGen
from ProtException import *

class Analyse:
	def __init__(self,tablecode,tablelemme=""):
		self.tablecode = tablecode
		self.tablelemme = tablelemme
		self.lect = LectureTable(tablecode)
		self.lect.lectureTable()
		self.listeTable = self.lect.listeTable
		self.pa = ProteusAna()
		self.pa.setTolerant(False)
		self.pa.build()
		self.pg = ProteusGen()
		self.pg.build()
		self.tlemme = {}
		if self.tablelemme != "":
			self.lectureLemmes()
		self.lect.calcLstCode()
		
	def lectureLemmes(self):
		fic = open(self.tablelemme)
		for l in fic:
			try:
				[l,c] = l.rstrip().split('\t')
			except:
				l = l.rstrip()
				c = "Vm----"
			self.tlemme[l] = c
	

	# lancement analyse pour un mot
	def analyse(self,mot):
		tabresl = []
		tabres = {}
		for t in self.lect.listeTable:
			c = t.getCode() 
			#print(c)
			infos = t.getInfo()
			ident = t.getIdent()
			try:
				res = self.pa.transforme(c,mot)
				for cat in self.lect.getName(c):
					if res in self.tlemme:# and self.tlemme[res][0] == cat[0]:
						k = res+cat
						if k not in tabres:
							tabresl.append({'l':res,'c':cat,'r':c})
							tabres[k] = 1
					else:
						pass
			except AnaError as toto:
				pass
		return tabresl
	
	#def afficheTable(self,ident):
	def etiqListe(self,nomfic):
		fic = open(nomfic)
		while 1:
			l = fic.readline().split('\t')
			if (l[0]==""):
				break
			print(l[0]+'\t',end=" ")
			res = self.analyse(l[0])
			if len(res)>0:
				elt = res.pop(0)
				le = elt['l']
				for elt in res:
					if len(elt['l'])<len(le):
						le = elt['l']
				print (le.encode('utf-8'))
			else:
				print ("INC")

	def nbEtiqListe(self,nomfic):
		fic = open(nomfic)
		while 1:
			l = fic.readline().split('\t')
			if (l[0]==""):
				break
			print (l[0]+'\t',end="")
			res = self.analyse(l[0])
			print (len(res))

		

if __name__ == '__main__':
	table = sys.argv[1]
	lemme = sys.argv[2]
	try:
		listemots = open(sys.argv[3])
	except:
		listemots = sys.stdin
	ana = Analyse(table,lemme)
	for i in listemots:
		m = i.rstrip()
		res = ana.analyse(m)
		#sys.stdout.write("<token>\n\t<w>"+m+"</w>\n\t<morph>\n")
		print(m+" :")
		for elt in res:
			#print(m+"\t"+elt+"\t"+res[elt])
			print("\t"+elt["l"]+"\t"+elt["c"])
			#sys.stdout.write('\t\t<item c="'+elt["c"]+'" l="'+elt["l"]+'"')
			#sys.stdout.write(' r="'+elt["r"]+'"')
			#sys.stdout.write('/>\n')
		#sys.stdout.write("\t</morph>\n</token>\n")
	#print ana.analyse('remanger')
	
