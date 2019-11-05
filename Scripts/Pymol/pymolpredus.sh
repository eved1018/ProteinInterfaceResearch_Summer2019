#!/usr/bin/env bash



file=/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Predus/predus_outputfiles/PD2.1avx_A.comb.pdb
protienname=`echo "1avx_A"`
echo $protienname
oututfile=/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Scripts/Pymol/outputfile.txt
cat $file | awk '{print $6, $11}' | uniq |sort -k2 -nr| uniq | head -n"15" | awk '{print $1}'> $oututfile
interfacefile=/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Annotated_Residues/Testquery30_Interface/1AVX.A
interfaceoutput=/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Scripts/Pymol/interfaceoutput.txt
cat $interfacefile | awk '{print $1}' | sort > $interfaceoutput
predus_residue_comm=`comm -23 $oututfile $interfaceoutput | awk '{printf $1"+"}'| awk '{print substr($1,1,length($1)-1)}'`
interface_residue_comm=`comm -13 $oututfile $interfaceoutput| awk '{printf $1"+"}'| awk '{print substr($1,1,length($1)-1)}'`
correrct_residue_comm=`comm -12 $oututfile $interfaceoutput | awk '{printf $1"+"}'| awk '{print substr($1,1,length($1)-1)}'`
echo $predus_residue_comm
echo $interface_residue_comm
echo $correrct_residue_comm
correrct_residue_comm_check=`test -z "$correrct_residue_comm" && echo "" || echo "; color green, resi $correrct_residue_comm"`
echo $correrct_residue_comm_check
