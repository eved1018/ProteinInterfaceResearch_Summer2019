#!/bin/bash
ispred=~/Desktop/Research_Mordechai/Data_Files/ISPRED/ISPRED_NOX_data_unsorted
for file in ${ispred}/*
do
String=`cat $file | head -n 1 | awk -F, '{print $1}'`
while [ -z "$String" ]
do
    sed -i "" '1d' $file
    String=`cat $file | head -n 1 | awk -F, '{print $1}'`
    echo $String
done
done
