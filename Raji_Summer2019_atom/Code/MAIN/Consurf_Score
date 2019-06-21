#!/bin/sh


cd /Users/evanedelstein/Desktop/LAB/Raji_Summer2019_atom/Code/Data_files/Consurf/ConsurfScores_DB
cat testquery30 | sed 's/\./ /g' >> ConSurfDB_list_feature/testquery_for_consurf
cd ConSurfDB_list_feature
mkdir consurfPDBS
perl ConSurfDB_list_feature.pl testquery_for_consurf
mv *_grades consurfPDBS


mkdir /Users/evanedelstein/Desktop/LAB/Raji_Summer2019_atom/Code/Data_files/Consurf/consurfconservationscores
echo "Proteinid Number_of_known_Interface_residues True_positives False_positives F_score" > /Users/evanedelstein/Desktop/LAB/Raji_Summer2019_atom/Code/Data_files/Consurf/F_score_table.txt
File=/Users/evanedelstein/Desktop/LAB/Raji_Summer2019_atom/Code/Data_files/Consurf/ConsurfScores_DB/ConSurfDB_list_feature/consurfPDBS/*
for f in $File
do
  proteinid=`echo $f | awk -F/ '{print $13}' | awk -F_ '{print $1"."$2}'`
  echo "protienid" $proteinid
  cat $f | awk '$1 ~ /^[0-9]*$/' | awk '{print $1,$3,$4}' | uniq | sort -k3 -n > /Users/evanedelstein/Desktop/LAB/Raji_Summer2019_atom/Code/Data_files/Consurf/consurfconservationscores/C_score_${proteinid}.txt
  interface=/Users/evanedelstein/Desktop/LAB/Raji_Summer2019_atom/Code/Data_files/testquery30_interface/${proteinid}
  consurf_prediction=/Users/evanedelstein/Desktop/LAB/Raji_Summer2019_atom/Code/Data_files/Consurf/consurfconservationscores/C_score_${proteinid}.txt
  combined_file=/Users/evanedelstein/Desktop/LAB/Raji_Summer2019_atom/Code/Data_files/Consurf/consurfconservationscores/C_score_${proteinid}.txthead.txt


  S=`cat "$consurf_prediction" | awk 'END{print NR}' `
  if [ $S != 0 ]
  then
    N=`cat "$interface" | awk 'END{print NR}'`
    echo $N
    cat "$consurf_prediction" | head -n"$N" | awk '{print $1, $2}' > "$combined_file"
    cat "$interface" >> "$combined_file"
    TP=`cat "$combined_file" | awk '{print $1}' | sort | uniq -d | awk 'END{print NR}' `
    echo $TP
    F_score=`echo "scale=3; $TP/$N" | bc -l `
    FP=$((N-TP))
    echo $F_score
    echo $proteinid  $N $TP $FP $F_score >> /Users/evanedelstein/Desktop/LAB/Raji_Summer2019_atom/Code/Data_files/Consurf/F_score_table.txt
    rm "$combined_file"
  else
    echo $proteinid >> /Users/evanedelstein/Desktop/LAB/Raji_Summer2019_atom/Code/Data_files/Consurf/consurf_pdb_not_on_database
  fi

done

cd /Users/evanedelstein/Desktop/LAB/Raji_Summer2019_atom/Code/Data_files/Consurf
cat F_score_table.txt | column -t > F_score_consurf.txt


avrg=`cat F_score_consurf.txt | awk 'NR>1 { sum += $5 } END { print sum / NR }'`
sum_interface=`cat F_score_consurf.txt | awk 'NR>1 {sum+=$2} END {print sum}' `
sum_TP=`cat F_score_consurf.txt | awk 'NR>1 {sum+=$3} END {print sum}' `
f_score=`echo "scale=3; $sum_TP/$sum_interface" | bc -l`
echo -e "\nglobal F score = ${f_score} \naverage F score = ${avrg}"  >> F_score_consurf.txt
echo -e "\nconsurf pdb not on database\n" >> F_score_consurf.txt
cat consurf_pdb_not_on_database >> F_score_consurf.txt

rm consurf_pdb_not_on_database
rm F_score_table.txt
