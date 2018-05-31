#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
import sys
import os
import xml
import xml.etree.ElementTree
import copy
import argparse
import xml.etree.ElementTree as ET
from xml.dom import minidom

#print colored('hello', 'red'), colored('world', 'green')

class demolitionStage():
	def __init__(self, stage):
		self.stage = stage
		self.nuclides = []
		self.typeDemolition = 0
		self.DR = -1.0
		self.ARF = -1.0
		self.ARFdrop = -1.0
		self.ARFsize = 1.0
		self.LPF = -1.0
		self.RF = -1.0
		self.WindS = -1.0
		self.Wet = -1.0
		self.Density = -1.0
		self.Heigh = -1.0
		self.LPFdrop = -1.0
		
class InvalidTypeARF(Exception):
	pass

class LessZero(Exception):
	pass
	
class LessH(Exception):
	pass
	
class MoreOne(Exception):
	pass

def save_xml(filename, xml_code):
	xml_string = ET.tostring(xml_code).decode()

	xml_prettyxml = minidom.parseString(xml_string).toprettyxml()
	with open(filename, 'w') as xml_file:
		xml_file.write(xml_prettyxml)
		
def printErr(text):
	print 
	print "-"*80
	print text
	print "-"*80
	print 
	return
	
def printEq():
	print 
	print "="*80
	print
	return
	
"""
	#Вводим RF для ручной обработки и хранения
	RFdrop = xml.etree.ElementTree.Element("RFdrop")
	for RFpart, RFper in ([[0.0, 0.11],[2.5, 0.09],[5.0, 0.15],[10.0, 0.13],[15.0, 0.26],[30.0, 0.26]]):
		rf = xml.etree.ElementTree.SubElement(LPFdrop, "RF", partSize=str(RFpart))
		rf.text = "{0}".format(RFper)
	root.append(LPFdrop)
"""	
	

