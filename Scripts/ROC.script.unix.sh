#!/bin/bash
echo "Threshold" "Global_TPR" "Global_FPR" >> ~/Desktop/LAB/ROC.threholds
for i in $(seq 0 .01 1.01)
do
   echo $i
   echo "Protein" "Threshold" "TP" "FP" "N" "Neg" "TPR" "FPR" >> ~/Desktop/LAB/ROC_scores/ispred.${i}

      for file in ~/Desktop/LAB/ISPRED_30_protein_data/*
      do
        pdb=`echo $file | awk -F/ '{print $7}' | awk -F'_' '{print $1}' | awk -F. '{print $1}'`
        chain=`echo $file | awk -F/ '{print $7}' | awk -F'_' '{print $1}' | awk -F. '{print $2}'`
        fileid=${pdb}.${chain}
        echo $fileid
        interface=~/Desktop/LAB/Testquery30_interface/${fileid}
        combined_file=~/Desktop/LAB/Combined_ROCfiles/${fileid}.combined
        cat "$file" | grep '0.' | tail -n +2 | awk '{if($4 >= 0.00) {print $1,$10}}'| sed 's/-/0.00/g' | awk -v p=$i '{if($2 >= p) {print $1}}' >> ${combined_file}.${i}
        M=`cat "${combined_file}.${i}" | awk 'END{print NR}'`
        echo "M =" $M
        cat "$interface" >> ${combined_file}.${i}
        TP=`cat "${combined_file}.${i}" | awk '{print $1}' | sort | uniq -d | awk 'END{print NR}'`
        echo "TP =" $TP
        N=`cat "$interface" | awk 'END{print NR}'`
        FP=$((M-TP))
        Surf=`cat "$file" | grep '0.' | tail -n +2 | awk '{if($4 >= 0.00) {print $1}}' | awk 'END{print NR}'`
        Neg=$((Surf-N))
        echo "Surf = " $Surf "Neg = " $Neg
        TPR=`bc <<<"scale=3; $TP/$N"`
        FPR=`bc <<<"scale=3; $FP/$Neg"`
        echo $fileid $i $TP $FP $N $Neg $TPR $FPR >> ~/Desktop/LAB/ROC_scores/ispred.${i}
       done
    cat ~/Desktop/LAB/ROC_scores/ispred.${i} | column -t >> ~/Desktop/LAB/ROC_scores/ispred.${i}.table
    tp_sum=`cat ~/Desktop/LAB/ROC_scores/ispred.${i}.table | awk '{s+=$3}END{print s}'`
    fp_sum=`cat ~/Desktop/LAB/ROC_scores/ispred.${i}.table | awk '{s+=$4}END{print s}'`
    n_sum=`cat ~/Desktop/LAB/ROC_scores/ispred.${i}.table | awk '{s+=$5}END{print s}'`
    neg_sum=`cat ~/Desktop/LAB/ROC_scores/ispred.${i}.table | awk '{s+=$6}END{print s}'`
    Global_TPR=`bc <<<"scale=3; $tp_sum/$n_sum"`
    Global_FPR=`bc <<<"scale=3; $fp_sum/$neg_sum"`
    avg_TPR=`cat ~/Desktop/LAB/ROC_scores/ispred.${i}.table | awk '{total += $7} END {print total/NR}'`
    avg_FPR=`cat ~/Desktop/LAB/ROC_scores/ispred.${i}.table | awk '{total += $8} END {print total/NR}'`
    echo "Global_TPR = " $Global_TPR >> ~/Desktop/LAB/ROC_scores/ispred.${i}.table
    echo "Global_FPR = " $Global_FPR >> ~/Desktop/LAB/ROC_scores/ispred.${i}.table
    echo "avg_TPR = " $avg_TPR >> ~/Desktop/LAB/ROC_scores/ispred.${i}.table
    echo "avg_FPR = " $avg_FPR >> ~/Desktop/LAB/ROC_scores/ispred.${i}.table
    echo $i $Global_TPR $Global_FPR >> ~/Desktop/LAB/ROC.threholds
done
    rm ~/Desktop/LAB/Combined_ROCfiles/*
    cat ~/Desktop/LAB/ROC.threholds | column -t >> ~/Desktop/LAB/ROC.threholds.table.csv
