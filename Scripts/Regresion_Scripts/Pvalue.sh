#!/bin/sh

csvfile=/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion/benchmarkdata.csv
# grep ",," $csvfile | awk -F',' '{print $1}' | awk -F_ '{print $2}' | uniq 


cat $csvfile | while read line
do

  proteinname=`echo $line | awk -F',' '{print $1}'`
  predusval=`echo $line | awk -F',' '{print $2}'`
  ispredval=`echo $line | awk -F',' '{print $3}'`
  dockpredval=`echo $line | awk -F',' '{print $4}'`
  exponent=$(bc <<< "-(-3.47243398 + 2.07435466 * $predusval + 2.43193857 * $ispredval+$dockpredval * 0.69229295)")
  pval=`awk -v exponent=$exponent 'BEGIN{print 1/(1+(2.71828**exponent))}'`
  echo $proteinname,$pval >> /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion/combinedscores/pvalbenhcmark.csv

done
