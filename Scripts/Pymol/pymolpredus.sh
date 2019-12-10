#!/usr/bin/env bash

# Function 1 - takes in predus pdbs with prediction and filters out a list of predicted residues

for file in /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Predus/predus_outputfiles/*
do
  proteinname=`echo $file | awk -F/ '{print $10}'| awk -F. '{print $2}' | sed 's/\_/./g'`


  interfacefile=/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Annotated_Residues/Testquery30_Interface/$proteinname
  interfaceoutput=/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/PymolPredus/interfaceoutput/interfaceoutput_${proteinname}.txt
  cat $interfacefile | awk '{print $1}' | sort > $interfaceoutput

  outputfile=/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/PymolPredus/predsort/predsort_${proteinname}.txt
  N=`cat "$interfaceoutput" | awk 'END{print NR}'`
  cat $file | awk '{print $6, $11}' | uniq |sort -k2 -nr| uniq | head -n"$N" | awk '{print $1}'> $outputfile

# Function 2 - comparison of predicted and annnotated residues
  #ispred_pred_comm
  #dock_pred_comm=
  predus_residue_comm=`comm -23 $outputfile $interfaceoutput | awk '{printf $1"+"}'| awk '{print substr($1,1,length($1)-1)}'`
  interface_residue_comm=`comm -13 $outputfile $interfaceoutput| awk '{printf $1"+"}'| awk '{print substr($1,1,length($1)-1)}'`
  correrct_residue_comm=`comm -12 $outputfile $interfaceoutput | awk '{printf $1"+"}'| awk '{print substr($1,1,length($1)-1)}'`
  correrct_residue_comm_check=`test -z "$correrct_residue_comm" && echo "" || echo "; color green, resi $correrct_residue_comm"`
  correct_res_sphere=`test -z "$correrct_residue_comm" && echo "" || echo "; select color green; show spheres, SEL"`
  correct_res_label=`test -z "$correrct_residue_comm" && echo "" || echo "; label resi $correrct_residue_comm, ID; set label_position,(3,2,1)"`

# Function 3- creation of pml script to image the proteins
  echo "
delete all
fetch $proteinname, async = 0
color white; color blue, resi $predus_residue_comm; color red, resi $interface_residue_comm $correrct_residue_comm_check
select color blue; show spheres, SEL
select color red; show spheres, SEL
$correct_res_sphere
$correct_res_label
set sphere_scale, 0.50, (all)
remove resn hoh
zoom complete=1
png ~/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/PymolPredus/Images/${proteinname}.png, width=900, height=900,ray=1, dpi=500
delete all" >> ../../Data_Files/PymolPredus/Scripts/script.pml
done

open -a "Pymol" /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/PymolPredus/Scripts/script.pml

# label resi $predus_residue_comm, ID
# set label_position,(3,2,1)
# label resi $interface_residue_comm, ID
# set label_position,(3,2,1)
