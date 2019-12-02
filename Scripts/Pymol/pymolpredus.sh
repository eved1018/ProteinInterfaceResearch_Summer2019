#!/usr/bin/env bash


# spheres on all colored, label on green, remove water groups

for file in ../../Data_Files/Predus/predus_outputfiles/*
do
  proteinname=`echo $file | awk -F/ '{print $6}'| awk -F. '{print $2}' | sed 's/\_/./g'`

  # echo $file" ~~~~ "$proteinname

  outputfile=../../Data_Files/PymolPredus/predsort/predsort_${proteinname}.txt
  cat $file | awk '{print $6, $11}' | uniq |sort -k2 -nr| uniq | head -n"15" | awk '{print $1}' > $outputfile

  # cat  "$outputfile"

  # echo "LALALLA"
  # pwd
  # ls ../../Data_Files/PymolPredus/predsort/
  # echo "END"

  interfacefile="../../Annotated_Residues/Testquery30_Interface/$proteinname"
  interfaceoutput=../../Data_Files/PymolPredus/interfaceoutput/interfaceoutput_${proteinname}.txt
  cat $interfacefile | awk '{print $1}' | sort > $interfaceoutput

  cat $outputfile | awk '{print $1}' | sort > $outputfile # just added

  predus_residue_comm=`comm -23 $outputfile $interfaceoutput | awk '{printf $1"+"}'| awk '{print substr($1,1,length($1)-1)}'`
  interface_residue_comm=`comm -13 $outputfile $interfaceoutput| awk '{printf $1"+"}'| awk '{print substr($1,1,length($1)-1)}'`
  correrct_residue_comm=`comm -12 $outputfile $interfaceoutput | awk '{printf $1"+"}'| awk '{print substr($1,1,length($1)-1)}'`
  correrct_residue_comm_check=`test -z "$correrct_residue_comm" && echo "" || echo "; color green, resi $correrct_residue_comm"`

  rm ../../Data_Files/PymolPredus/Scripts/script.pml
  echo "
delete all
fetch $proteinname, async = 0
color white; color blue, resi $predus_residue_comm; color red, resi $interface_residue_comm $correrct_residue_comm_check
zoom complete=1

png ../../Data_Files/PymolPredus/Images/${proteinname}.png, width=900, height=900,ray=1, dpi=500

delete all" >> ../../Data_Files/PymolPredus/Scripts/script.pml


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
  # echo "WORKS"
  pymol ../../Data_Files/PymolPredus/Scripts/script.pml
else
  open -a "Pymol" ../../Data_Files/PymolPredus/Scripts/script.pml
fi

# ../../Data_Files/PymolPredus/Scripts/script.pml
