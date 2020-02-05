#!/bin/bash
for file in ~/Desktop/Research_Mordechai/Data_Files/ISPRED/ISPRED_DBMark_data/*
  do
  pdb=`echo $file | awk -F/ '{print $9}' | awk -F'_' '{print $1}'`
  protein=`echo $file | awk -F/ '{print $9}' | awk -F'_' '{print $1}' | awk -F. '{print $1}'`
  echo $pdb
  cat "$file" | grep '0.' | tail -n +2 | awk '{print $1", "$4}' | sed 's/Surface//g' | sed 's/://g' | sed 's/ , //g' | sed 's/Protein//g' | sed 's/length//g' | sed 's/chain//g' | sed 's/id//g' | sed '/^ *$/d' | awk '{print $1, $2}' > ~/Desktop/Research_Mordechai/Data_Files/ISPRED/ISPRED_DBMark_data_RSA/${pdb}_ispred_RSA.csv
done
