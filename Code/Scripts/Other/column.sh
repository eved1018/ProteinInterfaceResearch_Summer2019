#!/bin/sh

for file in /Users/evanedelstein/Desktop/LAB/Raji_Summer2019_atom/Code/results/CoeffeciantROC/ROCcurve/*
do
  echo $file >> /Users/evanedelstein/Desktop/LAB/Raji_Summer2019_atom/Code/results/CoeffeciantROC/ROCtemp.txt
  column -t $file >> /Users/evanedelstein/Desktop/LAB/Raji_Summer2019_atom/Code/results/CoeffeciantROC/CoefficantROC.txt
done

rm /Users/evanedelstein/Desktop/LAB/Raji_Summer2019_atom/Code/results/CoeffeciantROC/ROCtemp.txt
