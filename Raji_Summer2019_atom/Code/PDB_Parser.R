#!/bin/R
# make itrative variabel for protien id's
# make sure system taeks in path to testquery and path for output

library(bio3d)
id <- system("cat Data_files/testquery30" , intern= TRUE )
pdbsplit( get.pdb( c(id), URLonly=TRUE , path = "/Data_files/Predus/Predus_inputfiles/") )
