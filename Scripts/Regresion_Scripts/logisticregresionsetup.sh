#!/bin/sh

# sorts based on nox or benchmark
mkdir /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/Noxfiles

file=/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/PDB_Files/PDB241/Nox_Raji_PDB/*
for f in $file
do
  protienID=`echo $f | awk -F/ '{print $10}'| awk -F. '{print $1}' | sed 's/\_/./g'| awk '{print toupper}'`
  echo $protienID >> /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/Noxfiles/noxpdbs.csv
done
csvfile=/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/final.csv
cat $csvfile | while read line
do
  # echo $line
  nox=/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/noxdata.csv
  benchmark=/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/benchmarkdata.csv
  file=/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/Noxfiles/noxpdbs.csv
  protein=`echo $line | awk -F"," '{print $1}'| awk -F_ '{print $2}'`
  # echo $protein
  if grep -q -w "$protein" "$file"; then
    echo $line >> $nox
  else
    echo $line >> $benchmark
  fi
done
