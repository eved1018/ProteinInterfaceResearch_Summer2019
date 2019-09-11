#!/bin/R
# make itrative variabel for protien id's
# make sure system taeks in path to testquery and path for output
#ids must be splt but _ not . 
library(bio3d)
id <- "2hmg_pdb"
pdbsplit( get.pdb( c(id), URLonly=TRUE , path = "~/Desktop") )
