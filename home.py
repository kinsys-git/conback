#!/usr/bin/python
# This python file uses the following encoding: utf-8
import sys
import subprocess
import re
import os.path
import getpass
import socket
from os import path
from pathlib import Path
from fileoperations import FileOperations

hostname = socket.gethostname()
user = getpass.getuser()
homeDir = "/home/" + user + "/"
configDir = homeDir + ".config/"
configFolders = FileOperations.delistLargeFolders(configDir , next(os.walk(configDir))[1])
configFiles = FileOperations.removeSymlinks(configDir , next(os.walk(configDir))[2])
configFoldersExcluded = next(os.walk(configDir))[1]
homeDirHiddenFolders = FileOperations.searchHidden(homeDir , True)
homeDirFolders = FileOperations.delistLargeFolders(homeDir , homeDirHiddenFolders)
homeDirFiles = FileOperations.searchHidden(homeDir , False)
homeDirFoldersExcluded = FileOperations.searchHidden(homeDir , True)

for folders in configFolders:
    configFoldersExcluded.remove(folders)
for folders in homeDirFolders:
    homeDirFoldersExcluded.remove(folders)
    if folders == ".cache":
        homeDirHiddenFolders.remove(folders)
        homeDirFoldersExcluded.append(folders)


