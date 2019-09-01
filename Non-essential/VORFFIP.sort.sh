#!/bin/bash

for file in ~/Desktop/VORFFIP_30_predictions/*
do awk '{print $2,$3,$4}' | sort -k 3nr > $file.sorted
done
