#!/usr/bin/env bash


# ispredfile=/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/ISPRED/ispred241/${proteinname}.ispred_unsorted.csv
# ispredfakeout=/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/ispred/${proteinname}_ispred_fakeout.csv
# ispredoutput=/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/ispred/${proteinname}_ispred.csv
ispredfile=/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/ISPRED/ispred241/1A0F.A.ispred_unsorted.csv
String=`cat $ispredfile | head -n 1 | awk -F, '{print $1}'`
echo $String

while [ -z "$String" ]
do
    sed -i "" '1d' $ispredfile
    String=`cat $ispredfile | head -n 1 | awk -F, '{print $1}'`
    echo $String
done 
