#!/bin/R
# make itrative variabel for protien id's
# make sure system taeks in path to testquery and path for output
#ids must be splt but _ not . 
library(bio3d)
my_txt <- readLines("/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Antogen/Antigen_300/proteins.txt")
ids <- c(my_txt)
raw.files <- get.pdb( ids , URLonly=TRUE)
chain.files <- pdbsplit(raw.files, ids, path= "/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Antogen/Antigen_300/Antigen_300_pdbs/")