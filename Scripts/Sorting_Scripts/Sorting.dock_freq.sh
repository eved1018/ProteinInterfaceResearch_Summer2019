#!/bin/bash
pathname=/Users/mordechaiwalder/Desktop/Research_Mordechai/Data_Files/Dock_freq/Unsorted_csv
echo $pathname
for file in /Users/mordechaiwalder/Desktop/Research_Mordechai/Data_Files/Dock_freq/Unsorted/*
    do
      while read p; do
      res=`echo "$p" | awk '{print $1}'`
      val=`echo "$p" | awk '{print $2}'`
      echo "$res,$val" >> ${file}.csv
    done <$file
for file in /Users/mordechaiwalder/Desktop/Research_Mordechai/Data_Files/Dock_freq/Unsorted/*.csv
    do
      filename=`echo $file | awk -F/ '{print $9}'`
      echo $filename
      cat "$file" | sort -k 1nr > ${pathname}/${filename}
    done
