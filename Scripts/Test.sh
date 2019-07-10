#!/bin/bash
cd ../ISPRED_30_protein_predictions_data
for file in ~/Desktop/LAB/ISPRED_30_protein_predictions_data/*
do
    pdb=`echo $file | awk -F/ '{print $7}'`
    chain=`echo $file | awk -F/ '{print $7}' | awk -F'_' '{print $1}' | awk -F. '{print $2}'`
    fileid=${pdb}.${chain}
    echo $pdb
done
