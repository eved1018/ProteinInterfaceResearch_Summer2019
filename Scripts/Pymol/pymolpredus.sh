#!/usr/bin/env bash


# spheres on all colored, label on green, remove water groups

for file in /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Predus/predus_outputfiles/*
do
  proteinname=`echo $file | awk -F/ '{print $10}'| awk -F. '{print $2}' | sed 's/\_/./g'`

  outputfile=/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/PymolPredus/predsort/predsort_${proteinname}.txt
  cat $file | awk '{print $6, $11}' | uniq |sort -k2 -nr| uniq | head -n"15" | awk '{print $1}'> $outputfile

  interfacefile=/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Annotated_Residues/Testquery30_Interface/$proteinname
  interfaceoutput=/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/PymolPredus/interfaceoutput/interfaceoutput_${proteinname}.txt
  cat $interfacefile | awk '{print $1}' | sort > $interfaceoutput
  predus_residue_comm=`comm -23 $outputfile $interfaceoutput | awk '{printf $1"+"}'| awk '{print substr($1,1,length($1)-1)}'`
  interface_residue_comm=`comm -13 $outputfile $interfaceoutput| awk '{printf $1"+"}'| awk '{print substr($1,1,length($1)-1)}'`
  correrct_residue_comm=`comm -12 $outputfile $interfaceoutput | awk '{printf $1"+"}'| awk '{print substr($1,1,length($1)-1)}'`
  correrct_residue_comm_check=`test -z "$correrct_residue_comm" && echo "" || echo "; color green, resi $correrct_residue_comm"`
  correct_res_sphere=`test -z "$correrct_residue_comm" && echo "" || echo "; select color green; show spheres, SEL"`
  correct_res_label=`test -z "$correrct_residue_comm" && echo "" || echo "; label resi $correrct_residue_comm, ID; set label_position,(3,2,1)"`


  echo "
delete all
fetch $proteinname, async = 0
color white; color blue, resi $predus_residue_comm; color red, resi $interface_residue_comm $correrct_residue_comm_check
select color blue; show spheres, SEL
select color red; show spheres, SEL
$correct_res_sphere
label resi $predus_residue_comm, ID
set label_position,(3,2,1)
label resi $interface_residue_comm, ID
set label_position,(3,2,1)
$correct_res_label
zoom complete=1
png ~/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/PymolPredus/Images/${proteinname}.png, width=900, height=900,ray=1, dpi=500
delete all" >> ../../Data_Files/PymolPredus/Scripts/script.pml


  # open -a "Pymol" /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/PymolPredus/Scripts/script_${proteinname}.pml
done
#
# for file in /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/PymolPredus/Scripts/* ;do
#   if [[ "$file" == script* ]];then
#     open -a "pymol" $file
#     echo "hi"
#   fi
# done
open -a "Pymol" /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/PymolPredus/Scripts/script.pml

# /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/PymolPredus/Scripts/script.pml
