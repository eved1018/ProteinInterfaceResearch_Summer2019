#!/usr/bin/env bash

for file in /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Antogen/InterfaceResidues/*
do
  newfilename=`echo $file | awk -F. '{print $1}'`
  mv $file $newfilename
done
