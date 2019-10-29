#!/bin/bash
pathname=/Users/mordechaiwalder/Desktop/Research_Mordechai/Data_Files/Dock_freq/Sorted
echo $pathname
for file in /Users/mordechaiwalder/Desktop/Research_Mordechai/Data_Files/Dock_freq/Sorted/*
    do
      filename=`echo $file | awk -F/ '{print $9}'`
      while read p; do
      res=`echo "$p" | awk '{print $1}'`
      val=`echo "$p" | awk '{print $2}'`
      echo "$res,$val" >> $file.csv
    done <$file
    #  cat "$file" | sort -k 2nr | sed '/^ *$/d' | column -t > $file.csv
    #  cat "$file" | sort -k 2nr | sed '/^ *$/d' | awk '{print $2}' >> ${pathname}/${filename}_sorted.csv
done
