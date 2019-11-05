#!/usr/bin/env bash

### input of file with name; protein id; and 4 col; predus ispred docking and annotated,
### find the intersect of each col and annotated then create mutilpe dif colored residue strings
###  delete image script after
### create general image script
###
for file in /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Antogen/residues/*
do
  proteinname=`echo $file | awk -F/ '{print $9}' | sed 's/\_/./g' | awk -F. '{print $3}' | awk '{print toupper}'`
  echo $proteinname

  interfacefile=/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Antogen/InterfaceResidues/${proteinname}
  interfacefilesorted=/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Antogen/InterfaceResidues/sorted/${proteinname}_sorted
  cat $interfacefile | sort -k1 -n > $interfacefilesorted

  predus_residue_comm=`comm -23 $file $interfacefilesorted | awk '{printf $1"+"}'| awk '{print substr($1,1,length($1)-1)}'`
  interface_residue_comm=`comm -13 $file $interfacefilesorted| awk '{printf $1"+"}'| awk '{print substr($1,1,length($1)-1)}'`
  correrct_residue_comm=`comm -12 $file $interfacefilesorted | awk '{printf $1"+"}'| awk '{print substr($1,1,length($1)-1)}'`
  echo $predus_residue_comm
  echo $interface_residue_comm
  echo $correrct_residue_comm
  correrct_residue_comm_check=`test -z "$correrct_residue_comm" && echo "" || echo "; color green, resi $correrct_residue_comm"`
  echo $correrct_residue_comm_check

  echo "delete all
  fetch $proteinname, async = 0
  color white; color blue, resi $predus_residue_comm; color red, resi $interface_residue_comm $correrct_residue_comm_check
  png ~/Desktop/Research_Evan/Raji_Summer2019_atom/Antogen/pymolimages/${proteinname}.png, ray=1, quiet=1
  " > /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Antogen/pymolscripts/script_${proteinname}.pml


  open -a "Pymol" /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Antogen/pymolscripts/script_${proteinname}.pml
done

cd /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Antogen/pymolscripts/
rm 'image'*
rm *'cif'
