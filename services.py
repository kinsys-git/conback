#!/usr/bin/python
import subprocess
import getpass
import os

## Run bash to export system information for processing
process = subprocess.run("systemctl list-unit-files | awk '{print $1 $2}' | grep enabled | grep -v enabled-runtime | sed 's/enabled//' | grep service | sed 's/\.service//' > enabledservices", shell=True, check=True, text=True)

allEnabledServicesPath = "enabledservices"
enabledServices = [""]

with open(allEnabledServicesPath) as fp:
   line = fp.readline()
   cnt = 1
   while line:
       line = fp.readline()
       enabledServices.append(line)
       cnt += 1

enabledServices.remove("")

## Cleanup
os.remove(allEnabledServicesPath)