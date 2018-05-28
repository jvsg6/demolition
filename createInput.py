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
from termcolor import colored
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
class InvalidTypeARF(Exception):
	pass

class LessZero(Exception):
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
		elARF = xml.etree.ElementTree.SubElement(element, "ARF_SUM")
		elSubARF = xml.etree.ElementTree.SubElement(elARF, "ARF")
		elSubARF.text = "{0}".format(stage.ARF)
		#Записываем AFRdrop
		if stage.ARFdrop != -1:
			elSubARFdrop = xml.etree.ElementTree.SubElement(elARF, "ARFdrop")
			elSubARFdrop.text = "{0}".format(stage.ARFdrop)
			
		#Записываем множитель размера частиц для AFR
		elSubARFsize = xml.etree.ElementTree.SubElement(elARF, "ARFsize")
		elSubARFsize.text = "{0}".format(stage.ARFsize)
		
		#Записываем LPF
		elLPF = xml.etree.ElementTree.SubElement(element, "LPF")
		elLPF.text = "{0}".format(stage.LPF)
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
			numDem = raw_input(colored("Enter number of demolitions stage ", "green"))
			t = type(numDem)
			numDem = int(numDem)
			if numDem<0:
				raise LessZero()
		except ValueError as err:
			printErr( "Error: Demolitions stage must be int, not {0}!".format(t))
		except LessZero as err:
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
				demStage.typeDemolition = raw_input("Enter the type of demolition:\n1 - Demolition of Cell with Shears;\n2 - Demolition of Cell with Explosive.\n")
				t = type(demStage.typeDemolition)
				demStage.typeDemolition = int(demStage.typeDemolition)
				if demStage.typeDemolition not in [1,2]:
					printErr( "Error: The type of demolition must be 1 or 2!")
					demStage.typeDemolition = 0
			except ValueError:
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
				printErr( "Error: The number of nuclides must be int, not {0}".format(t))
		print
		#Вводим нуклиды		
		nuclides = []
		for j in range(1, numNucl+1):
			
			nameNucl = ""
			while nameNucl == "":
				try:
					nameNucl = raw_input("Enter the name of the nuclide {0} ".format(j))
					t = type(nameNucl)
					nameNucl = str(nameNucl)
				except ValueError: #Добавить проверку на совпадение в бд
					printErr( "Error: The name of nuclides must be str, not {0}".format(t))
					
			valNucl = 0.0
			while valNucl == 0.0:
				try:
					valNucl = raw_input("Enter the activity of the nuclide {0} ".format(nameNucl))
					t = type(valNucl)
					valNucl = float(valNucl)
				except ValueError: #Добавить ввод в граммах и перевод его в активность и наоборот
					printErr( "Error: The activity of nuclides must be float")
			nuclides.append([nameNucl,  valNucl])
			
			
		demStage.nuclides = nuclides
		
		printEq()
		#Вводим DR
		while demStage.DR == -1.0:
			try:
				if demStage.typeDemolition == 1:
					print "Warning: Literary data 0.1<=DR<=0.9"
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
				printErr( "Error: The damage ratio must be float, not {0}".format(t))
			except MoreOne as err:
				demStage.DR = -1.0
				printErr("Error: DR must be less than one")
		
		printEq()
		#Вводим ARF
		typeARF = 0.0
		while typeARF == 0.0:
			try:
				print "\nEnter: \n1 if you want to enter ARF manually; \n2 if you want to enter ARF using the program."
				typeARF = raw_input()
				t = type(typeARF)
				typeARF = int(typeARF)
				if typeARF not in [1,2]:
					raise InvalidTypeARF()
			except ValueError as arr:
				printErr( "Error: The ARF type should be int, not {0}".format(t) )
			except InvalidTypeARF as err:
				printErr( "Error: The ARF type should be 1 or 2")
		
		
		if typeARF == 1:	
			while demStage.ARF == -1.0:
				try:
					print "\nWarning: Literary data 6*10^(-6)<=DR<=3*10^(-3)"
					demStage.ARF = raw_input("Enter ARF ")
					t = type(demStage.ARF)
					demStage.ARF = float(demStage.ARF)
					if demStage.ARF<0:
						raise LessZero()
					if demStage.ARF>1:
						raise MoreOne()
				except ValueError as err:
					demStage.ARF = -1.0
					printErr("Error: ARF must be int, not {0}!".format(t))
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
					print "Enter:\n0 - Demolition without the use of fixative;\n1 - Demolition with one coat of fixative;\n2 - Demolition with two coat of fixative."
					typeFix = raw_input()
					t = type(typeFix)
					typeFix = int(typeFix)
					if typeFix not in [0,1,2]:
						
						printErr("Value must be 0, 1 or 2, not {0}".format(typeFix))
						typeFix = -1
				except ValueError as err:
					printErr("Error: Value must be int, not {0}!!!".format(t))
			valFix = [0.001, 0.0001, 0.00001]
			demStage.ARF = valFix[typeFix]
			if demStage.typeDemolition == 1:
				drop = None
				while drop == None:
					print "Consider falling? [Y/n]"
					s = raw_input()
					if s in ["y", "Y", "Yes", "yes", "YES", "д", "Д", "да", "ДА"]:
						drop = True
					elif s in ["n", "N", "no", "No", "NO", "н", "Н", "Нет", "НЕТ", "нет", "not", "NOT", "Not"]:
						drop = False
					else:
						printErr("Try again")
				if drop:
					matType = -1
					while matType == -1:
						try:
							matType = raw_input("Enter the type of material:\n1 - Concrete;\n2 - Sheet methal.\n")
							t = type(matType)
							matType = int(matType)
							if matType not in [1,2]:
								printErr( "Error: The type of material must be 1 or 2!")
								matType = -1
						except ValueError:
							printErr( "Error: The type of material must be int, not {0}".format(t))
					ARFdrop = [2.3e-06, 1.0e-06]
					demStage.ARFdrop = ARFdrop[matType-1]
					
					
			elif demStage.typeDemolition == 2:
				trash = None
				while trash == None:
					print "Consider garbage collection? [Y/n]"
					s = raw_input()
					if s in ["y", "Y", "Yes", "yes", "YES"]:
						trash = True
					elif s in ["n", "N", "no", "No", "NO", "not", "NOT", "Not"]:
						trash = False
					else:
						printErr("Try again")
				if trash:
					demStage.ARFdrop = 2.3e-06
		sizeFlag = None
		while sizeFlag == None:
			print "Consider particle-size multiplier? Considerativity set to 1.0 [Y/n]"
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
		while demStage.LPF == -1.0:
			try:
				if demStage.typeDemolition == 1:
					print "Warning: Literary data LPF=0.1-0.3"
				if demStage.typeDemolition == 2:
					print "Warning: Literary data LPF=0.1"
				print colored("Enter the Leak Path Factor (LPF)", 'green')
				demStage.LPF = raw_input()
				t = type(demStage.LPF)
				demStage.LPF = float(demStage.LPF)
				if demStage.LPF > 1:
					raise MoreOne()
				if demStage.LPF<0:
					raise LessZero()
			except ValueError as err:
				demStage.LPF = -1.0
				printErr("Error: Particle-size multiplier must be int, not {0}!".format(t))
			except LessZero as err:
				demStage.LPF = -1.0
				printErr("Error: Particle-size multiplier must be more than zero!")
			except MoreOne as err:
				demStage.LPF = -1.0
				printErr("Error: Particle-size multiplier must be less than one!")
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
