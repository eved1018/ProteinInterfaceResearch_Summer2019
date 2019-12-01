#!/usr/bin/env bash

for file in /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Predus/predus_outputfiles/*
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
    annotatedfile=/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Annotated_Residues/Testquery30_Interface/$proteinname
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

for file in /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/ROC_3/final/*
do
  sed -i '' '/^,/d' $file
done
