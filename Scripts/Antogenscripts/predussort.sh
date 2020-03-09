#!/bin/bash

# for file in /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Antogen/predictionvalue/Predus_antogens/*
# do 
#     proteinname=`echo $file |  awk -F/ '{print $10}' | awk -F. '{print $2}'` 
#     echo $proteinname
#     cat $file | awk '{print $2, $11}' | sort -k1,1 -u | sort -g -k 1,1 | awk '{print $1","$2}'  >> /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Antogen/predictionvalue/res_pred/predus/${proteinname}_predus.csv

# done
# for file in /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Antogen/predictionvalue/Dock_freq/* 
# do 
#     proteinname=`echo $file |  awk -F/ '{print $10}' | awk -F. '{print $1}'`
#     cat $file |  awk '{print $1, $2}' | sort -k1,1 -u | sort -g -k 1,1 | awk '{print $1","$2}'  >> /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Antogen/predictionvalue/res_pred/dockpred/${proteinname}_dockpred.csv
# done

# for file in /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Antogen/predictionvalue/ISPRED_Antigen_data/*
# do 
#     proteinname=`echo $file |  awk -F/ '{print $10}' | awk -F. '{print $1}'`
#     cat "$file" | grep '0.' | tail -n +2 | awk '{print $1", "$10}' | sed 's/-/0.00/g' | sed 's/0.001/1/g' | sed 's/Surface//g' | sed 's/://g' | sed 's/ , //g' | sed 's/Protein//g' | sed 's/length//g' | sed 's/id//g' | sed '/^ *$/d' | awk '{print $1, $2}' >> /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Antogen/predictionvalue/res_pred/ispred/${proteinname}_ispred.csv 
# done 
for file in /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Antogen/InterfaceResidues/*
do 
    proteinname=`echo $file |  awk -F/ '{print $9}' | awk -F_ '{print $1}'`
    cat $file | awk '{print $1}' >> /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Antogen/predictionvalue/res_pred/annotated/${proteinname}_annotated.csv
done 