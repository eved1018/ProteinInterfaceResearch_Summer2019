#!/bin/sh
# shoudl be switched to R to use with PDB parser

cat Data_files/testquery30 | awk -v ORS='\",'\" '{ print  $1 }' | sed 's/\./_/g'
