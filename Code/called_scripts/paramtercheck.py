#!/bin/python
import os
import sys

file_list = (sys.argv)

fileA = file_list[2]
print(fileA)

# N=`cat "$file1" | awk 'END{print NR}'`
# echo $N



  # ProtienID=`echo $f | awk -F/ '{print $11}' | awk -F. '{print $2}'`
  # echo $ProtienID
  # chainid=`echo $ProteinID | awk -F_ '{print $1}'`
  # echo $chainid
  # fileid=`echo $ProtienID | awk -F. '{print toupper($11)}'`
  # fileid+=."$chainid"
  #| tee -a /Users/evanedelstein/Desktop/LAB/Raji_Summer2019_atom/Code/Data_files/Predus/F_score_unix
