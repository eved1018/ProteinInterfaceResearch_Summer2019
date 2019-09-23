#!/usr/bin/env bash

for f in /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Antogen/InterfaceResidues/*
do
  proteinname=`echo $f | awk -F/ '{print $9}'`
  residue=`cat $f | awk '{printf $1"+"}'| awk '{print substr($1,1,length($1)-1)}'`
  echo "delete all
  set max_threads, 1
  fetch $proteinname , async = 0
  color white, resi $residue
  count_atoms
  png ~/Desktop/Research_Evan/Raji_Summer2019_atom/Antogen/pymolimages/${proteinname}.png
  " > /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Antogen/pymolscripts/script_${proteinname}.pml
  # /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Antogen/script.pml
done
