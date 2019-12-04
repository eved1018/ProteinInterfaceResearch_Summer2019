#!/usr/bin/env bash

# Function 1- Create CSV file from Predus,Ispred, Dockpred.

for file in /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/PDB_Files/Predus_241_for_real/*
do
  proteinname=`echo $file | awk -F/ '{print $10}'| awk -F. '{print $2}' | sed 's/\_/./g'`
  ###Predus
  output=/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/ROC_3/predus/${proteinname}_predus.csv
  cat $file | awk '{print $6, $11}' | uniq |sort -n | uniq | awk '{print $1","$2}'> $output
  ###Ispred
  ispredfile=/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/ISPRED/ISPRED_30_resorder/${proteinname}_iorder
  ispredoutput=/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/ROC_3/ispred/${proteinname}_ispred.csv
  cat $ispredfile | awk '{print $2}'| paste -d "," $output - > $ispredoutput
  ###Dockpred
  dockpredfile=/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Unsorted/${proteinname}.docking_freq.csv
  dockpredoutput=/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/ROC_3/dockpred/${proteinname}_dockpred.csv
  cat $dockpredfile |sort -n | awk -F, '{print $2}'| paste -d "," $ispredoutput - > $dockpredoutput
  ##anotated
  predcorrectfile=/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/ROC_3/predcorrect/correct.${proteinname}
  cat $dockpredoutput | while read line
  do
    annotatedfile=/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Annotated_Residues/Annotated/${proteinname}_Interface_Residues
    residue=`echo $line | awk -F, '{print $1}'`
    if grep -q -w "$residue" "$annotatedfile"; then
      echo $residue,1 >> $predcorrectfile
    else
      echo $residue,0 >> $predcorrectfile
    fi
  done
  finaloutput=/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/ROC_3/final/${proteinname}_final.csv
  cat $predcorrectfile | awk -F, '{print $2}'| paste -d "," $dockpredoutput - > $finaloutput
done

# honestly not sure

for file in /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/ROC_3/final/*
do
  sed -i '' '/^,/d' $file
done

# appends protein name to begining of residue

for file in /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/ROC_3/final/*
do
  outputfilesort=/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/ROC_3/final_sort.csv
  proteinname=`echo $file | awk -F/ '{print $10}'| awk -F_ '{print $1}'`
  echo $proteinname
  awk -v var=$proteinname -F, '{print $1=$1"_"var","$2","$3","$4","$5 }' $file >> $outputfilesort
done

# created headers

outputfilesort=/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/ROC_3/final_sort.csv
echo "residue,predus,ispred,dockpred,annotated" > $outputfilesort
for file in /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/ROC_3/final/*
do
  outputfilesort=/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/ROC_3/final_sort_noheader.csv
  cat $file >> $outputfilesort
done
