#!/usr/bin/env bash

### change n to be cutoff of interface

# rm ../../Data_Files/PymolPredus/Scripts/script.pml
rm ../../Antogen/pymolscripts/script.pml # deletes the file if it already exists


find ../../Antogen/pymolimages/ -type f -name "*.png" -delete
 



# old directory: ../../Data_Files/Predus/predus_outputfiles/*

#for file in ../../Antogen/Predus_antogens/*
for file in ../../Antogen/predictionvalue/Predus_antogens/*
do
  proteinname=`echo $file | awk -F/ '{print $5}'| awk -F. '{print $2}' | sed 's/\_/./g'`

  echo $file" ~~~~ "$proteinname

  #interfacefile="../../Annotated_Residues/Testquery30_Interface/$proteinname"

  # annotated files
  interfacefile="../../Antogen/InterfaceResidues/sorted/${proteinname}_sorted" 

  # interfaceoutput=../../Data_Files/PymolPredus/interfaceoutput/interfaceoutput_${proteinname}.txt
  
  interfaceoutput=../../Antogen/preduce_interface_output/interfaceoutput_${proteinname}.txt
  cat $interfacefile | awk '{print $1}' | sort > $interfaceoutput


  # outputfile=../../Data_Files/PymolPredus/predsort/predsort_${proteinname}.txt
  outputfile=../../Antogen/predsort/predsort_${proteinname}.txt

  # cat $file | awk '{print $6, $11}' | uniq |sort -k2 -nr| uniq | head -n"15" | awk '{print $1}' > $outputfile

  # outputfile=/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/PymolPredus/predsort/predsort_${proteinname}.txt
  N=`cat "$interfaceoutput" | awk 'END{print NR}'`
  # cat $file | awk '{print $6, $11}' | uniq |sort -k2 -nr| uniq | head -n"$N" | awk '{print $1}'> $outputfile
  cat $file | awk '{print $6, $11}' | uniq | uniq | head -n"$N" | awk '{print $1}'> $outputfile
  
  #cat $outputfile | awk '{print $1}' | sort > $outputfile # just added
  # echo "UNSORTED1--------------"
  # cat $outputfile
  # echo "UNSORTED1--------------"
  
  # sort -on2 outputfile outputfile
  # ################## DEBUG
  # echo "SORTED--------------"
  # cat $outputfile
  # echo "FILE: $outputfile"
  # echo "--done--"
  ################## DEBUG

  # for debugging
  #cat $file | awk '{print $6, $11}' | uniq |sort -k2 -nr| uniq | head -n"$N" | awk '{print $1}'

  # printf "\n\n------------------------------------------------\n"
  # printf "FILE: $outputfile\n"

  predus_residue_comm=`comm -23 $outputfile $interfaceoutput | awk '{printf $1"+"}'| awk '{print substr($1,1,length($1)-1)}'`
  interface_residue_comm=`comm -13 $outputfile $interfaceoutput| awk '{printf $1"+"}'| awk '{print substr($1,1,length($1)-1)}'`
  correct_residue_comm=`comm -12 $outputfile $interfaceoutput | awk '{printf $1"+"}'| awk '{print substr($1,1,length($1)-1)}'`
  correct_residue_comm_check=`test -z "$correct_residue_comm" && echo "" || echo "; color green, resi $correct_residue_comm"`
  correct_res_sphere=`test -z "$correct_residue_comm" && echo "" || echo "; select color green; show spheres, SEL"`
  correct_res_label=`test -z "$correct_residue_comm" && echo "" || echo "; label resi $correct_residue_comm, ID; set label_position,(3,2,1)"`

  # cat $outputfile
  # printf "~~~~~~~~~~~~~~\n"
  # cat $interfaceoutput

  
  # rm ../../Data_Files/PymolPredus/Images/${proteinname}.png
  # rm ../../Antogen/pymolimages/${proteinname}.png   # file in main folder
  

  # files_in_subfolders = ../../Antogen/pymolimages/${proteinname}/*.png  # files in subfolders
  # for f in $files_in_subfolders
  # do 
  #   rm $f
  # done
  


  echo "
delete all
fetch $proteinname, async = 0

# Blue -- Predus ($predus_residue_comm)
# Red -- Annotated ($interface_residue_comm)

color white; color blue, resi $predus_residue_comm; color red, resi $interface_residue_comm $correrct_residue_comm_chek
color green, resi $correct_residue_comm

select color blue; show spheres, SEL
select color red; show spheres, SEL
$correct_res_sphere
$correct_res_label
remove resn hoh
zoom complete=1

# blue
orient resi $predus_residue_comm 

# removes the shadows that give the appearannce of depth
set depth_cue, 0

center $proteinname


python

import pymolpredus

rotator = pymolpredus.Rotate(\"${proteinname}\", \"$correct_residue_comm\", \"$predus_residue_comm\")
rotator.take_pictures()


python end

# the directory to which the png files are outputted
# png ../../Antogen/pymolimages/${proteinname}.png, width=900, height=900,ray=1, dpi=500



delete all" >> ../../Antogen/pymolscripts/script.pml



# zoom complete=1
# rotate x, 180
# orient resi ---
# unset opaque-background
# dpi = 300
# show spheres

  # open -a "Pymol" ../../Data_Files/PymolPredus/Scripts/script_${proteinname}.pml
  done
#
# for file in ../../Data_Files/PymolPredus/Scripts/* ;do
#   if [[ "$file" == script* ]];then
#     open -a "pymol" $file
#     echo "hi"
#   fi
# done


unameOut="$(uname -s)"

if [ "$unameOut" == "Linux" ]
then
  pymol ../../Antogen/pymolscripts/script.pml # if the script is run on linux
else
  open -a "Pymol" ../../Antogen/pymolscripts/script.pml # if it's run on windows/mac
fi

# ../../Data_Files/PymolPredus/Scripts/script.pml

# /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/PymolPredus/Scripts/script.pml

# label resi $predus_residue_comm, ID
# set label_position,(3,2,1)
# label resi $interface_residue_comm, ID
# set label_position,(3,2,1)
