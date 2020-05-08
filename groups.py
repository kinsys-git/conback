#!/usr/bin/python
import subprocess
import getpass
import os

## Run bash to export system information for processing
process = subprocess.run('groups $USER > usergroups', shell=True, check=True, text=True)

allUserGroupsPath = "usergroups"
userGroups = [""]

with open(allUserGroupsPath,'r') as f:
    for line in f:
        for word in line.split():
           userGroups.append(word)

## Remove init
userGroups.remove("")

## User is automatically added to a group under self, removing
userGroups.remove(getpass.getuser())

## Cleanup
os.remove(allUserGroupsPath)