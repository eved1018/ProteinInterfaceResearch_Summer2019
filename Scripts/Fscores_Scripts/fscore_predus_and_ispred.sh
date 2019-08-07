#!/bin/sh


echo "protien Predus Ispred" > /Users/evanedelstein/Desktop/LAB/Raji_Summer2019_atom/Code/results/tmp.txt
File=/Users/evanedelstein/Desktop/LAB/Raji_Summer2019_atom/Code/results/Fscores/*
echo $File
paste $File | grep '^1.*$'| awk '{if ($1==$2 && $1==$7) print $1, $6, $11 ; else print $1}'  >> /Users/evanedelstein/Desktop/LAB/Raji_Summer2019_atom/Code/results/tmp.txt
f=`grep -E -i  "global" /Users/evanedelstein/Desktop/LAB/Raji_Summer2019_atom/Code/results/Fscores/* | awk -F: '{print $2}' | awk -F= 'BEGIN { ORS="\t" }; { print  $2 }' | awk -F% '{print $1}' `
A=`grep -E -i  "Average" /Users/evanedelstein/Desktop/LAB/Raji_Summer2019_atom/Code/results/Fscores/* | awk -F: '{print $2}' | awk -F= 'BEGIN { ORS="\t" }; { print  $2 }' | awk -F% '{print $1}'`
echo "GFS" ${f} >>/Users/evanedelstein/Desktop/LAB/Raji_Summer2019_atom/Code/results/tmp.txt
echo "AFS" ${A} >>/Users/evanedelstein/Desktop/LAB/Raji_Summer2019_atom/Code/results/tmp.txt
cat /Users/evanedelstein/Desktop/LAB/Raji_Summer2019_atom/Code/results/tmp.txt | column -t > /Users/evanedelstein/Desktop/LAB/Raji_Summer2019_atom/Code/results/Fscores/F_Score_results_full
