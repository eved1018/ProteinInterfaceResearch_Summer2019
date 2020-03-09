#!/bin/bash

for file in /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Antogen/predictionvalue/Predus_antogens/*
do 
    proteinname=`echo $file |  awk -F/ '{print $10}' | awk -F. '{print $2}'` 
    echo $proteinname
    cat $file | awk '{print $2","$11}' | sort -k1,1 -u | sort -g -k 1,1 | awk '{print $1","$2}'  >> /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Antogen/predictionvalue/${proteinname}.csv
    
done