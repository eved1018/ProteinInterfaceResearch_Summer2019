#!/usr/bin/env bash

temppdbs=/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/PDB_Files/temppdbs.txt
temppdbssorted=/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/PDB_Files/temppdbssorted.txt
temppred=/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/PDB_Files/temppred.txt
temppredsorted=/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/PDB_Files/temppredsorted.txt
missingpdbs=/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/PDB_Files/tempmissing.txt

for file in /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/PDB_Files/PDB241/Dbmark_Raji_PDB/*
do
  echo $file | awk -F/ '{print $10}' | awk -F. '{print $1}' >> $temppdbs
done

for file in /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/PDB_Files/PDB241/Nox_Raji_PDB/*
do
  echo $file | awk -F/ '{print toupper($10)}' | awk -F. '{print $1}'  >> $temppdbs
done

for file in /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/PDB_Files/Predus_241/*
do
  echo $file | awk -F/ '{print $9}' |awk -F. '{print $1}' | awk -F_ '{print $2 "_"$3}' >> $temppred
done

sort $temppdbs > $temppdbssorted
sort $temppred > $temppredsorted
comm -23 $temppdbssorted $temppredsorted > $missingpdbs
echo pdbs
cat $temppdbs | awk 'END{print NR}'
echo predus
cat $temppred | awk 'END{print NR}'
echo missing
cat $missingpdbs | awk 'END{print NR}'
