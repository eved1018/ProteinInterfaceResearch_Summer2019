#!/bin/bash

# for file in /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Antogen/predictionvalue/Dock_freq/*
# do 
#     proteinname=`echo $file | awk -F/ '{print $10}' | awk -F. '{print $1}'`
#     cat $file | sort -k1 -n >> /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Antogen/predictionvalue/docksort/${proteinname}_sort.csv
# done
# for file in /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Antogen/predictionvalue/Predus_antogens/*
# do 
#     proteinname=`echo $file |  awk -F/ '{print $10}' | awk -F. '{print $2}'` 
#     echo $proteinname
#     cat $file | awk '{print $6, $11}' | sort -k1,1 -u | sort -g -k 1,1 | awk '{print $1","$2}'  >> /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Antogen/predictionvalue/res_pred/predus/${proteinname}_predus.csv

# done

# for file in /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Antogen/predictionvalue/docksort/* 
# do 
#     proteinname=`echo $file |  awk -F/ '{print $10}' | awk -F. '{print $1}'`
#     cat $file |  awk '{print $1, $2}' | sort -k1,1 -u | sort -g -k 1,1 | awk '{print $1","$2}'  >> /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Antogen/predictionvalue/res_pred/dockpred/${proteinname}_dockpred.csv
# done

# for file in /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Antogen/predictionvalue/ISPRED_Antigen_data/*
# do 
#     proteinname=`echo $file |  awk -F/ '{print $10}' | awk -F. '{print $1}'`
#     cat "$file" | grep '0.' | tail -n +2 | awk '{print $1", "$10}' | sed 's/-/0.00/g' | sed 's/0.001/1/g' | sed 's/Surface//g' | sed 's/://g' | sed 's/ , //g' | sed 's/Protein//g' | sed 's/length//g' | sed 's/id//g' | sed '/^ *$/d' | awk '{print $1, $2}' >> /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Antogen/predictionvalue/res_pred/ispred/${proteinname}_ispred.csv 
# done 
# for file in /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Antogen/InterfaceResidues/*
# do 
#     proteinname=`echo $file |  awk -F/ '{print $9}' | awk -F_ '{print $1}'`
#     cat $file | awk '{print $1}' >> /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Antogen/predictionvalue/res_pred/annotated/${proteinname}_annotated.csv
# done 
cd /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Antogen/predictionvalue/sorted/
mkdir predussort ispredsort dockpredsort annotatedsort final
for file in /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Antogen/predictionvalue/res_pred/predus/*
do
    proteinname=`echo $file | awk -F/ '{print $11} '| awk -F'_' '{print toupper ($1)}' `
    cat $file | awk -v var=$proteinname -F, '{print $1=$1"_"var "," $2}'  >> /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Antogen/predictionvalue/sorted/predussort/${proteinname}_predussort.csv
done 

for file in /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Antogen/predictionvalue/res_pred/ispred/*
do  
    proteinname=`echo $file |  awk -F/ '{print $11}' | awk -F_ '{print toupper ($1)}'`  
    echo $proteinname  
    predfile=/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Antogen/predictionvalue/sorted/predussort/${proteinname}_predussort.csv
    ispredfile=/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Antogen/predictionvalue/sorted/ispredsort/${proteinname}_ispred.csv
    cat $file | awk -F"," '{print $2}'| paste -d "," $predfile - > $ispredfile
done 

# for file in /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Antogen/predictionvalue/res_pred/dockpred/*
# do 
    
#     proteinname=`echo $file |  awk -F/ '{print $11}' | awk -F_ '{print toupper ($1)}'`    
#     dockpred=/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Antogen/predictionvalue/sorted/dockpredsort/${proteinname}_docksort.csv
#     ispredfile=/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Antogen/predictionvalue/sorted/ispredsort/${proteinname}_ispred.csv
#     cat $file | awk -F, '{print $2}'| sed 's/^ *//g'| paste -d "," $ispredfile - > $dockpred
# done 

# for file in /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Antogen/predictionvalue/res_pred/annotated/*
# do 
#     proteinname=`echo $file |  awk -F/ '{print $11}' | awk -F_ '{print toupper ($1)}'` 
#     dockpred=/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Antogen/predictionvalue/sorted/dockpredsort/${proteinname}_docksort.csv
#     annotatedfinal=/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Antogen/predictionvalue/sorted/annotatedsort/${proteinname}_ispred.csv
#     cat $dockpred | while read line
#     do
#         annotatedfile=/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Antogen/predictionvalue/res_pred/annotated/${proteinname}_annotated.csv
#         residue=`echo $line | awk -F"," '{print $1}'`
#         if grep -q -w "$residue" "$annotatedfile"; then
#         echo $residue,1 >> $annotatedfinal
#         else
#         echo $residue,0 >> $annotatedfinal
#         fi
#     done
#     finaloutput=/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Antogen/predictionvalue/sorted/final/${proteinname}_final.csv
#     cat $annotatedfinal | awk -F, '{print $2}'| paste -d "," $dockpred - > $finaloutput
# done

