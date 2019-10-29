#!/usr/bin/env bash

for file in /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Antogen/Predus_antogens/*
do
  protienID=`echo $file | awk -F/ '{print $9}' | sed 's/\_/./g' | awk -F. '{print $2}' `
  echo $protienID
  predictionfile=/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Antogen/residues/P_score_${protienID}.prediction.txt
  interface=/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Antogen/InterfaceResidues/${protienID}
  combined_file=/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Antogen/combined/P_score_${protienID}.combined.txt
  N=`cat "$interface" | awk 'END{print NR}'`
  echo $N
  cat $file | awk '{print $2, $11}' | uniq | sort -k2 -nr | head -n"$N" > $predictionfile
  cat "$predictionfile" > "$combined_file"
  cat "$interface" >> "$combined_file"
  TP=`cat "$combined_file" | awk '{print $1}' | sort | uniq -d | awk 'END{print NR}' `
  echo $TP

done
