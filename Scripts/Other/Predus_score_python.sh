#!/usr/bin/env bash

: '
input -> dowloaded pdb files from Predus
output -> text file containing residues sorted from most conserved to least conserved
notes -> can easly add a command to only output top number of scores by changing the final sort command
final part computes f score
'

cd /Users/evanedelstein/Desktop/LAB/Raji_Summer2019_atom/Code/Data_files/Predus/predus_outputfiles

FILES=/Users/evanedelstein/Desktop/LAB/Raji_Summer2019_atom/Code/Data_files/Predus/predus_outputfiles/*
for f in $FILES
do
  echo "Processing $f file..."
  fileid=`echo $f | awk -F/ '{print toupper $11}' | awk -F. '{print $2}' | sed 's/\_/./g'`
  echo "protien id"
  echo $fileid
  cat $f | awk '{print $4,$5,$6,$11}' | uniq | sort -k4 -nr > /Users/evanedelstein/Desktop/LAB/Raji_Summer2019_atom/Code/Data_files/Predus/Predus_Score/P_score_${fileid}.txt
  file1=/Users/evanedelstein/Desktop/LAB/Raji_Summer2019_atom/Code/Data_files/testquery30_interface/${fileid}
  file2=/Users/evanedelstein/Desktop/LAB/Raji_Summer2019_atom/Code/Data_files/Predus/Predus_Score/P_score_${fileid}.txt
  file3=/Users/evanedelstein/Desktop/LAB/Raji_Summer2019_atom/Code/Data_files/Predus/Predus_Score/P_score_${fileid}.txthead.txt
  echo ""
  cd ..
  cat "$file2" | awk '{print $3, $1}' > "$file3"
  cd /Users/evanedelstein/Desktop/LAB/Raji_Summer2019_atom/Code/called_scripts
  python3 F_score_Python.py "$file1" "$file3" "$fileid"
  cd ..
  echo
  echo
  echo
  cd /Users/evanedelstein/Desktop/LAB/Raji_Summer2019_atom/Code/Data_files/Predus/Predus_Score
  rm "$file3"
done > /Users/evanedelstein/Desktop/LAB/Raji_Summer2019_atom/Code/Data_files/Predus/F_score_data_Predus.txt




avrg=`cat /Users/evanedelstein/Desktop/LAB/Raji_Summer2019_atom/Code/Data_files/Predus/F_score_data_Predus.txt | grep F_score | awk -F "F_score = "  '{ sum += $2 } END { print sum / NR }'`
sum_TP=`cat /Users/evanedelstein/Desktop/LAB/Raji_Summer2019_atom/Code/Data_files/Predus/F_score_data_Predus.txt | grep "true positives" | awk -F "true positives"   '{ sum += $2 } END { print sum }'`
sum_interface=`cat /Users/evanedelstein/Desktop/LAB/Raji_Summer2019_atom/Code/Data_files/Predus/F_score_data_Predus.txt | grep "residues" | awk -F "residues" '{ sum += $2 } END { print sum }'`
f_score=`echo "scale=3; $sum_TP/$sum_interface" | bc -l`

cd /Users/evanedelstein/Desktop/LAB/Raji_Summer2019_atom/Code/Data_files/Predus
echo -e "\nscore from Python"
echo -e "\nglobal F score = ${f_score} \naverage F score = ${avrg}"  >> /Users/evanedelstein/Desktop/LAB/Raji_Summer2019_atom/Code/Data_files/Predus/F_score_only_unix_Table.txt