#!/bin/bash
pathname=/Users/mordechaiwalder/Desktop/Research_Mordechai/Data_Files/Dock_freq/Unsorted_adjusted
echo $pathname
for file in /Users/mordechaiwalder/Desktop/Research_Mordechai/Data_Files/Dock_freq/Sorted_adjusted/*
    do
      filename=`echo $file | awk -F/ '{print $9}' | awk -F'_' '{print $1}'`
      echo $filename
      cat "$file" | sort -k 1n > ${pathname}/${filename}_freq.csv
    done
