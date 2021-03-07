#!/bin/bash

# for file in /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Antogen/predictionvalue/res_pred/docksort/*
# do 
#     sed -i "" 's/      /,/g' $file 
# done 

for file in /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Antogen/InterfaceResidues/*
do 
    sed -i "" 's/	 /_/g' $file 
done 
