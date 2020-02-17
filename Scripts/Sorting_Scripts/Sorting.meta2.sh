#!/bin/bash
for file in ~/Desktop/Research_Mordechai/Data_Files/Meta/Dbmark/*
  do
    while read p; do
    res=`echo "$p" | awk -F'_' '{print $1}'`
    val=`echo "$p" | awk -F',' '{print $2}'`
    pdb=`echo "$p" | awk -F',' '{print $1}' | awk -F'_' '{print $2}'`
    echo "$res, $val" >> ~/Desktop/Research_Mordechai/Data_Files/Meta/Dbmark_space_unsorted/${pdb}.meta_unsorted.csv
  done <$file
done
for file in ~/Desktop/Research_Mordechai/Data_Files/Meta/NOX/*
  do
    while read p; do
    res=`echo "$p" | awk -F'_' '{print $1}'`
    val=`echo "$p" | awk -F',' '{print $2}'`
    pdb=`echo "$p" | awk -F',' '{print $1}' | awk -F'_' '{print $2}'`
    echo $pdb
    echo "$res, $val" >> ~/Desktop/Research_Mordechai/Data_Files/Meta/NOX_space_unsorted/${pdb}.meta_unsorted.csv
  done <$file
done
