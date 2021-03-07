#!/usr/bin/env bash

# for f in /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/PDB_Files/PDB241/Nox_Raji_PDB/*
# do
#   curl -F "file=$f" https://honiglab.c2b2.columbia.edu/PredUs/index_omega.html
# done

file=/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/PDB_Files/PDB241/Nox_Raji_PDB/1a0f_A.pdb
# curl -d file=${file} https://honiglab.c2b2.columbia.edu/PredUs/index_omega.html

# curl --form pdbfile=@${file}   \
#      https://honiglab.c2b2.columbia.edu/PredUs/index_omega.html

# curl -X POST -H "Content-Type: multipart/form-data" -d @${file} https://honiglab.c2b2.columbia.edu/PredUs/index_omega.html

# curl -F "file=$file" https://honiglab.c2b2.columbia.edu/PredUs/index_omega.html

# curl -d $file -H "enctype= multipart/form-data" -X POST https://honiglab.c2b2.columbia.edu/PredUs/index_omega.html

curl --upload-file "$file" https://honiglab.c2b2.columbia.edu/PredUs/index_omega.html
