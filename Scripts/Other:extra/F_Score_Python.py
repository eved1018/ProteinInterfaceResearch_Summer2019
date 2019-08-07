#!/bin/python
import os
import sys

def Fscore():
    file_list = (sys.argv)
    fileA = file_list[1]
    fileB = file_list[2]
    fileid = file_list[3]
    my_set1 = set()
    my_set2 = set()
    head = 0
    
    with open(fileA, 'r+') as file1:

            for line in file1:
                sentence = line.replace('\t'," ")
                sentence = sentence.replace('\n',"")
                my_set1.add(sentence)
                head += 1

            with open(fileB, 'r+') as file2:
                firstNlines = file2.readlines()[0:head]

                for line2 in firstNlines:
                    sentence2 = line2.replace('\n', "")
                    my_set2.add(sentence2)

            known_residues = len(my_set1)
            print(known_residues, "experimental/known interface")
            print(my_set1)

            predicted_residues = len(my_set2)
            print(predicted_residues, "predicted interface")
            print(my_set2)

            True_Positives = len(my_set1 & my_set2)
            print("correctly predicted s")
            print(my_set1 & my_set2)

            False_positives = len(my_set2 - my_set1)
            print("incorrectly predicted ")
            print(my_set2 - my_set1)

            print("true positives", True_Positives)
            print("False positives", False_positives)
            print("residues", known_residues)

            F_score = True_Positives / known_residues
            print("F_score = ", F_score)


            filepath = str(os.getcwd())
            filepath_new = filepath + "F_score_python.txt"
            with open(filepath_new, 'a+') as file3:
                file3.write(fileid)
                file3.write("    ")
                file3.write(str(F_score))
                file3.write("\n")


Fscore()
