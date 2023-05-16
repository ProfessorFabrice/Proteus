#!/usr/bin/python3
##
# LDI 2008
# Fabrice Issac
# Classe LectureTable
##
# lecture des tables de flexion

import re
import sys
import xml.dom.minidom
import glob
import os

from ProteusAna import ProteusAna
from ProteusGen import ProteusGen
from Table import Table

class LectureTable:
	def __init__(self,ficCode):
		self.ficCode = ficCode
		self.listeTable = []
		self.tbl = None
		self.pg = ProteusGen()
		self.pg.build()
		self.listeId = {}
		self.listeCode = {}
			
	def lectureTable(self):
		self.listeFlexTotal = []
		self.lectTableRec(self.ficCode)
		for noeudFlex in self.listeFlexTotal:
			if noeudFlex.getAttribute('type') == 'final':
				noeudId = noeudFlex.getAttribute('id')
				for elt in self.tabCode(noeudId):
					self.listeTable.append(elt)
	
	def lectTableRec(self,rep):
		for elt in glob.glob(rep+"/*"):
			if os.path.isdir(elt):
				self.lectTableRec(elt)
		for fic in glob.glob(rep+'/*.xml'):
			tbl = xml.dom.minidom.parse(fic)
			# lecture flex
			listeFlex = tbl.getElementsByTagName('flex')
			for fl in listeFlex:
				self.listeId[fl.getAttribute('id')] = fl
			self.listeFlexTotal = self.listeFlexTotal + listeFlex
			# lecture des masques
			listeMask = tbl.getElementsByTagName('mask')
			for ms in listeMask:
				self.listeId[ms.getAttribute('id')] = ms
	
			
	# retourne un tableau de code par rapport a un identifiant
	def tabCode(self,ident):
		noeud = self.listeId[ident]
		typenoeud = noeud.getAttribute('type')
		ident = noeud.getAttribute('id')
		name = self.getTextNode(noeud,'name')
		info = self.getTextNode(noeud,'info')
		if typenoeud == 'nonterm' or typenoeud == 'final':
			opnoeudtab = noeud.getElementsByTagName('op')
			listecoderes = []
			for opnoeud in opnoeudtab:
				optype = opnoeud.getAttribute('type')
				if optype == 'mask':
					idop = opnoeud.getAttribute('value')
					lcr = self.tabCode(idop)
					for item in opnoeud.getElementsByTagName('item'):
						lcr = self.getMask(item.getAttribute('value'),lcr)
				elif optype == 'add': # add
					listeNoeudItem = opnoeud.getElementsByTagName('item')
					lcr = []
					for lni in listeNoeudItem:
						lcr = lcr + self.tabCode(lni.getAttribute('value'))
				listecoderes = listecoderes + lcr
		elif typenoeud == 'term': # term
			listecoderes = []
			for fl in noeud.getElementsByTagName('flex'):
				identInt = fl.getAttribute('id')
				nameInt = self.getTextNode(fl,'name')
				code  = self.getTextNode(fl,'code')
				infoInt = self.getTextNode(fl,'info')
				listecoderes.append(Table(identInt,nameInt,code,infoInt))
		for i in range(0,len(listecoderes)):
			listecoderes[i].putIdent(ident+ '.' + listecoderes[i].getIdent())
			listecoderes[i].putName(name + listecoderes[i].getName())
			listecoderes[i].putInfo(info + listecoderes[i].getInfo())
			listecoderes[i].putType(typenoeud)
		return listecoderes
	
	
	def getMask(self,ident,lcr):
		noeud = self.listeId[ident]
		for item in noeud.getElementsByTagName('item'):
			ervalue = item.getAttribute('ervalue')
			textecode = item.firstChild.nodeValue
			for i in range(0,len(lcr)):
				if re.search(ervalue,lcr[i].getIdent()):
					lcr[i].putCode(self.pg.transforme(textecode,lcr[i].getCode()))
		return lcr

	# transforme tables
	def calcLstCode(self):
		self.listeCode = {}
		for elt in self.listeTable:
			try:
				if not elt.getCode() in self.listeCode:
					self.listeCode[elt.getCode()].append(elt.getName())
			except:
				self.listeCode[elt.getCode()] = []
				self.listeCode[elt.getCode()].append(elt.getName())
		try:
			del self.listeCode["]S"]
		except:
			pass
	
	def getLstCode(self):
		return self.listeCode
		
	def getName(self,code):
		return self.listeCode[code]
	
	# fonctions utilitaires
	def getTextNode(self,noeud,tag):
		try:
			val = noeud.getElementsByTagName(tag)[0].firstChild.nodeValue
		except:
			val= ""
		return val
			
if __name__ == '__main__':
	table = sys.argv[1]
	ana = LectureTable(table)
	ana.lectureTable()
	for elt in ana.listeTable:
		if elt.getType() == 'final':
			print(elt.getName(),end="\t")	
			print(elt.getIdent(),end="\t")	
			print(elt.getInfo(),end="\t")	
			print(elt.getCode())

