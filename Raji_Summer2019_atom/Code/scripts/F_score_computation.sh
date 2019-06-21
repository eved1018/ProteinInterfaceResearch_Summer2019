#!/bin/sh

cd /Users/evanedelstein/Desktop/LAB/Raji_Summer2019_atom/Code/Data_files/Predus
avrg=`cat F_score_only_unix_Table.txt | awk 'NR>1 { sum += $5 } END { print sum / NR }'`
sum_interface=`cat F_score_only_unix_Table.txt | awk 'NR>1 {sum+=$2} END {print sum}' `
sum_TP=`cat F_score_only_unix_Table.txt | awk 'NR>1 {sum+=$3} END {print sum}' `
f_score=`echo "scale=3; $sum_TP/$sum_interface" | bc -l`
echo -e "\nglobal F score = ${f_score} \naverage F score = ${avrg}"  >> F_score_only_unix_Table.txt
