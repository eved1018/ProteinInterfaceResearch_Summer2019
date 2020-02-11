#!/bin/sh

csvfile=/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion/benchmarkdata.csv
# csvfile=/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/test.csv
# calculates P values
cat $csvfile | while read line
do

  proteinname=`echo $line | awk -F',' '{print $1}'`
  predusval=`echo $line | awk -F',' '{print $2}'`
  ispredval=`echo $line | awk -F',' '{print $3}'`
  dockpredval=`echo $line | awk -F',' '{print $4}'`
  preduscoef=1.26625079
  ispredcoef=2.74825078
  dockpredcoef=1.81020245
  yintercept=3.65825493

  exponent=$(bc <<< "-(-$yintercept + $preduscoef * $predusval + $ispredcoef * $ispredval+$dockpredval * $dockpredcoef)")
  pval=`awk -v exponent=$exponent 'BEGIN{print 1/(1+(2.71828**exponent))}'`
  echo $proteinname,$pval >> /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/pvaltest.csv

done
