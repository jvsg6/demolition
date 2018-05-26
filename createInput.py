#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
import sys
import os
import xml

class demolitionStage():
	def __init__(self, stage):
		self.stage = stage
		self.nuclides = {}
	


def main():
	numDem = 0
	while numDem == 0:
		try:
			numDem = int(raw_input("Enter number of demolitions stage "))
		except ValueError:
			print "Error: Demolitions stage must be int"
			print
	for i in range(1, numDem+1):
		print "Processing stage {0}".format(i)
		print 
		demStage = demolitionStage(i)
		numNucl = 0
		while numNucl == 0:
			try:
				numNucl = int(raw_input("Enter the number of nuclides "))
			except ValueError:
				print "Error: The number of nuclides must be int"
				print
		for j in range(1, numNucl+1):
			nuclides = {}
			nameNucl = ""
			while nameNucl == "":
				try:
					nameNucl = str(raw_input("Enter the name of the nuclide {0} ".format(j)))
				except ValueError: #Добавить проверку на совпадение в бд
					print "Error: The name of nuclides must be str"
					print
					
			valNucl = 0.0
			while valNucl == 0.0:
				try:
					valNucl = float(raw_input("Enter the activity of the nuclide {0} ".format(nameNucl)))
				except ValueError: #Добавить ввод в граммах и перевод его в активность и наоборот
					print "Error: The activity of nuclides must be float"
					print
			nuclides.update({nameNucl : valNucl})
		demStage.nuclides = nuclides
					
		
	print "Done!"
	return
	
	
	
if __name__=="__main__":
	sys.exit(main())
