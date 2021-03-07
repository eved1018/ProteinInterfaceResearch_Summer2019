#!/usr/bin/env bash

for f in /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Antogen/InterfaceResidues/*
do
  protienid1=`echo $f | awk -F/ '{print $9}'`
  proteinid2=`echo $f | awk -F/ '{print $9}'| awk -F_ '{print $1}'`
  echo $proteinid1
  prediction=`/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Antogen/InterfaceResidues/${protienid1}`
  cat $prediction | awk '{print $1}'

  # echo "fetch $proteinid2
  #   > script.pml
done
