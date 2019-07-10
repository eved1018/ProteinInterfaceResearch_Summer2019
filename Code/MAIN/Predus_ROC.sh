#!/bin/sh


mkdir /Users/evanedelstein/Desktop/LAB/Raji_Summer2019_atom/Code/Data_files/ROC_scores
mkdir /Users/evanedelstein/Desktop/LAB/Raji_Summer2019_atom/Code/Data_files/ROC_scores/ROC_combined
mkdir /Users/evanedelstein/Desktop/LAB/Raji_Summer2019_atom/Code/Data_files/ROC_scores/Pscores
echo "Threshold" "Global_TPR" "Global_FPR" >> /Users/evanedelstein/Desktop/LAB/Raji_Summer2019_atom/Code/Data_files/ROC_scores/ROC.thresholds
for i in $(seq 0 .01 1.1)
do
   echo $i
   echo "Protein" "Threshold" "TP" "FP" "N" "Neg" "TPR" "FPR" >> /Users/evanedelstein/Desktop/LAB/Raji_Summer2019_atom/Code/Data_files/ROC_scores/Pscores/P_score_.${i}

      for file in /Users/evanedelstein/Desktop/LAB/Raji_Summer2019_atom/Code/Data_files/Predus/Predus_Score/*
      do
        echo "Processing $file file..."
        protienID=`echo $file | awk -F_ '{print $7}'`
        echo "protien id"
        echo $protienID
        interface=/Users/evanedelstein/Desktop/LAB/Raji_Summer2019_atom/Code/Data_files/testquery30_interface/${protienID}
        Predus_prediction=/Users/evanedelstein/Desktop/LAB/Raji_Summer2019_atom/Code/Data_files/Predus/Predus_Score/P_score_${protienID}
        combined_file=/Users/evanedelstein/Desktop/LAB/Raji_Summer2019_atom/Code/Data_files/ROC_scores/ROC_combined/${protienID}.combined
        N=`cat "$interface" | awk 'END{print NR}'`
        cat "$file" | awk '{print $3, $4}'| awk -v p=$i '{if($2 >= p) {print $1}}' | awk '!seen[$1]++' >> ${combined_file}.${i}
        M=`cat "${combined_file}.${i}" | awk 'END{print NR}'`
        echo "M =" $M
        cat "$interface" >> ${combined_file}.${i}
        TP=`cat "${combined_file}.${i}" | awk '{print $1}' | sort | uniq -d | awk 'END{print NR}'`
        echo "TP =" $TP
        N=`cat "$interface" | awk 'END{print NR}'`
        FP=$((M-TP))
        Surface_predictions=/Users/evanedelstein/Desktop/LAB/Raji_Summer2019_atom/Code/Data_files/ISPRED_30_protein_data/${protienID}_ispred.data.txt
        Surf=`cat "$Surface_predictions" | grep '0.' | tail -n +2 | awk '{if($4 >= 0.00) {print $1}}' | awk 'END{print NR}'`
        Neg=$((Surf-N))
        echo "Surf = " $Surf "Neg = " $Neg
        TPR=`bc <<<"scale=3; $TP/$N"`
        FPR=`bc <<<"scale=3; $FP/$Neg"`
        echo $protienID $i $TP $FP $N $Neg $TPR $FPR >> /Users/evanedelstein/Desktop/LAB/Raji_Summer2019_atom/Code/Data_files/ROC_scores/Pscores/P_score_.${i}
       done
    table=/Users/evanedelstein/Desktop/LAB/Raji_Summer2019_atom/Code/Data_files/ROC_scores/Pscores/P_score_.${i}.table
    cat /Users/evanedelstein/Desktop/LAB/Raji_Summer2019_atom/Code/Data_files/ROC_scores/Pscores/P_score_.${i} | column -t >> $table
    tp_sum=`cat $table | awk '{s+=$3}END{print s}'`
    fp_sum=`cat $table | awk '{s+=$4}END{print s}'`
    n_sum=`cat $table | awk '{s+=$5}END{print s}'`
    neg_sum=`cat $table| awk '{s+=$6}END{print s}'`
    Global_TPR=`bc <<<"scale=3; $tp_sum/$n_sum"`
    Global_FPR=`bc <<<"scale=3; $fp_sum/$neg_sum"`
    avg_TPR=`cat $table | awk '{total += $7} END {print total/NR}'`
    avg_FPR=`cat $table | awk '{total += $8} END {print total/NR}'`
    echo "Global_TPR = " $Global_TPR >> $table
    echo "Global_FPR = " $Global_FPR >> $table
    echo "avg_TPR = " $avg_TPR >> $table
    echo "avg_FPR = " $avg_FPR >> $table
    echo $i $Global_TPR $Global_FPR >> /Users/evanedelstein/Desktop/LAB/Raji_Summer2019_atom/Code/Data_files/ROC_scores/ROC.thresholds
done

    rm /Users/evanedelstein/Desktop/LAB/Raji_Summer2019_atom/Code/Data_files/ROC_scores/ROC_combined/*
    echo SEP=, > /Users/evanedelstein/Desktop/LAB/Raji_Summer2019_atom/Code/Data_files/ROC_scores/ROC.thresholds.table.csv
    cat /Users/evanedelstein/Desktop/LAB/Raji_Summer2019_atom/Code/Data_files/ROC_scores/ROC.thresholds | column -t -s \t | sed 's/ /,/g' >> /Users/evanedelstein/Desktop/LAB/Raji_Summer2019_atom/Code/Data_files/ROC_scores/ROC.thresholds.table.csv
    rm -r /Users/evanedelstein/Desktop/LAB/Raji_Summer2019_atom/Code/Data_files/ROC_scores/ROC_combined

# for file in /Users/evanedelstein/Desktop/LAB/Raji_Summer2019_atom/Code/Data_files/ROC_scores/Pscores/*
# do
#     echo $file >> /Users/evanedelstein/Desktop/LAB/Raji_Summer2019_atom/Code/Data_files/ROC_scores/rocscores.txt
#     column -t $file >> /Users/evanedelstein/Desktop/LAB/Raji_Summer2019_atom/Code/Data_files/ROC_scores/rocscores.txt
# done
