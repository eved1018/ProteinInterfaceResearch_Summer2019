#!/usr/bin/env bash

### input of file with name; protein id; and 4 col; predus ispred docking and annotated,
### find the intersect of each col and annotated then create mutilpe dif colored residue strings
###  delete image script after
### create general image script
###

for f in /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Antogen/InterfaceResidues/*
do
  proteinname=`echo $f | awk -F/ '{print $9}' | awk -F_ '{print $1}'`
  residue=`cat $f | awk '{printf $1"+"}'| awk '{print substr($1,1,length($1)-1)}'`

  echo "delete all
  fetch $proteinname , async = 0
  color white, resi $residue
  " > /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Antogen/pymolscripts/script_${proteinname}.pml
  echo "
  png  ~/Desktop/Research_Evan/Raji_Summer2019_atom/Antogen/pymolimages/${proteinname}.png
  quit
  " > /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Antogen/pymolscripts/image_${proteinname}.pml

  open -a "Pymol" /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Antogen/pymolscripts/script_${proteinname}.pml
  sleep 10
  open -a "Pymol" /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Antogen/pymolscripts/image_${proteinname}.pml
  sleep 5

done

cd /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Antogen/pymolscripts/
rm 'image'*
rm *'cif'
