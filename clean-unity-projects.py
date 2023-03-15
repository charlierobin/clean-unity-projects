#!/usr/bin/python3

import sys
import os

from pathlib import Path
from send2trash import send2trash

def isUnityProject(path):

	try:
	
		subfolders = os.listdir(path)
		
		if subfolders.index("Assets") and subfolders.index("Packages") and subfolders.index("ProjectSettings") and subfolders.index("UserSettings"):

			projectSettingsFolderPath = os.path.join(path, "ProjectSettings")

			projectVersionPath = os.path.join(projectSettingsFolderPath, "ProjectVersion.txt")

			with open(projectVersionPath) as f:

				lines = f.readlines()

				line = lines[0].replace("\n","")

				version = line.replace("m_EditorVersion: ","")

			projectSettingsPath = os.path.join(projectSettingsFolderPath, "ProjectSettings.asset")

			with open(projectSettingsPath) as f:

				lines = f.readlines()

				for line in lines:

					if line.count("productName: ")==1:

						productName = line.replace("\n","")

						productName = productName.replace("  productName: ","")

						break

				for line in lines:

					if line.count("companyName: ")==1:

						companyName = line.replace("\n","")

						companyName = companyName.replace("  companyName: ","")

						break


			projectFolderName = os.path.split(path)[1]

			return path, projectFolderName, productName, companyName, version
	
	except:
	
		pass

def tryMovetoTrash(path,name,projectFolderName):

	result = False

	try:

		currentItemPath = os.path.join(path, name)
		currentItemPathNEW = os.path.join(path, name + " from " + projectFolderName)
		os.rename(currentItemPath, currentItemPathNEW)
		send2trash(currentItemPathNEW)

		result = True

	except:

		result = False

	return result

def tryToCleanProjectFolder(path):

	logs = tryMovetoTrash(projectPath, "Logs",projectFolderName)
	library = tryMovetoTrash(projectPath, "Library",projectFolderName)
	obj = tryMovetoTrash(projectPath, "obj",projectFolderName)

	return logs, library, obj

def getListOfPlacesToScan():

	paths = []

	documentsPath = Path.home()

	documentsPath = os.path.join(documentsPath, "Documents")

	paths.append(documentsPath)

	import subprocess

	s = subprocess.getstatusoutput(f'df -Hl')

	( code, text ) = s

	lines = text.split("\n")

	for i in range(2, len(lines)):

		bits = lines[i].split(" ")

		path = bits[len(bits)-1]

		if path != "/System/Volumes/Data" and path != "/private/var/vm" and path != "/Volumes/Recovery":

			paths.append(path)

	return paths

def letUserSelectListOfPlacesToScan(places):

	done = False

	selected = []

	while not done and len(places)>0:

		print("")

		print("Selected:")

		for place in selected:

			print(place)

		print("")

		print("Available places:")

		number = 1

		for place in places:

			print(str(number) + ": " + str(place))

			number = number + 1

		print("")

		test = False

		while not test:

			command = input("❓ Enter the number of place to add (enter 0 when done)  ")

			if command.isnumeric():

				command = int(command)

				if command == 0:

					test = True

					done = True

				else:

					if command <= len( places ):

						test = True

						place = places[command-1]

						if selected.count( place ) == 0:

							selected.append(place)

							places.remove(place)

	return selected

def doFolder(path,depth):

	unityProjects = []

	maxPathLength=0
	maxNameLength=0

	try:

		for name in os.listdir(path):

			fullpath = os.path.join(path, name)
			
			if os.path.isdir(fullpath):

				data = isUnityProject( fullpath )

				if data:

					unityProjects.append(data)

					(projectPath, projectFolderName, productName, companyName, version) = data

					maxPathLength = max(maxPathLength,len(projectPath))
					maxNameLength = max(maxNameLength,len(productName))

				else:

					if depth < maxDepth:

						( unityProjectsNEW, maxPathLengthNEW, maxNameLengthNEW ) = doFolder( fullpath, depth + 1 )

						unityProjects = unityProjects + unityProjectsNEW

						maxPathLength = max(maxPathLength,maxPathLengthNEW)
						maxNameLength = max(maxNameLength,maxNameLengthNEW)

	except:

		pass

	return unityProjects, maxPathLength, maxNameLength

def gatherUnityProjects(places):

	print("Scan depth set to: " + str(maxDepth))

	unityProjects = []

	maxPathLength=0
	maxNameLength=0

	for volume in volumes:

		( unityProjectsNEW, maxPathLengthNEW, maxNameLengthNEW ) = doFolder(volume,0)

		unityProjects = unityProjects + unityProjectsNEW

		maxPathLength = max(maxPathLength,maxPathLengthNEW)
		maxNameLength = max(maxNameLength,maxNameLengthNEW)

	return unityProjects, maxPathLength, maxNameLength

# start

maxDepth = 2

volumes = getListOfPlacesToScan()

volumes = letUserSelectListOfPlacesToScan(volumes)

if len(volumes)==0:

	print("")

	quit();

print("")

result = input("Scan depth? (💬 Bigger values go deeper into folder hierarchy, scan takes longer.) (Currently " + str( maxDepth ) + ")  ")

if result.isnumeric():

	maxDepth = int(result)

print("")

print("Scanning for Unity project folders. (💬 This can take some time.)")

print("")

(unityProjects, maxPathLength, maxNameLength) = gatherUnityProjects(volumes)

print("")
print("")

if unityProjects.count == 0:

	print("No Unity projects were found")

	exit()

s = "{: <" + str( maxPathLength + 10 ) + "} {: <" + str( maxNameLength ) + "}"

for entry in unityProjects:

	(projectPath, projectFolderName, productName, companyName, version) = entry

	print(s.format(projectPath,productName))

print("")

result = input("❓ Are you sure you want to clean these projects? (y/n)  ")

print("")

if result != "y":

	print("💬 Your projects were left unchanged")

	print("")
	
	quit()

print("Cleaning ...")

print("")

logsCleaned = 0
librariesCleaned = 0
objCleaned = 0

s = "{: <" + str( maxPathLength + 10 ) + "} {: <6} {: <9} {: <5}"

print(s.format("Project","Logs","Library", "obj"))

for entry in unityProjects:

	(projectPath, projectFolderName, productName, companyName, version) = entry

	(logs, library, obj) = tryToCleanProjectFolder(projectPath)

	if logs: logsCleaned = logsCleaned + 1
	if library: librariesCleaned = librariesCleaned + 1
	if obj: objCleaned = objCleaned + 1

	print(s.format(projectPath, "X" if logs else " ", "X" if library else " ", "X" if obj else " "))

print("")

print(s.format("Totals:",logsCleaned, librariesCleaned, objCleaned))

print("")









