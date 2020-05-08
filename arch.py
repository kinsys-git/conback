#!/usr/bin/python
import subprocess
import getpass
import os

allPackPath = "arch-allpackages"
allAurPath = "arch-allaur"
allPackages = [""]
allAur = [""]
noAur = [""]

## Run bash to export system information for processing
process = subprocess.run("pacman -Qqe > arch-allpackages && pacman -Qqm > arch-allaur", shell=True, check=True, text=True)

## Parse exported information
with open(allPackPath) as fp:
   line = fp.readline()
   cnt = 1
   while line:
       line = fp.readline()
       allPackages.append(line)
       noAur.append(line)
       cnt += 1

with open(allAurPath) as fp:
   line = fp.readline()
   cnt = 1
   while line:
       line = fp.readline()
       allAur.append(line)
       noAur.remove(line)
       cnt += 1

## Remove initialize variables
allPackages.remove("")
allAur.remove("")
noAur.remove("")

## Cleanup
os.remove(allPackPath)
os.remove(allAurPath)