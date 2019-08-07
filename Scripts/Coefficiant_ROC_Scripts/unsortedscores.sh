#!/bin/sh


for f in /Users/evanedelstein/Desktop/LAB/Raji_Summer2019_atom/Code/Data_files/Predus/predus_outputfiles/*
do
  coefA=".5212705531"
  coefB="0.493834223"
  protienID=`echo $f | awk -F/ '{print toupper $11}' | awk -F. '{print $2}' | sed 's/\_/./g'`
  cat $f | awk -v A=$coefA B=$coefB '{print $6, $11, $11 * A , $11 * B }'| uniq | column -t > /Users/evanedelstein/Desktop/LAB/Raji_Summer2019_atom/Code/results/CoeffeciantROC/coeffeciant/${protienID}_PCOEF

done
