#!/bin/sh

for file in /Users/evanedelstein/Desktop/LAB/Raji_Summer2019_atom/Code/Data_files/ROC_scores/Pscores/*
do
  echo $file >> /Users/evanedelstein/Desktop/LAB/Raji_Summer2019_atom/Code/Data_files/ROC_scores/rocscores.txt
  column -t $file >> /Users/evanedelstein/Desktop/LAB/Raji_Summer2019_atom/Code/Data_files/ROC_scores/rocscores.txt
done
