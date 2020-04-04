#!/bin/bash
pacman -Qqe > arch-allpackages
pacman -Qqm > arch-allaur
systemctl list-unit-files | awk '{print $1 $2}' | grep enabled | grep -v enabled-runtime | sed 's/enabled//' | grep service | sed 's/\.service//' > arch-enabledservices