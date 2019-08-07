#!/bin/sh

cd /Users/evanedelstein/Desktop/LAB/Raji_Summer2019_atom/Code/Data_files/Predus
echo "Proteinid Number_of_known_Interface_residues True_positives False_positives F_Score" > F_score_only_unix.txt
cd predus_outputfiles
for f in /Users/evanedelstein/Desktop/LAB/Raji_Summer2019_atom/Code/Data_files/Predus/predus_outputfiles/*
do
  echo "Processing $f file..."
  protienID=`echo $f | awk -F/ '{print toupper $11}' | awk -F. '{print $2}' | sed 's/\_/./g'`
  echo "protien id"
  echo $protienID
  cat $f | awk '{print $4,$5,$6,$11}' | uniq | sort -k4 -nr > /Users/evanedelstein/Desktop/LAB/Raji_Summer2019_atom/Code/Data_files/Predus/Predus_Score/P_score_${protienID}
  interface=/Users/evanedelstein/Desktop/LAB/Raji_Summer2019_atom/Code/Data_files/testquery30_interface/${protienID}
  Predus_prediction=/Users/evanedelstein/Desktop/LAB/Raji_Summer2019_atom/Code/Data_files/Predus/Predus_Score/P_score_${protienID}
  combined_file=/Users/evanedelstein/Desktop/LAB/Raji_Summer2019_atom/Code/Data_files/Predus/P_score_${protienID}.txthead.txt
  N=`cat "$interface" | awk 'END{print NR}'`
  echo $N
  cat "$Predus_prediction" | head -n"$N" | awk '{print $3, $1}' > "$combined_file"
  cat "$interface" >> "$combined_file"
  TP=`cat "$combined_file" | awk '{print $1}' | sort | uniq -d | awk 'END{print NR}' `
  echo $TP
  F_score=`echo "scale=3; $TP/$N" | bc -l `
  FP=$((N-TP))
  echo $F_score
  echo $protienID  $N $TP $FP $F_score >> ../F_score_only_unix.txt
  rm "$combined_file"
done
cd ..
cat F_score_only_unix.txt | column -t > F_score_only_unix_Table.txt

avrg=`cat F_score_only_unix_Table.txt | awk 'NR>1 { sum += $5 } END { print sum / NR }'`
sum_interface=`cat F_score_only_unix_Table.txt | awk 'NR>1 {sum+=$2} END {print sum}' `
sum_TP=`cat F_score_only_unix_Table.txt | awk 'NR>1 {sum+=$3} END {print sum}' `
f_score=`echo "scale=3; $sum_TP/$sum_interface" | bc -l`
echo -e "\nglobal F score = ${f_score} \naverage F score = ${avrg}"  >> F_score_only_unix_Table.txt

rm F_score_only_unix.txt