def createXML(allStages, oFileFolder, filename):
	root = xml.etree.ElementTree.Element("demolitionStage")
	for stageId, stage in enumerate(allStages):
		element = xml.etree.ElementTree.Element("stage")
		#Записываем номер стадии
		elStage = xml.etree.ElementTree.SubElement(element, "stageNumber")
		elStage.text = "stage {0}".format(stageId+1)
		
		#Записываем тип сноса
		if stage.typeDemolition == 1:
			elStage = xml.etree.ElementTree.SubElement(element, "typeOfDemolition", typeDem=str(stage.typeDemolition))
			elStage.text = "Demolition of Cell with Shears".format(stageId+1)
		elif stage.typeDemolition == 2:
			elStage = xml.etree.ElementTree.SubElement(element, "typeOfDemolition", typeDem=str(stage.typeDemolition))
			elStage.text = "Demolition of Cell with Explosive".format(stageId+1)
		
		#Записываем нуклиды
		elNuc = xml.etree.ElementTree.SubElement(element, "nuclides")
		for nucName, nucVal in stage.nuclides:
			nuc = xml.etree.ElementTree.SubElement(elNuc, "activity", nuclide=nucName)
			nuc.text = str(nucVal)
			
		#Записываем DR
		elDR = xml.etree.ElementTree.SubElement(element, "DR")
		elDR.text = "{0}".format(stage.DR)
		
		#Записываем ARF
		elARF = xml.etree.ElementTree.SubElement(element, "ARF")
		elSubARF = xml.etree.ElementTree.SubElement(elARF, "ARFdem")
		elSubARF.text = "{0}".format(stage.ARF)
		
		
		#Записываем AFRdrop
		if stage.Wet != -1:
			elSubARFdrop = xml.etree.ElementTree.SubElement(elARF, "ARFdrop")
			elSubARFdropWet = xml.etree.ElementTree.SubElement(elSubARFdrop, "Wettering")
			elSubARFdropWet.text = "{0}".format(stage.Wet)
			elSubARFdropWindS = xml.etree.ElementTree.SubElement(elSubARFdrop, "WindSpeed")
			elSubARFdropWindS.text = "{0}".format(stage.WindS)
		if stage.Density != -1:
			elSubARFdrop = xml.etree.ElementTree.SubElement(elARF, "ARFdrop", g="980")
			elSubARFdropD = xml.etree.ElementTree.SubElement(elSubARFdrop, "Density")
			elSubARFdropD.text = "{0}".format(stage.Density)
			elSubARFdropH = xml.etree.ElementTree.SubElement(elSubARFdrop, "Heigh")
			elSubARFdropH.text = "{0}".format(stage.Heigh)
		#Записываем множитель размера частиц для AFR
		elSubARFsize = xml.etree.ElementTree.SubElement(elARF, "ARFsize")
		elSubARFsize.text = "{0}".format(stage.ARFsize)
		
		#Записываем LPF
		elLPF = xml.etree.ElementTree.SubElement(element, "LPF")
		elLPFdem = xml.etree.ElementTree.SubElement(elLPF, "LPFdem")
		elLPFdem.text = "{0}".format(stage.LPF)

		#Вводим LPF для падения
		if stage.LPFdrop == 0.0:
			LPFdrop = xml.etree.ElementTree.SubElement(elLPF, "LPFdrop")
			for LPFpart, LPFper in ([[0.0, 0.95],[2.5, 0.60],[5.0, 0.30],[10.0, 0.25],[15.0, 0.25],[30.0, 0.25]]):
				lpf = xml.etree.ElementTree.SubElement(LPFdrop, "LPFp", partSize=str(LPFpart))
				lpf.text = "{0}".format(LPFper)
		elif (stage.LPFdrop != 0.0) and (stage.LPFdrop != -1.0):
			LPFdrop = xml.etree.ElementTree.SubElement(elLPF, "LPFdrop")
			LPFdrop.text = "{0}".format(stage.LPFdrop)
			

		#Записываем RF
		elRF = xml.etree.ElementTree.SubElement(element, "RF")
		elRFdem = xml.etree.ElementTree.SubElement(elRF, "RFdem")
		elRFdem.text = "{0}".format(stage.RF)
		
		#Вводим RF при защитных мерах
		if stage.LPFdrop == 0.0:
			RFdrop = xml.etree.ElementTree.SubElement(elRF, "RFdrop")
			for RFpart, RFper in ([[0.0, 0.72],[2.5, 0.24],[5.0, 0.02],[10.0, 0.009],[15.0, 0.0017],[30.0, 0.0017]]):
				rf = xml.etree.ElementTree.SubElement(RFdrop, "RFp", partSize=str(RFpart))
				rf.text = "{0}".format(RFper)
		elif (stage.LPFdrop != 0.0) and (stage.LPFdrop != -1.0):
			elRFdrop = xml.etree.ElementTree.SubElement(elRF, "RFdrop")
			elRFdrop.text = "{0}".format(stage.RF)
		root.append(element)
	
	tree = xml.etree.ElementTree.ElementTree(root)
	try:
		tree.write(oFileFolder+"/"+filename, "UTF-8")
		save_xml(oFileFolder+"/norm_"+filename, root)
	except EnvironmentError as err:
		print "{0}: import error: {1}".format(os.path.basename(sys.argv[0]), err)
	return
	
