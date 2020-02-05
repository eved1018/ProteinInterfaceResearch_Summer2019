#!/bin/bash
for file in ~/Desktop/Research_Mordechai/Data_Files/ISPRED/ISPRED_DBMark_data_unsorted/*
  do
  chain=`echo $file | awk -F/ '{print $9}' | awk -F'_' '{print $1}' | awk -F. '{print $2}'`
  protein=`echo $file | awk -F/ '{print $9}' | awk -F'_' '{print $1}' | awk -F. '{print $1}'`
  pdb=${protein}.${chain}
  echo $pdb
  cat "$file" | column -t | sort -k 2nr | awk '{print $1,$2}' > ~/Desktop/Research_Mordechai/Data_Files/ISPRED/ISPRED_DBMark_data_sorted/${pdb}.ispred_sorted.csv
done
