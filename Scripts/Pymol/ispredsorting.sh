#!/bin/bash
for file in ~/Desktop/Research_Mordechai/Data_Files/ISPRED/ISPRED_NOX_data/*
  do
  pdb=`echo $file | awk -F/ '{print $9}' | awk -F'_' '{print $1}'`
  protein=`echo $file | awk -F/ '{print $9}' | awk -F'_' '{print $1}' | awk -F. '{print $1}'`
  echo $pdb
  cat "$file" | grep '0.' | tail -n +2 | awk '{print $1", "$10}' | sed 's/-/0.00/g' | sed 's/0.001/1/g' | sed 's/Surface//g' | sed 's/://g' | sed 's/ , //g' | sed 's/Protein//g' | sed 's/length//g' | sed 's/id//g' | sed '/^ *$/d' | awk '{print $1, $2}' > ~/Desktop/Research_Mordechai/Data_Files/ISPRED/ISPRED_NOX_data_unsorted/${pdb}.ispred_unsorted.csv
done