def defStages():
	#Вводим количество этапов сноса
	printEq()
	numDem = 0
	while numDem == 0:
		try:
			numDem = raw_input("Enter number of demolitions stage ")
			t = type(numDem)
			numDem = int(numDem)
			if numDem<0:
				raise LessZero()
		except ValueError as err:
			numDem = 0
			printErr( "Error: Demolitions stage must be int, not {0}!".format(t))
		except LessZero as err:
			numDem = 0
			printErr("Error: Demolitions stage must be more than zero!")
	allStages = []
	#Цикл по всем этапам сноса
	for i in range(1, numDem+1):
		printEq()
		print "Processing stage {0}".format(i)
		print 
		demStage = demolitionStage(i)
		
		#Вводим тип сноса
		while demStage.typeDemolition == 0:
			try:
				demStage.typeDemolition = raw_input("Enter the type of demolition:\n\t1 - Demolition of Cell with Shears;\n\t2 - Demolition of Cell with Explosive.\n")
				t = type(demStage.typeDemolition)
				demStage.typeDemolition = int(demStage.typeDemolition)
				if demStage.typeDemolition not in [1,2]:
					printErr( "Error: The type of demolition must be 1 or 2!")
					demStage.typeDemolition = 0
			except ValueError:
				demStage.typeDemolition = 0
				printErr( "Error: The type of demolition must be int, not {0}".format(t))
		printEq()
		#Вводим количество нуклидов
		numNucl = 0
		while numNucl == 0:
			try:
				numNucl = raw_input("Enter the number of nuclides ")
				t = type(numNucl)
				numNucl = int(numNucl)
			except ValueError:
				numNucl = 0
				printErr( "Error: The number of nuclides must be int, not {0}".format(t))
		print
		#Вводим нуклиды		
		nuclides = []
		for j in range(1, numNucl+1):
			
			nameNucl = ""
			while nameNucl == "":
				try:
					nameNucl = raw_input("\tEnter the name of the nuclide {0} ".format(j))
					t = type(nameNucl)
					nameNucl = str(nameNucl)
				except ValueError: #Добавить проверку на совпадение в бд
					nameNucl = ""
					printErr( "Error: The name of nuclides must be str, not {0}".format(t))
					
			valNucl = 0.0
			while valNucl == 0.0:
				try:
					valNucl = raw_input("\tEnter the activity of the nuclide {0} ".format(nameNucl))
					t = type(valNucl)
					valNucl = float(valNucl)
				except ValueError: #Добавить ввод в граммах и перевод его в активность и наоборот
					valNucl = 0.0
					printErr( "Error: The activity of nuclides must be float")
			print
			nuclides.append([nameNucl,  valNucl])
			
			
		demStage.nuclides = nuclides
		
		printEq()
		#Вводим DR
		while demStage.DR == -1.0:
			print "Damage Ratio (DR)"
			try:
				if demStage.typeDemolition == 1:
					print "(Warning: Literary data 0.1<=DR<=0.9)"
					demStage.DR = raw_input("\nEnter the damage ratio ")
					t = type(demStage.DR)
					demStage.DR = float(demStage.DR)
					if demStage.DR>1:
						raise MoreOne()
				elif demStage.typeDemolition == 2:
					print "Warning: Literary data DR=0.5"
					demStage.DR = raw_input("\nEnter the damage ratio ")
					t = type(demStage.DR)
					demStage.DR = float(demStage.DR)
					if demStage.DR>1:
						raise MoreOne()
			except ValueError as err:
				demStage.DR = -1.0
				printErr( "Error: The damage ratio must be float, not {0}".format(t))
			except MoreOne as err:
				demStage.DR = -1.0
				printErr("Error: DR must be less than one")
		
		printEq()
		#Вводим ARF
		typeARF = 0.0
		print "Airborne Release Fraction (ARF) for demolition"
		while typeARF == 0.0:
			try:
				print "\nEnter: \n\t1 if you want to enter ARF manually; \n\t2 if you want to enter ARF using the program."
				typeARF = raw_input()
				t = type(typeARF)
				typeARF = int(typeARF)
				if typeARF not in [1,2]:
					raise InvalidTypeARF()
			except ValueError as arr:
				typeARF = 0.0
				printErr( "Error: The ARF type should be int, not {0}".format(t) )
			except InvalidTypeARF as err:
				typeARF = 0.0
				printErr( "Error: The ARF type should be 1 or 2")
				
		
		drop = False
		if typeARF == 1:	
			while demStage.ARF == -1.0:
				try:
					print #"\nWarning: Literary data 6*10^(-6)<=DR<=3*10^(-3)"
					demStage.ARF = raw_input("Enter ARF ")
					t = type(demStage.ARF)
					demStage.ARF = float(demStage.ARF)
					if demStage.ARF<0:
						raise LessZero()
					if demStage.ARF>1:
						raise MoreOne()
				except ValueError as err:
					demStage.ARF = -1.0
					printErr("Error: ARF must be float, not {0}!".format(t))
				except LessZero as err:
					demStage.ARF = -1.0
					printErr("Error: ARF must be more than zero!")
				except MoreOne as err:
					demStage.ARF = -1.0
					printErr("Error: ARF must be less than one!")
		elif typeARF == 2:
			typeFix = -1
			while typeFix == -1:
				try:
					print "Enter:\n\t0 - Demolition without the use of fixative;\n\t1 - Demolition with one coat of fixative;\n\t2 - Demolition with two coat of fixative."
					typeFix = raw_input()
					t = type(typeFix)
					typeFix = int(typeFix)
					if typeFix not in [0,1,2]:
						
						printErr("Value must be 0, 1 or 2, not {0}".format(typeFix))
						typeFix = -1
				except ValueError as err:
					typeFix = -1
					printErr("Error: Value must be int, not {0}!!!".format(t))
			valFix = [0.001, 0.0001, 0.00001]
			demStage.ARF = valFix[typeFix]

		#Определяем AFRdrop
		drop = None
		print "\nDetermine the ARF coefficient for the fall? [Y/n]"
		while drop == None:
			
			s = raw_input()
			if s in ["y", "Y", "Yes", "yes", "YES"]:
				drop = True
			elif s in ["n", "N", "no", "No", "NO", "not", "NOT", "Not"]:
				drop = False
			else:
				printErr("Try again")
		if drop:
			matType = -1
			while matType == -1:
				try:
					matType = raw_input("Enter:\n\t1 - To enter manually;\n\t2 - To enter using programm.\n")
					t = type(matType)
					matType = int(matType)
					if matType not in [1,2]:
						printErr( "Error: The type of enter must be 1 or 2!")
						matType = -1
				except ValueError:
					matType = -1
					printErr( "Error: The type of enter must be int, not {0}".format(t))
			
			if matType == 1:
				while demStage.ARFdrop == -1.0:
					try:
						print "Enter ARFdrop"
						demStage.ARFdrop = raw_input()
						t = type(demStage.ARFdrop)
						demStage.ARFdrop = float(demStage.ARFdrop)
						if demStage.ARFdrop > 1:
							raise MoreOne()
						if demStage.ARFdrop<0.0:
							raise LessZero()
					except ValueError as err:
						demStage.ARFdrop = -1.0
						printErr("Error: ARFdrop must be float, not {0}!".format(t))
					except LessZero as err:
						demStage.ARFdrop = -1.0
						printErr("Error: ARFdrop must be more than zero!")
					except MoreOne as err:
						demStage.ARFdrop = -1.0
						printErr("Error: ARFdrop must be less than one!")
			elif matType == 2:
				formType = -1
				while formType == -1:
					try:
						formType = raw_input("Enter:\n\t1 - To use the formula with wind and moisture;\n\t2 - To use a formula with height and density.\n")
						t = type(formType)
						formType = int(formType)
						if formType not in [1,2]:
							printErr( "Error: The type of formula must be 1 or 2!")
							formType = -1
					except ValueError:
						formType = -1
						printErr( "Error: The type of formula must be int, not {0}".format(t))
				if formType == 1:
					while demStage.WindS == -1.0:
						try:
							demStage.WindS = raw_input("Enter Wind speed in (m/s) ")
							t = type(demStage.WindS)
							demStage.WindS = float(demStage.WindS)
							if demStage.WindS<0.0:
								raise LessZero()
						except ValueError as err:
							demStage.WindS = -1.0
							printErr("Error: Wind speed must be float, not {0}!".format(t))
						except LessZero as err:
							demStage.WindS = -1.0
							printErr("Error: Wind speed must be more than zero!")
					while demStage.Wet == -1.0:
						try:
							demStage.Wet = raw_input("Enter Wetting in (%) ")
							t = type(demStage.Wet)
							demStage.Wet = float(demStage.Wet)
							if demStage.Wet<0.0:
								raise LessZero()
							if demStage.Wet>100.0:
								raise MoreH()
						except ValueError as err:
							demStage.Wet = -1.0
							printErr("Error: Wetting must be float, not {0}!".format(t))
						except LessZero as err:
							demStage.Wet = -1.0
							printErr("Error: Wetting must be more than zero!")
						except MoreH as err:
							demStage.Wet = -1.0
							printErr("Error: Wetting must be less than 100%!")
				elif formType == 2:
					while demStage.Heigh == -1.0:
						try:
							demStage.Heigh = raw_input("Enter Heigh in (sm) ")
							t = type(demStage.Heigh)
							demStage.Heigh = float(demStage.Heigh)
							if demStage.Heigh<0.0:
								raise LessZero()
						except ValueError as err:
							demStage.Heigh = -1.0
							printErr("Error: Heigh must be float, not {0}!".format(t))
						except LessZero as err:
							demStage.Heigh = -1.0
							printErr("Error: Heigh must be more than zero!")
					while demStage.Density == -1.0:
						try:
							demStage.Density = raw_input("Enter Density in (g/sm^3) ")
							t = type(demStage.Density)
							demStage.Density = float(demStage.Density)
							if demStage.Density<0.0:
								raise LessZero()
						except ValueError as err:
							demStage.Density = -1.0
							printErr("Error: Density must be float, not {0}!".format(t))
						except LessZero as err:
							demStage.Density = -1.0
							printErr("Error: Density must be more than zero!")
				#ARFdrop = [2.3e-06, 1.0e-06]
				#demStage.ARFdrop = ARFdrop[matType-1]

		sizeFlag = None
		while sizeFlag == None:
			print "\nConsider particle-size multiplier? Considerativity set to 1.0 [Y/n]"
			s = raw_input()
			if s in ["y", "Y", "Yes", "yes", "YES"]:
				sizeFlag = True
			elif s in ["n", "N", "no", "No", "NO", "not", "NOT", "Not"]:
				sizeFlag = False
			else:
				printErr("Try again")	

		if sizeFlag:
			size = -1.0
			while size == -1.0:
				try:
					print "Enter particle-size multiplier"
					size = raw_input()
					t = type(size)
					size = float(size)
					if size > 1:
						raise MoreOne()
					if size<0:
						raise LessZero()
				except ValueError as err:
					size = -1.0
					printErr("Error: Particle-size multiplier must be int, not {0}!".format(t))
				except LessZero as err:
					size = -1.0
					printErr("Error: Particle-size multiplier must be more than zero!")
				except MoreOne as err:
					size = -1.0
					printErr("Error: Particle-size multiplier must be less than one!")
			demStage.ARFsize = size
			
		printEq()
		print "Leak Path Factor (LPF)"
		print
		if demStage.typeDemolition == 2:
			LPF_Flag = None
			while LPF_Flag == None:
				print "Is the calculation at the time of the explosion? (Considerativity LPF set to 1.0) [Y/n]"
				s = raw_input()
				if s in ["y", "Y", "Yes", "yes", "YES"]:
					LPF_Flag = True
					demStage.LPF = 1.0
				elif s in ["n", "N", "no", "No", "NO", "not", "NOT", "Not"]:
					LPF_Flag = False
				else:
					printErr("Try again")
					
		#Вводим LPF
		
		while demStage.LPF == -1.0:
			try:
				if demStage.typeDemolition == 1:
					print "Warning: Literary data LPF=0.1-0.3\n"
				if demStage.typeDemolition == 2:
					print "Warning: Literary data LPF=0.1\n"
				demStage.LPF = raw_input("Enter the Leak Path Factor (LPF) for demolition " )
				t = type(demStage.LPF)
				demStage.LPF = float(demStage.LPF)
				if demStage.LPF > 1:
					raise MoreOne()
				if demStage.LPF<0:
					raise LessZero()
			except ValueError as err:
				demStage.LPF = -1.0
				printErr("Error: LPF must be int, not {0}!".format(t))
			except LessZero as err:
				demStage.LPF = -1.0
				printErr("Error: LPF must be more than zero!")
			except MoreOne as err:
				demStage.LPF = -1.0
				printErr("Error: LPF must be less than one!")
		
		if drop:
			print
			print "LPF for falling"
			LPFdropType = -1
			while LPFdropType == -1:
				try:
					LPFdropType = raw_input("Enter:\n\t1 - To enter LPFdrop manually;\n\t2 - To enter using programm (LPF distribution as a function of size).\n")
					t = type(LPFdropType)
					LPFdropType = int(LPFdropType)
					if LPFdropType not in [1,2]:
						printErr( "Error: The enter number must be 1 or 2!")
						LPFdropType = -1
				except ValueError:
					printErr( "Error: The enter number must be int, not {0}".format(t))	
			if LPFdropType == 1:
				while demStage.LPFdrop == -1.0:
					try:
						print "Enter LPFdrop"
						demStage.LPFdrop = raw_input()
						t = type(demStage.LPFdrop)
						demStage.LPFdrop = float(demStage.LPFdrop)
						if demStage.LPFdrop > 1:
							raise MoreOne()
						if demStage.LPFdrop<0.0:
							raise LessZero()
					except ValueError as err:
						demStage.LPFdrop = -1.0
						printErr("Error: LPFdrop must be float, not {0}!".format(t))
					except LessZero as err:
						demStage.LPFdrop = -1.0
						printErr("Error: LPFdrop must be more than zero!")
					except MoreOne as err:
						demStage.LPFdrop = -1.0
						printErr("Error: LPFdrop must be less than one!")
			elif LPFdropType == 2:
				demStage.LPFdrop = 0.0
		#Вводим RF
		printEq()
		print "Respirable Fraction (RF)"
		print "Warning: Literary data RF=1"
		while demStage.RF == -1.0:
			try:

				
				print 
				demStage.RF = raw_input("Enter the Respirable Factor (RF) ")
				t = type(demStage.RF)
				demStage.RF = float(demStage.RF)
				if demStage.RF > 1:
					raise MoreOne()
				if demStage.RF<0:
					raise LessZero()
			except ValueError as err:
				demStage.RF = -1.0
				printErr("Error: RF must be int, not {0}!".format(t))
			except LessZero as err:
				demStage.RF = -1.0
				printErr("Error: RF must be more than zero!")
			except MoreOne as err:
				demStage.RF = -1.0
				printErr("Error: RF must be less than one!")
		allStages.append(copy.deepcopy(demStage))
		del demStage
		printEq()
		
	return allStages

