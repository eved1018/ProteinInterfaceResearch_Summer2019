import pymolpredus
from pymol import cmd
from pathlib import Path
import re
import csv
import codecs

import os
import sys


os.chdir(os.path.dirname(sys.argv[0])) # change dir to this file's dir


class PredictMethod:
    def __init__(self, name, directory):
        self.name = name
        self.dir = directory

class Residues:
    def __init__(self, color):
        self.color = color
        self.residues = []
        self.selection_string = "none"

def saveProteinImages(method, protein_name, annotated, correct, wrong):
    global rotator
    cmd.delete("all")

    print(f"PROTEIN NAME: {protein_name}")

    cmd.fetch(protein_name, async_=0)
    cmd.color("0xFFFFFF") # colors the entire protein white (so that the predictions can be colored)

    cmd.hide("lines")
    cmd.hide("spheres")
    cmd.show("cartoon")
    
    cmd.color(annotated.color, annotated.selection_string) # colors annotated blue
    cmd.color(wrong.color, wrong.selection_string) # colors wrongly predicted red
    cmd.color(correct.color, correct.selection_string) # colors correctly predicted green

    cmd.show("spheres", annotated.selection_string)
    cmd.show("spheres", correct.selection_string)
    cmd.show("spheres", wrong.selection_string)

    sphere_size = f"vdw={SPHERE_SIZE}"     # the size of the rendered spheres
    cmd.alter(wrong.selection_string, sphere_size)    # changes the sphere size
    cmd.alter(correct.selection_string, sphere_size)
    cmd.alter(annotated.selection_string, sphere_size)
    cmd.rebuild() # rerenders the spheres to the new size

    cmd.remove("resn hoh")  # removes the HOH's from image 
    cmd.orient(annotated.selection_string)
    cmd.zoom(complete=1)
    cmd.set("depth_cue", "0")       # removes shadows of depth
    cmd.center(protein_name)

    rotator = pymolpredus.Rotate(
        method, protein_name, correct.selection_string, wrong.selection_string)

    rotator.generate_images(INCREMENT, WIDTH, HEIGHT)

def read_method_predictions(proteinFileString):
    proteinFile = open(str(proteinFileString), 'r')
    predictions_list = list( csv.reader(proteinFile) )
    predictions_list = [[int(x), float(y)] for x,y in predictions_list]
    # values are stored as such: proteinResList = [ ['128', '0.52'], ['129', '0.46'], ...]

    predictions_list.sort(key=(lambda x: x[1]), reverse=True) # sorts using highest score

    return predictions_list

def classify_predictions(protein_name, method_predictions,annotated, wrong, correct):
    for residue in method_predictions:
        # checks if it was correctly predicted
        # residue[0] is the residue num, while residue[1] is it's score
        if residue[0] in ANNOTATED_DICT[protein_name]:
            correct.residues.append(residue[0])
        else:
            wrong.residues.append(residue[0])


def gen_prediction_images(method):

    wrong = Residues("0xFF0000") # red
    correct = Residues("0x00FF00") # green
    annotated = Residues("0x0000FF") # blue
    
    for proteinFileString in (PREDICTION_DIR/method.dir).iterdir():
        protein_name = (re.split(r"[./_]", str(proteinFileString))[11]).lower() # gets protein name
        
        if protein_name == '':
            continue
        if protein_name == "1tfh": # for some reason annotated is missing 1tfh so it is skipped for now
            continue 
        # if protein_name != "2vpf":
        #     continue  
        
        annotated.residues = ANNOTATED_DICT[protein_name]
        CUTOFF = len(annotated.residues)
        # takes the 'CUTOFF' number of highest scoring residues. E.g. if CUTOFF == 2, it takes the 2 highest 

        method_predictions = read_method_predictions(proteinFileString)[0:CUTOFF]

        classify_predictions(protein_name, method_predictions, annotated, wrong, correct)

        annotated.selection_string = "resi " + "+".join(map(str, annotated.residues))
        if len(correct.residues) > 0:
            correct.selection_string = "resi " + "+".join(map(str, correct.residues))
        if len(wrong.residues) > 0:
            wrong.selection_string = "resi " + "+".join(map(str, wrong.residues))
        
        
        saveProteinImages(method, protein_name, annotated, correct, wrong)

# Deletes the images, gifs, and videos that were previously outputed
def delete_previous():
    os.system("find ../../Antogen/pymolimages/ -type f -name \"*.png\" -delete")
    os.system("find ../../Antogen/pymolimages/ -type f -name \"*.gif\" -delete")
    os.system("find ../../Antogen/pymolimages/ -type f -name \"*.mp4\" -delete")

# Creates a dictionary of the annotated values. E.g. dict["1a43"] = [21, 23, 24, ...]
def create_annotated_dict():
    annotatedDict = {}
    for annotatedFileString in (PREDICTION_DIR/"annotated").iterdir():
        protein_name = (re.split(r"[./_]", str(annotatedFileString))[11]).lower() # gets protein name

        annotatedFile = open(str(annotatedFileString), 'r')
        annotatedResListTemp = list(csv.reader(annotatedFile))
        annotatedResList = []
        for res in annotatedResListTemp:
            annotatedResList.append(int(res[0]))

        annotatedResList.sort()
        annotatedDict[protein_name] = annotatedResList

    return annotatedDict

# returns a list of all the proteins names: list = ["1a43", 1bv1", ...]
def get_all_protein_names():
    temp = []
    for folder in PREDICTION_DIR.iterdir():
        if folder.is_file():
            continue
        for protein_file in folder.iterdir():
            if protein_file.name[:4].lower() not in temp and protein_file.suffix == ".csv":
                temp.append(protein_file.name[:4].lower())
    return temp

rotator = None

# SETTINGS VARIABLES
# where the predictions are stored
PREDICTION_DIR = Path("../../Antogen/predictionvalue/res_pred")

# Methods of prediction
PREDICTION_METHODS = [
    PredictMethod("Predus", "predus"),
    PredictMethod("ISPRED", "ispred"),
    PredictMethod("DockPred", "dockpred")
]
WIDTH, HEIGHT = 700, 700
INCREMENT = 30
SPHERE_SIZE = 1.2
PROTEINS_TO_RUN = get_all_protein_names()


delete_previous()
ANNOTATED_DICT = create_annotated_dict()


for method in PREDICTION_METHODS:
    gen_prediction_images(method)


# pymol -cq pymolimaging.py

#rotator = pymolpredus.Rotate(\"${proteinname}\", \"$correct_residue_comm\", \"$predus_residue_comm\")
#rotator.take_pictures()


# DEBUGGING
# print("AAAAAAAAAA")
# print(f"Length: {len(method_predictions)}\nRes list: {method_predictions}\n\n")

# print(f"\nLength: {len(annotated.residues)}\nAnnonated: {annotated.residues}")
# print(f"\nLength: {len(correct.residues)}\nCorrect: {correct.residues}")
# print(f"\nLength: {len(wrong.residues)}\nIncorrect: {wrong.residues}")
# print("AAAAAAAAAA")
# print(correct.selection_string)