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
    def __init__(self, color, is_annotated=False):
        self.color = color
        self.is_annotated = is_annotated

        self.residues = []
        self.selection_string = "none"

    def gen_selection_string(self):
        if len(self.residues) > 0:
            self.selection_string = "resi " + "+".join(map(str, self.residues))

    def clear(self):
        if self.is_annotated:
            return
        self.residues = []
        self.selection_string = "none"


def beautify_images(protein_name, residue_sets):
    cmd.delete("all")

    cmd.fetch(protein_name, async_=0)
    cmd.color("0xFFFFFF") # colors the entire protein white (so that the predictions can be colored)

    cmd.hide("lines")
    cmd.hide("spheres")
    cmd.show("cartoon")

    sphere_size = f"vdw={SPHERE_SIZE}"     # the size of the rendered sphere

    for res_set in residue_sets:
        cmd.color(res_set.color, res_set.selection_string) # colors annotated blue
        cmd.show("spheres", res_set.selection_string)
        cmd.alter(res_set.selection_string, sphere_size)    # changes the sphere size
        
    cmd.rebuild() # rerenders the spheres to the new size
    
    # cmd.color(annotated.color, annotated.selection_string) # colors annotated blue
    # cmd.color(wrong.color, wrong.selection_string) # colors wrongly predicted red
    # cmd.color(correct.color, correct.selection_string) # colors correctly predicted green

    # cmd.show("spheres", annotated.selection_string)
    # cmd.show("spheres", correct.selection_string)
    # cmd.show("spheres", wrong.selection_string)

    # cmd.alter(wrong.selection_string, sphere_size)    # changes the sphere size
    # cmd.alter(correct.selection_string, sphere_size)
    # cmd.alter(annotated.selection_string, sphere_size)
    # cmd.rebuild() # rerenders the spheres to the new size

    cmd.remove("resn hoh")  # removes the HOH's from image 
    cmd.orient(residue_sets[0].selection_string)
    cmd.zoom(complete=1)
    cmd.set("depth_cue", "0")       # removes shadows of depth
    cmd.center(protein_name)


def read_method_predictions(proteinFileString):
    proteinFile = open(str(proteinFileString), 'r')
    predictions_list = list( csv.reader(proteinFile) )
    predictions_list = [[int(x), float(y)] for x,y in predictions_list]
    # values are stored as such: proteinResList = [ ['128', '0.52'], ['129', '0.46'], ...]

    predictions_list.sort(key=(lambda x: x[1]), reverse=True) # sorts using highest score

    return predictions_list

def classify_predictions(protein_name, method_predictions, wrong, correct):
    for residue in method_predictions:
        # checks if it was correctly predicted
        # residue[0] is the residue num, while residue[1] is it's score
        if residue[0] in ANNOTATED_DICT[protein_name]:
            correct.residues.append(residue[0])
        else:
            wrong.residues.append(residue[0])

def non_duplicate_append(list1, list2):
    list1.extend(list2)
    remove_duplicates(list1)

def remove_duplicates(list1):
    aux = []
    for item in list1:
        if item not in aux:
            aux.append(item)
    list1 = aux

def gen_prediction_images():

    for protein in PROTEINS_TO_RUN:

        if protein not in PROTEINS_TO_RUN:
                continue
        if protein == "1TFH": # for some reason annotated is missing 1tfh so it is skipped for now
            continue 
        if protein != "8LYZ":
            continue  

        wrong = Residues("0xFF0000") # red
        correct = Residues("0x00FF00") # green
        annotated = Residues("0x0000FF", is_annotated=True) # blue

        combined_correct = Residues("0x00FF00") # blue
        combined_wrong = Residues("0xFF0000") # blue

        residue_sets = [annotated, correct, wrong]
        combined_sets = [annotated, combined_correct, combined_wrong]

        annotated.residues = ANNOTATED_DICT[protein]
        CUTOFF = len(annotated.residues)

        combined_predictions = []

        for method in PREDICTION_METHODS:
            proteinFileString = PREDICTION_DIR/method.dir/f"{protein}_{method.dir}.csv"

            for res_set in residue_sets:
                res_set.clear()
    
            protein_name = protein

            print(f"protein_name: {protein_name}")
            
            # takes the 'CUTOFF' number of highest scoring residues. E.g. if CUTOFF == 2, it takes the 2 highest 
            method_predictions = read_method_predictions(proteinFileString)[0:CUTOFF]

            non_duplicate_append(combined_predictions, method_predictions)

            classify_predictions(protein_name, method_predictions, wrong, correct)

            for res_set in residue_sets:
                res_set.gen_selection_string()
            
            beautify_images(protein_name, residue_sets)

            print(f"PROTEIN NAME: {protein_name}")

            rotator = pymolpredus.Rotator(OUTPUT_DIR,
                method, protein_name, correct.selection_string, wrong.selection_string)

            rotator.generate_images(INCREMENT, WIDTH, HEIGHT)

        combined_predictions.sort(key=(lambda x: x[1]), reverse=True) # sorts using highest score
        combined_predictions = combined_predictions[0:CUTOFF]
        print(f"COMBINEDDDDDDDD: {combined_predictions}")
        
        for res_set in residue_sets:
            res_set.clear()
        classify_predictions(protein_name, combined_predictions, wrong, correct)

        for res_set in residue_sets:
            res_set.gen_selection_string()

        beautify_images(protein_name, residue_sets)

        combined = PredictMethod("Combined", "combined")

        rotator = pymolpredus.Rotator(OUTPUT_DIR,
                combined, protein_name, correct.selection_string, wrong.selection_string)

        rotator.generate_images(INCREMENT, WIDTH, HEIGHT)


# Deletes the images, gifs, and videos that were previously outputed
def delete_previous():
    os.system("find ../../Antogen/pymolimages/ -type f -name \"*.png\" -delete")
    os.system("find ../../Antogen/pymolimages/ -type f -name \"*.gif\" -delete")
    os.system("find ../../Antogen/pymolimages/ -type f -name \"*.mp4\" -delete")

# Creates a dictionary of the annotated values. E.g. dict["1a43"] = [21, 23, 24, ...]
def create_annotated_dict():
    annotatedDict = {}
    for annotatedFileString in (PREDICTION_DIR/"annotated").iterdir():
        protein_name = (re.split(r"[./_]", str(annotatedFileString))[11]).upper() # gets protein name

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
            if protein_file.name[:4].upper() not in temp and protein_file.suffix == ".csv":
                temp.append(protein_file.name[:4].upper())
    return temp

rotator = None

# SETTINGS VARIABLES
# where the predictions are stored
PREDICTION_DIR = Path("../../Antogen/predictionvalue/res_pred")
OUTPUT_DIR = Path("../../Antogen/pymolimages/")

# Methods of prediction
PREDICTION_METHODS = [
    PredictMethod("Predus", "predus"),
    PredictMethod("ISPRED", "ispred"),
    PredictMethod("DockPred", "dockpred")
]
WIDTH, HEIGHT = 700, 700
INCREMENT = 120
SPHERE_SIZE = 1.2
PROTEINS_TO_RUN = get_all_protein_names()


delete_previous()
ANNOTATED_DICT = create_annotated_dict()



gen_prediction_images()


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