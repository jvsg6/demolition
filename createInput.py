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
class demolitionStage():
	def __init__(self, stage):
		self.stage = stage
		self.nuclides = []
		self.typeDemolition = 0
		self.DR = 0
	

def save_xml(filename, xml_code):
	xml_string = ET.tostring(xml_code).decode()

	xml_prettyxml = minidom.parseString(xml_string).toprettyxml()
	with open(filename, 'w') as xml_file:
		xml_file.write(xml_prettyxml)

def createXML(allStages, oFileFolder, filename):
	root = xml.etree.ElementTree.Element("demolitionStage")
	for stageId, stage in enumerate(allStages):
		element = xml.etree.ElementTree.Element("stage")
		
		elStage = xml.etree.ElementTree.SubElement(element, "stageNumber")
		elStage.text = "stage {0}".format(stageId+1)
		
		if stage.typeDemolition == 1:
			elStage = xml.etree.ElementTree.SubElement(element, "typeOfDemolition", typeDem=str(stage.typeDemolition))
			elStage.text = "Demolition of Cell with Shears".format(stageId+1)
		elif stage.typeDemolition == 2:
			elStage = xml.etree.ElementTree.SubElement(element, "typeOfDemolition", typeDem=str(stage.typeDemolition))
			elStage.text = "Demolition of Cell with Explosive".format(stageId+1)
		
		elNuc = xml.etree.ElementTree.SubElement(element, "nuclides")
		for nucName, nucVal in stage.nuclides:
			nuc = xml.etree.ElementTree.SubElement(elNuc, "activity", nuclide=nucName)
			nuc.text = str(nucVal)
			
		elDR = xml.etree.ElementTree.SubElement(element, "DR")
		elDR.text = "{0}".format(stage.DR)
		
		root.append(element)
		
	tree = xml.etree.ElementTree.ElementTree(root)
	try:
		tree.write(oFileFolder+"/"+filename, "UTF-8")
		save_xml(oFileFolder+"/norm_"+filename, root)
	except EnvironmentError as err:
		print "{0}: import error: {1}".format(os.path.basename(sys.argv[0]), err)
	return
def main(filename, oFileFolder):
	numDem = 0
	while numDem == 0:
		try:
			numDem = int(raw_input("Enter number of demolitions stage "))
		except ValueError:
			print "Error: Demolitions stage must be int"
			print
	allStages = []
	for i in range(1, numDem+1):
		print "-----------------------------------------\n"
		print "Processing stage {0}".format(i)
		print 
		demStage = demolitionStage(i)
	
		while demStage.typeDemolition == 0:
			try:
				demStage.typeDemolition = int(raw_input("Enter the type of demolition:\n1 - Demolition of Cell with Shears\n2 - Demolition of Cell with Explosive\n"))
				if demStage.typeDemolition not in [1,2]:
					print "Error: The type of demolition must be 1 or 2"
					demStage.typeDemolition = 0
			except ValueError:
				print "Error: The type of demolition must be int"
		
		numNucl = 0
		while numNucl == 0:
			try:
				numNucl = int(raw_input("Enter the number of nuclides "))
			except ValueError:
				print "Error: The number of nuclides must be int"
				print
		nuclides = []
		for j in range(1, numNucl+1):
			
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
			nuclides.append([nameNucl,  valNucl])
			
			
		demStage.nuclides = nuclides
		
		while demStage.DR == 0.0:
			try:
				if demStage.typeDemolition == 1:
					print "Warning: Literary data 0.1<=DR<=0.9"
					demStage.DR = float(raw_input("\nEnter the damage ratio "))	
				elif demStage.typeDemolition == 2:
					print "Warning: Literary data DR=0.5"
					demStage.DR = float(raw_input("\nEnter the damage ratio "))
			except ValueError: #Добавить ввод в граммах и перевод его в активность и наоборот
				print "Error: The damage ratio must be float"
				print
		#print "nuclides", nuclides
		
		allStages.append(copy.deepcopy(demStage))
		del demStage
	createXML(allStages, oFileFolder, filename)
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
	
	optional.add_argument('--fName', action = 'store', dest='filename',  type=str, help='Output filename', required=False, default = "new_xml")
	optional.add_argument('--ofnf', action = 'store', dest='oFileNewFolder',metavar='NEW_FOLDER', type=str, help='path to the new output folder for output files', required=False, default=mypath)
	
	args_new = parser.parse_args()
	oFileNewFolder = args_new.oFileNewFolder
	if oFileNewFolder != mypath:
		try:
			os.makedirs(oFileNewFolder)
		except OSError as err:
			print "Warning! {0}".format(err)
	filename = args_new.filename
	filename = filename+".xml"
	sys.exit(main(filename, oFileNewFolder))
