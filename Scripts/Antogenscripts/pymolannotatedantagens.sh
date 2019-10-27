#!/usr/bin/env bash

### input of file with name; protein id; and 4 col; predus ispred docking and annotated,
### find the intersect of each col and annotated then create mutilpe dif colored residue strings
###  delete image script after
### create general image script
###
for file in /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Antogen/residues/*
do
  residue=`cat $file | awk '{printf $1"+"}'| awk '{print substr($1,1,length($1)-1)}'`
  proteinname=`echo $file | awk -F/ '{print $9}' | awk -F_ '{print $3}' | awk -F. '{print $1"." $2}'`
  echo $proteinname
  echo $residue


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
