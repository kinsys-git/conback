#!/usr/bin/python
# This python file uses the following encoding: utf-8
import home
import arch
import groups
import services
import os
import shutil
import pathlib
from os import path

cwd = os.getcwd()
## TODO custom folder name
bootstrapFolder = "Package/" + home.hostname + "_" + "ConfigBackup"
bootstrapFolderBash = bootstrapFolder.replace("Package/", "")
homeStaging = bootstrapFolder + "/home"
homeStagingBash = homeStaging.replace("Package/" , "")
configStaging = homeStaging + "/.config"
configStagingBash = configStaging.replace("Package/" , "")
fileOut = cwd + "/Package/" + "/bootstrap.sh"
fileOutPackages = cwd + "/Package/" + "/arch-packages"
fileOutAUR = cwd + "/Package/" + "/arch-packages-aur"

## Folder staging
pathlib.Path(cwd + "/" + configStaging).mkdir(parents=True, exist_ok=True)

if os.path.exists(fileOut):
    os.remove(fileOut)
if os.path.exists(fileOutPackages):
    os.remove(fileOutPackages)
if os.path.exists(fileOutAUR):
    os.remove(fileOutAUR)
script = open(fileOut , "a")
script.write("#!/bin/bash\n")
script.write("##THIS IS AN AUTOMATICALLY GENERATED SCRIPT AND WILL BE OVERWRITTEN\n")
script.write("##PLEASE SEE https://github.com/soripants/conback FOR DETAILS\n")
script.write("\n")

scriptPackage = open(fileOutPackages , "a")
scriptAUR = open(fileOutAUR , "a")

## Print exclusions
print("----- CHANGE EXCLUSIONS IN conback.conf -----")
print("Folders Exluded (Size > 10MB):")
for folders in home.configFoldersExcluded:
    print(home.configDir + folders)
for folders in home.homeDirFoldersExcluded:
    print(home.homeDir + folders)

## ARCH SPECIFIC
## TODO arch specific config file - aur vs non-aur options
## Package Install
script.write("##### PACKAGES #####\n")
script.write("sudo pacman -Syyu --noconfirm\n")
script.write("sudo pacman -S --noconfirm --needed $(cat arch-packages)")
for packages in arch.noAur:
    scriptPackage.write(packages)
scriptPackage.close()
script.write("\n")
script.write("\n")
script.write("##### AUR Packages #####\n")
script.write("mkdir tmp\n")
script.write("cd tmp\n")
script.write("git clone https://aur.archlinux.org/yay\n")
script.write("cd yay\n")
script.write("makepkg -si\n")
script.write("cd ../..\n")
script.write("rm -rf tmp\n")
script.write("yay -S --noconfirm --needed $(cat arch-packages-aur)")
for packages in arch.allAur:
    if packages != "yay" or packages != "yay-git":
        scriptAUR.write(packages)
scriptAUR.close()
script.write("\n")
script.write("\n")


## SYSTEMD SPECIFIC
## Enable services
script.write("##### SERVICES #####\n")
for services in services.enabledServices:
    if services != "":
        script.write("sudo systemctl enable " + services)
script.write("\n")

## Copy files to stage and write bootstrap
## TODO Symlink option
script.write("\n")
script.write("##### FILE COPY #####\n")
for items in home.homeDirFolders:
    if os.path.exists(cwd + "/" + homeStaging + "/" + items):
        print("Deleting " + cwd + "/" + homeStaging + "/" + items)
        shutil.rmtree(cwd + "/" + homeStaging + "/" + items)
    print("Copying " +  home.homeDir + items)
    shutil.copytree(home.homeDir + items , cwd + "/" + homeStaging + "/" + items, symlinks=True, ignore=shutil.ignore_patterns("*.pipe"))
    script.write("cp -r $PWD/" + homeStagingBash + "/" + items + "/ ~/" + items + "/" + "\n")
for items in home.configFolders:
    if os.path.exists(cwd + "/" + configStaging + "/" + items):
        print("Deleting" + cwd + "/" + configStaging + "/" + items)
        shutil.rmtree(cwd + "/" + configStaging + "/" + items)
    print("Copying " + home.configDir + items)
    shutil.copytree(home.configDir + items , cwd + "/" + configStaging + "/" + items, symlinks=True, ignore=shutil.ignore_patterns("*.pipe"))
    script.write("cp -r $PWD/" + configStagingBash + "/" + items + "/ ~/.config/" + items + "/" + "\n")
for items in home.homeDirFiles:
    print("Copying " + home.homeDir + items)
    shutil.copyfile(home.homeDir + items , cwd + "/" + homeStaging + "/" + items)
    script.write("cp $PWD/" + homeStagingBash + "/" + items + " ~/" + items + "\n")
for items in home.configFiles:
    print("Copying " + home.configDir + items)
    shutil.copyfile(home.configDir + items , cwd + "/" + configStaging + "/" + items)
    script.write("cp $PWD/" + configStagingBash + "/" + items + " ~/.config/" + items + "\n")
script.write("\n")

## Add user to previous groups
script.write("##### USER GROUPS #####\n")
for items in groups.userGroups:
    script.write("sudo usermod -a -G " + items + " $USER\n")
script.write("\n")

## Reboot option
script.write("##### REBOOT QUESTION #####\n")
script.write("echo 'Reboot now?(y/N)'\n")
script.write("echo '  '\n")
script.write("echo 'Enter: '\n")
script.write("read choice\n")
script.write("if [ $choice == Y -o $choice == y ]\n")
script.write("    then\n")
script.write("    systemctl reboot\n")
script.write("fi\n")
script.close()