#!/bin/sh
file=/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/PDB_Files/PDB241/Nox_Raji_PDB/*
for f in $file
do
  protienID=`echo $f | awk -F/ '{print $10}'| awk -F. '{print $1}' | sed 's/\_/./g'| awk '{print toupper}'`
  echo $protienID >> /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion/Noxfiles/noxpdbs
done
csvfile=/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion/final_sort.csv
cat $csvfile | while read line
do
  echo $line
  nox=/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion/noxdata.csv
  benchmark=/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion/benchmarkdata.csv
  file=/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion/Noxfiles/noxpdbs
  protein=`echo $line | awk -F"," '{print $1}'| awk -F_ '{print $2}'`
  echo $protein
  if grep -q -w "$protein" "$file"; then
    echo $line >> $nox
  else
    echo $line >> $benchmark
  fi
done
