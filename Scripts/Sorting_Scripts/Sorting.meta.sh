#!/bin/bash
meta_dbmark=~/Desktop/ProteinInterfaceResearch_Summer2019-E_Edelstein/Data_Files/Logistic_regresion_corrected/predictionvalues/benchmarkpredictionvalues.csv
meta_NOX=~/Desktop/ProteinInterfaceResearch_Summer2019-E_Edelstein/Data_Files/Logistic_regresion_corrected/predictionvalues/noxpredictionvalues.csv
for file in ~/Desktop/Research_Mordechai/Annotated_Residues/Dbmark_Annotated_Residues/*
  do
  pdb=`echo $file | awk -F/ '{print $8}' | awk -F'_' '{print $1}'`
  cat "$meta_dbmark" | grep $pdb > ~/Desktop/Research_Mordechai/Data_Files/Meta/Dbmark/${pdb}.meta.csv
done
for file in ~/Desktop/Research_Mordechai/Annotated_Residues/NOX_Annotated_Residues/*
  do
  pdb=`echo $file | awk -F/ '{print $8}' | awk -F'_' '{print $1}'`
  cat "$meta_NOX" | grep $pdb > ~/Desktop/Research_Mordechai/Data_Files/Meta/NOX/${pdb}.meta.csv
done
