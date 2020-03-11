import pymolpredus
from pymol import cmd
from pathlib import Path
import re
import csv
import codecs

import os

def saveProteinImages(method, protein_name, annotated, correctly_predicted, wrongly_predicted):
    cmd.delete("all")

    cmd.fetch(protein_name, async=0)
    cmd.color("0xFFFFFF") # colors it all white
    cmd.color(wrongly_predicted["color"], wrongly_predicted["selection_string"]) # colors wrongly blue
    cmd.color("0xFF0000", annotated["selection_string"]) # colors annotated red
    cmd.color(correctly_predicted["color"], correctly_predicted["selection_string"]) # colors correctly green

    cmd.show("spheres", wrongly_predicted["selection_string"])
    cmd.show("spheres", correctly_predicted["selection_string"])
    cmd.show("spheres", annotated["selection_string"])

    cmd.remove("resn hoh")
    cmd.zoom(complete=1)
    cmd.orient(wrongly_predicted["selection_string"])

    cmd.set("depth_cue", "0")
    cmd.center(protein_name)

    rotator = pymolpredus.Rotate(
        method,
        protein_name, 
        correctly_predicted["selection_string"],
        wrongly_predicted["selection_string"])
    rotator.take_pictures()

def sortByScore(item):
    return item[1]  # the 2nd item in each sublist is the score      

def fooThing(dirName):
    wrongly_predicted = {"list": [], "color": "0x0000FF"} # Color: Blue
    correctly_predicted = {"list": [], "color": "0x00FF00"} # Color: Green
    annotated = {"list": [], "color": "0xFF0000"} # Color: Red

    for proteinFileString in (predictionDir/dirName).iterdir():
        protein_name = (re.split(r"[./_]", str(proteinFileString))[11]).lower() # gets protein name
        
        if protein_name == '':
            continue

        if protein_name == "1tfh":
            continue
        

        proteinFile = open(str(proteinFileString), 'r')
        proteinResList = list( csv.reader(proteinFile) )

        proteinResList.sort(key=(lambda x: x[1]), reverse=True)
        proteinResList = proteinResList[0:CUTOFF]
        print()
        print(proteinResList)
        print()
        
        for residue in proteinResList:

            if residue[0] in annotatedDict[protein_name]:
                correctly_predicted["list"].append(residue[0])
            else:
                wrongly_predicted["list"].append(residue[0])

        annotated["list"] = annotatedDict[protein_name]

        correctly_predicted["selection_string"] = "none"
        wrongly_predicted["selection_string"] = "none"

        if len(correctly_predicted["list"]) > 0:
            correctly_predicted["selection_string"] = "resi " + "+".join(correctly_predicted["list"])
        if len(wrongly_predicted["list"]) > 0:
            wrongly_predicted["selection_string"] = "resi " + "+".join(wrongly_predicted["list"])
        
        annotated["selection_string"] = "resi " + "+".join(annotated["list"])

        print()
        print(correctly_predicted["selection_string"])
        print(wrongly_predicted["selection_string"])
        print()
        
        saveProteinImages(dirName.upper(), protein_name, annotated, correctly_predicted, wrongly_predicted)



predictionDir = Path("../../Antogen/predictionvalue/res_pred")
CUTOFF = 2

os.system("find ../../Antogen/pymolimages/ -type f -name \"*.png\" -delete")


annotatedDict = {}
for annotatedFileString in (predictionDir/"annotated").iterdir():
    protein_name = (re.split(r"[./_]", str(annotatedFileString))[11]).lower() # gets protein name

    annotatedFile = open(str(annotatedFileString), 'r')
    annotatedResListTemp = list(csv.reader(annotatedFile))
    annotatedResList = []
    for res in annotatedResListTemp:
        annotatedResList.append(res[0])

    annotatedDict[protein_name] = annotatedResList

fooThing("predus")
fooThing("ispred")
fooThing("dockpred")





# pymol -cq pymolimaging.py

#rotator = pymolpredus.Rotate(\"${proteinname}\", \"$correct_residue_comm\", \"$predus_residue_comm\")
#rotator.take_pictures()