#!/usr/bin/python
import subprocess

allPackPath = "arch-allpackages"
allAurPath = "arch-allaur"
allEnabledServicesPath = "arch-enabledservices"
allPackages = [""]
allAur = [""]
noAur = [""]
enabledServices = [""]

## Run bash to export system information for processing
archBash = subprocess.Popen(["bash", "arch-infoexport.sh"])
archBash.wait()

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

with open(allEnabledServicesPath) as fp:
   line = fp.readline()
   cnt = 1
   while line:
       line = fp.readline()
       enabledServices.append(line)
       cnt += 1

## Remove initialize variable
allPackages.remove("")
allAur.remove("")
noAur.remove("")
enabledServices.remove("")
