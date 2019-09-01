#!/bin/bash
#creating F_score file
echo "protein" "tp" "fp" "interface_residues" "F_Score" > ~/Desktop/ISPRED.Fscores.txt
#iterating through the prediction files, combining them with the annotated residues into a new file, and calculating tp based on duplicate lines
for file in ~/Desktop/LAB/ISPRED_30_protein_data/*
    do
        pdb=`echo $file | awk -F/ '{print $7}' | awk -F'_' '{print $1}' | awk -F. '{print $1}'`
        chain=`echo $file | awk -F/ '{print $7}' | awk -F'_' '{print $1}' | awk -F. '{print $2}'`
        fileid=${pdb}.${chain}
        echo $pdb
        echo $chain
        echo $fileid
        interface=~/Desktop/LAB/Testquery30_interface/${fileid}
        combined_file=~/Desktop/LAB/Combined_files/${fileid}.combined
        N=`cat "$interface" | awk 'END{print NR}'`
        echo $N
        cat "$file" | grep '0.' | tail -n +2 | awk '{if($4 >= 0.00) {print $1,$10}}'| sed 's/-/0.00/g' | sort -k 2nr | head -n"$N" | awk '{print $1}' > $combined_file
        cat "$interface" >> $combined_file
        TP=` cat "$combined_file" | awk '{print $1}' | sort | uniq -d | awk 'END{print NR}'`
        echo $TP
        F_score=`echo "scale=3; $TP/$N" | bc -l`
        FP=$((N-TP))
        echo $F_score
        echo $fileid $TP $FP $N $F_score >> ~/Desktop/ISPRED.Fscores.txt
done
#formatting F_score file into table, calculating global and average F_scores of the 30 proteins
cat ~/Desktop/ISPRED.Fscores.txt | column -t > ~/Desktop/ISPRED.Fscores.table.txt
tp_sum=`cat ~/Desktop/ISPRED.Fscores.table.txt | awk '{s+=$2}END{print s}'`
n_sum=`cat ~/Desktop/ISPRED.Fscores.table.txt | awk '{s+=$4}END{print s}'`
global_fscore=`echo "scale=3; $tp_sum/$n_sum" | bc -l`
echo "Global F_score =" $global_fscore >> ~/Desktop/ISPRED.Fscores.table.txt
avg=`cat ~/Desktop/ISPRED.Fscores.table.txt | awk '{total += $5} END {print total/NR}'`
echo "Average F_score =" $avg  >> ~/Desktop/ISPRED.Fscores.table.txt
