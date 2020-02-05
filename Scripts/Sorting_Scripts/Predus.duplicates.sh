#!/bin/bash
pathname=~/Desktop/ProteinInterfaceResearch_Summer2019-E_Edelstein/Data_Files/Logistic_regresion/predus
for file in ${pathname}/*
  do
protein=`echo $file | awk -F/ '{print $9}' | awk -F. '{print $1}'`
chain=`echo $file | awk -F/ '{print $9}' | awk -F. '{print $2}'`
pdb=${protein}.${chain}
echo $pdb
cat "$file" | awk '{print $1}'
done
