#!/bin/R
# make itrative variabel for protien id's
library(bio3d)
pdbsplit( get.pdb( c("1ACB_E","1ACB_I","1AHW_A","1AK4_A","1AVX_A","1AY7_A","1AY7_B","1BGX_H","1DE4_E","1DFJ_E","1DFJ_I","1DQJ_A","1E4K_C","1E6J_H","1EXB_E","1F34_A","1FC2_D","1FFW_A","1FFW_B","1FLE_E","1GHQ_A","1GXD_A","1GXD_C","1IRA_X","1JIW_I","1JIW_P","1JPS_H","1KAC_A","1KAC_B","1KLU_D"), URLonly=TRUE , path = "/Data_files/Predus/Predus_inputfiles/") )
