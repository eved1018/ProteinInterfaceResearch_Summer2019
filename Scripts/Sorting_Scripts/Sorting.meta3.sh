#!/bin/bash
for file in ~/Desktop/Research_Mordechai/Data_Files/Meta/Dbmark_space_unsorted/*
do
chain=`echo $file | awk -F/ '{print $9}' | awk -F'_' '{print $1}' | awk -F. '{print $2}'`
protein=`echo $file | awk -F/ '{print $9}' | awk -F'_' '{print $1}' | awk -F. '{print $1}'`
pdb=${protein}.${chain}
echo $pdb
cat "$file" | sort -k 2nr | awk '{print $1,$2}' > ~/Desktop/Research_Mordechai/Data_Files/Meta/Dbmark_sorted/${pdb}.meta_sorted.csv
done
for file in ~/Desktop/Research_Mordechai/Data_Files/Meta/NOX_space_unsorted/*
do
chain=`echo $file | awk -F/ '{print $9}' | awk -F'_' '{print $1}' | awk -F. '{print $2}'`
protein=`echo $file | awk -F/ '{print $9}' | awk -F'_' '{print $1}' | awk -F. '{print $1}'`
pdb=${protein}.${chain}
echo $pdb
cat "$file" | sort -k 2nr | awk '{print $1,$2}' > ~/Desktop/Research_Mordechai/Data_Files/Meta/NOX_sorted/${pdb}.meta_sorted.csv
done
