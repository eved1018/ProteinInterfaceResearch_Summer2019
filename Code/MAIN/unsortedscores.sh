#!/bin/sh


for f in /Users/evanedelstein/Desktop/LAB/Raji_Summer2019_atom/Code/Data_files/Predus/predus_outputfiles/*
do
  protienID=`echo $f | awk -F/ '{print toupper $11}' | awk -F. '{print $2}' | sed 's/\_/./g'`
  cat $f | awk '{print $6, $11, $11 * ".5212705531" , $11 * "0.493834223" }'| column -t > /Users/evanedelstein/Desktop/LAB/Raji_Summer2019_atom/Code/Data_files/Predus/unsorted/${protienID}_Porder

done