def readStages(iFilePath):
	allStages = []
	et = xml.etree.ElementTree.parse(iFilePath)
	root = et.getroot()
	stages = root.findall('stage')

	for stage in stages:
		
		stageNumber = stage.find('stageNumber')
		stageNumber = stageNumber.text.split(" ")[-1]
		demStage = demolitionStage(float(stageNumber))
		print stageNumber

		demStage.typeDemolition = int(stage.find("typeOfDemolition").attrib["typeDem"])
		nuclides = stage.find('nuclides')
		
		for nuclide in nuclides.findall('activity'):
			#print nuclide
			act = float(nuclide.text)
			nuc = nuclide.attrib["nuclide"]
			#print act, nuc
			demStage.nuclides.append([nuc, act])
		
		demStage.DR = float(stage.find("DR").text)
		
		ARF_SUM = stage.find("ARF_SUM")
		demStage.ARF = float(ARF_SUM.find("ARF").text)
		try:
			demStage.ARFdrop = float(ARF_SUM.find("ARFdrop").text)
			demStage.ARFsize = float(ARF_SUM.find("ARFsize").text)
		except AttributeError as err:
			pass
		
		demStage.LPF = float(stage.find("LPF").text)
		
		#print 	demStage.nuclides
		allStages.append(copy.deepcopy(demStage))
		del demStage
	
	return allStages
	
	
