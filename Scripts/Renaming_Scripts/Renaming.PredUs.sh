#!/bin/bash
pathname=~/Desktop/ProteinInterfaceResearch_Summer2019-E_Edelstein/Data_Files/Logistic_regresion_corrected/predus
for file in ${pathname}/*
  do
  pdb=`echo $file | awk -F/ '{print $9}' | awk -F'_' '{print $1}'`
  echo $pdb
  mv $file ${pathname}/${pdb}.predus.csv
done
