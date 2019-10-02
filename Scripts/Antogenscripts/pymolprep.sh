#!/usr/bin/env bash

for file in /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Antogen/Predus_antogens/*
do
  protienID=`echo $file | awk -F/ '{print $9}' | sed 's/\_/./g' | awk -F. '{print $1 "." $3}' `
  echo $protienID
  Predus_prediction=/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Antogen/Predus_antogens
  interface=/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Antogen/InterfaceResidues/${protienID}
  N=`cat "$interface" | awk 'END{print NR}'`


done
