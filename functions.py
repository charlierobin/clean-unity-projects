import os
import json
import codecs

from picker import picker
from pathlib import Path
from send2trash import send2trash


def getListOfPossiblePlacesToScan():

    paths = []

    documentsPath = Path.home()

    documentsPath = os.path.join(documentsPath, "Documents")

    paths.append(documentsPath)

    import subprocess

    s = subprocess.getstatusoutput(f'df -Hl')

    (code, text) = s

    lines = text.split("\n")

    for i in range(2, len(lines)):

        bits = lines[i].split("%   ")

        path = bits[len(bits)-1]

        if path != "/System/Volumes/Data" and path != "/private/var/vm" and path != "/Volumes/Recovery":

            paths.append(path)

    return paths


def letUserSelectListOfPlacesToScan(places):

    selected = picker(
        places, "Please select the places you want to search for Unity projects")

    selectedPlaces = []

    for item in selected:
        selectedPlaces.append(places[item])

    return selectedPlaces


def letUserSelectListOfProjectsToClean(projects):

    captions = []

    for p in projects:

        (path, projectFolderName, productName, companyName, version) = p

        captions.append(path + "\t" + productName + "\t" + companyName + "\t" + version)

    selected = picker(
        captions, "Please select the projects you want to clean")

    selectedProjects = []

    for item in selected:
        selectedProjects.append(projects[item])

    return selectedProjects


def readFile(path):

    lines = []

    try:

        with codecs.open(path, encoding='utf-8') as f:

            try:

                lines = f.readlines()

            except UnicodeDecodeError as err:

                print("UnicodeDecodeError", path)

                print(err)

                print("")

        f.close()

    except RuntimeError as err:

        print("RuntimeError", path)

        print("")

        print(err)

    return lines


def isUnityProject(path):

    subfolders = os.listdir(path)

    if "Assets" in subfolders and "Packages" in subfolders and "ProjectSettings" in subfolders and "UserSettings" in subfolders:

        version = "⚠️ Unknown"
        productName = "⚠️ Unknown"
        companyName = "⚠️ Unknown"

        projectSettingsFolderPath = os.path.join(path, "ProjectSettings")

        projectVersionPath = os.path.join(
            projectSettingsFolderPath, "ProjectVersion.txt")

        lines = readFile(projectVersionPath)

        if len(lines) > 0:

            line = lines[0].replace("\n", "")

            version = line.replace("m_EditorVersion: ", "")

        projectSettingsPath = os.path.join(
            projectSettingsFolderPath, "ProjectSettings.asset")

        lines = readFile(projectSettingsPath)

        for line in lines:

            if line.count("productName: ") == 1:

                productName = line.replace("\n", "")

                productName = productName.replace("  productName: ", "")

                break

        for line in lines:

            if line.count("companyName: ") == 1:

                companyName = line.replace("\n", "")

                companyName = companyName.replace("  companyName: ", "")

                break

        projectFolderName = os.path.split(path)[1]

        return path, projectFolderName, productName, companyName, version


def tryMovetoTrash(path, name, projectFolderName):

    result = False

    try:

        currentItemPath = os.path.join(path, name)
        currentItemPathNEW = os.path.join(
            path, name + " from " + projectFolderName)
        os.rename(currentItemPath, currentItemPathNEW)
        send2trash(currentItemPathNEW)

        result = True

    except:

        result = False

    return result


def tryToCleanProjectFolder(project):

    (path, projectFolderName, productName, companyName, version) = project

    logs = tryMovetoTrash(path, "Logs", projectFolderName)
    library = tryMovetoTrash(path, "Library", projectFolderName)
    obj = tryMovetoTrash(path, "obj", projectFolderName)

    return logs, library, obj


def doFolder(path, skip):

    unityProjects = []

    for name in os.listdir(path):

        if name[0] == ".":
            continue

        fullpath = os.path.join(path, name)

        if os.path.isdir(fullpath) and fullpath not in skip:

            data = isUnityProject(fullpath)

            if data:

                unityProjects.append(data)

            else:

                found = doFolder(fullpath, skip)

                unityProjects = unityProjects + found

    return unityProjects


def gatherUnityProjects(volumes):

    f = open(os.path.join(os.path.dirname(__file__), "config.json"))

    skip = json.load(f)

    f.close()

    unityProjects = []

    for volume in volumes:

        found = doFolder(volume, skip)

        unityProjects = unityProjects + found

    return unityProjects
