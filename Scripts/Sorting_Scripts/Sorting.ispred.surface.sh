#!/bin/bash
RSAdir=/Users/mordechaiwalder/Desktop/Research_Mordechai/Data_Files/ISPRED/ISPRED_NOX_data_RSA
path=/Users/mordechaiwalder/Desktop/Research_Mordechai/Data_Files/ISPRED/ISPRED_NOX_data_surface
a=10
for file in ${RSAdir}/*
  do
    pdb=`echo $file | awk -F/ '{print $9}' | awk -F'_' '{print $1}'`
    while read p; do
      res=`echo "$p" | awk '{print $1}'`
      RSA=`echo "$p" | awk '{print $2}'`
      if [$RSA -ge $a]
      then
        echo "$res,$RSA" >> ${path}/${pdb}_surface.csv
      fi
    done <$file
  done
