#!/bin/bash
for file in ~/Desktop/Research_Mordechai/Data_Files/ISPRED/ISPRED_DBMark_data/*
  do
  pdb=`echo $file | awk -F/ '{print $9}' | awk -F'_' '{print $1}'`
  protein=`echo $file | awk -F/ '{print $9}' | awk -F'_' '{print $1}' | awk -F. '{print $1}'`
  echo $protein
  cat "$file" | grep '0.' | tail -n +2 | awk '{print $1,$10}' | sed 's/-/0.00/g' | sort -k 2nr | sed 's/Surface//g' | sed 's/Protein//g' | sed 's/length//g' | sed 's/id//g' | sed '/^ *$/d' | sed 's/ /_/g' | column -t > ~/Desktop/Research_Mordechai/Data_Files/ISPRED/ISPRED_DBMark_data_sorted/${pdb}.ispred_sorted
done
