#!/usr/bin/env bash


for file in /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Annotated_Residues/Annotated/*
do
    sed -i '' 's/"//g' $file
done
