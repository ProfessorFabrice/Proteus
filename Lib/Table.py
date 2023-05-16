#!/usr/bin/python
# -*- coding: utf8 -*- 

##
# LDI 2008
# Fabrice Issac
# Classe Table
##
# Object content tables


class Table(object):
	def __init__(self,ident,name,code,info):
		self.ident = ident
		self.name = name
		self.code = code
		self.info = info
		self.typen = ""
	
	# accesseurs
	# identifiant
	def getIdent(self):
		return self.ident
	
	def putIdent(self,ident):
		self.ident = ident
	# name	
	def getName(self):
		return self.name
	
	def putName(self,name):
		self.name = name
	# code	
	def getCode(self):
		return self.code
	
	def putCode(self,code):
		self.code = code
	# info	
	def getInfo(self):
		return self.info
	
	def putInfo(self,info):
		self.info = info
		
	# type	
	def getType(self):
		return self.typen
	
	def putType(self,typen):
		self.typen = typen
		
