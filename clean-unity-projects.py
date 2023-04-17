#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from functions import getListOfPossiblePlacesToScan
from functions import letUserSelectListOfPlacesToScan
from functions import gatherUnityProjects
from functions import letUserSelectListOfProjectsToClean
from functions import tryToCleanProjectFolder

volumes = getListOfPossiblePlacesToScan()

volumes = letUserSelectListOfPlacesToScan(volumes)

if len(volumes) == 0:

    print("")

    quit()

print("")

print("Scanning for Unity project folders. (💬 This can take some time.)")

print("")

unityProjects = gatherUnityProjects(volumes)

if len(unityProjects) == 0:

    print("No Unity projects were found")

    print("")

    quit()

print(len(unityProjects), "projects found")

print("")

result = input("❓ Do you want to review the found projects? (y/n)  ")

if result == "y":

    unityProjects = letUserSelectListOfProjectsToClean(unityProjects)

print("")

print(len(unityProjects), "projects selected")

print("")

if len(unityProjects) == 0:

    print("No Unity projects selected")

    print("")

    quit()

result = input("❓ Are you sure you want to clean these projects? (y/n)  ")

print("")

if result != "y":

    print("💬 Your projects were left unchanged")

    print("")

    quit()

print("Cleaning…")

print("")

logsCleaned = 0
librariesCleaned = 0
objCleaned = 0

for project in unityProjects:

    (logs, library, obj) = tryToCleanProjectFolder(project)

    if logs:
        logsCleaned = logsCleaned + 1
    if library:
        librariesCleaned = librariesCleaned + 1
    if obj:
        objCleaned = objCleaned + 1

print("Totals:")

print("")

print("Logs:", logsCleaned)
print("Libraries:", librariesCleaned)
print("obj:", objCleaned)

print("")
