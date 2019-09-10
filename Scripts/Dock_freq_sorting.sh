#!/bin/bash
pathname=/Users/mordechaiwalder/Desktop/Research_Mordechai/Data_Files/Dock_freq/Sorted
echo $pathname
for file in /Users/mordechaiwalder/Desktop/Research_Mordechai/Data_Files/Dock_freq/Unsorted/*
    do
      filename=`echo $file | awk -F/ '{print $9}'`
      cat "$file" | sort -k 2nr > ${pathname}/${filename}_sorted
done
  #  cat "$file" | sort -k 2nr > ${file}_sorted