"""
class demolitionStage():
	def __init__(self, stage):
		self.stage = stage
		self.nuclides = []
		self.typeDemolition = 0
		self.typeDemolitionText = ""
		self.DR = -1.0
		self.ARF = -1.0
		self.ARFdrop = -1.0
		self.AFRsize = 1.0	
"""
def main(iFilePath, filename, oFileFolder):

	if iFilePath == "":
		allStages = defStages()
		#Создаем XML
		createXML(allStages, oFileFolder, filename)
	else:
		allStages = readStages(iFilePath)
		createXML(allStages, "./", "wow.xml")
	print "Done!"
	return
	
	
	
if __name__ == "__main__":
	try:
		mypath = os.path.dirname(os.path.abspath(__file__))
	except NameError:
		mypath = os.path.dirname(os.path.abspath(sys.argv[0]))
	os.chdir(mypath)
	#if len(sys.argv) == 1: sys.argv[1:] = ["-h"]
	parser = argparse.ArgumentParser()
	parser._action_groups.pop()
	required = parser.add_argument_group('required arguments')
	optional = parser.add_argument_group('optional arguments')
	
	optional.add_argument('--ifp', action = 'store', dest='iFilePath',  type=str, help='Path to input file (with name)', required=False, default = "")
	optional.add_argument('--fName', action = 'store', dest='filename',  type=str, help='Output filename', required=False, default = "new_xml")
	optional.add_argument('--ofnf', action = 'store', dest='oFileNewFolder',metavar='NEW_FOLDER', type=str, help='path to the new output folder for output files', required=False, default=mypath)
	
	args_new = parser.parse_args()
	oFileNewFolder = args_new.oFileNewFolder
	iFilePath = args_new.iFilePath
	if oFileNewFolder != mypath:
		try:
			os.makedirs(oFileNewFolder)
		except OSError as err:
			print "Warning! {0}".format(err)
	filename = args_new.filename
	filename = filename+".xml"
	sys.exit(main(iFilePath, filename, oFileNewFolder))
