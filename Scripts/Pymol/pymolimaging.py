from Rotator import Rotator
from pymol import cmd
from pathlib import Path
import re
import csv
import codecs

import os
import sys

from enum import Enum


os.chdir(os.path.dirname(sys.argv[0])) # change dir to this file's dir



class PredictMethod:

    def __init__(self, name, directory):
        self.name = name
        self.dir = directory


class ResidueSubset:

    def __init__(self, subset_name, color="0x555555",set_type="PRIMARY"):
        self.color = color
        self.name = subset_name

        # Possible set types are: "PRIMARY", "SECONDARY", and "ANNOTATED"
        self.set_type = set_type 

        self.residues = []
        self.selection_string = "none"

    def gen_selection_string(self):
        if len(self.residues) > 0:
            self.selection_string = "resi " + "+".join(map(str, self.residues))
        else:
            self.selection_string = "none"

    def clear(self):
        if self.set_type == "ANNOTATED":
            return
        self.residues = []
        self.selection_string = "none"

    def __repr__(self):
        return str(self.residues)

    def __str__(self):
        return self.__repr__()


def beautify_images(protein_name, residue_sets):
    cmd.delete("all")

    cmd.fetch(protein_name, async_=0)
    cmd.color("0x555555") # colors the entire protein chrome balck (so that the predictions can be colored)

    cmd.hide("lines")
    cmd.hide("spheres")
    cmd.show("cartoon")

    sphere_size = f"vdw={SPHERE_SIZE}"     # the size of the rendered sphere

    for res_set in residue_sets:
        if res_set.set_type != "ANNOTATED":
            cmd.color(res_set.color, res_set.selection_string) # colors the set of residues
        else:
            cmd.set("label_size", 10)
            cmd.set("label_font_id", 16)
            cmd.set("label_position", (0, 0, 2.5))
            cmd.set("label_color", "white")
            
            cmd.set("label_bg_color", "black")
            cmd.label(res_set.selection_string, "resi")

        # cmd.hide("cartoon", res_set.selection_string)            
        cmd.show("spheres", res_set.selection_string)
        cmd.alter(res_set.selection_string, sphere_size)    # changes the sphere size          

        
    cmd.rebuild() # rerenders the spheres to the new size

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

# The predictions are originally stored as [(17, 0.843), (19, 0.722), ...]
# This function removes that so it's only [17, 19, ...]
def remove_residue_score(predictions):
    out = [x[0] for x in predictions]
    return out

# puts all the true positive in one list and all the false positives in the other
def classify_predictions(protein_name, method_predictions, wrong, correct):
    for residue in method_predictions:
        # checks if it was correctly predicted
        # residue is the residue num, while residue[1] is it's score
        if residue in ANNOTATED_DICT[protein_name]:
            correct.residues.append(residue)
        else:
            wrong.residues.append(residue)


def classify_many_methods(annotated, predictions_dict):
    num_of_colorings = 2**(len(predictions_dict)) - 1

    prime_colors = ["0x0000FF", "0xFF0000", "0xFFFF00"] # Blue, Red, Yellow
    second_colors = ["0xEE82EE", "0x00FF00", "0xFFA500", "0x00FFFF"] # Violet, Green, Orange, Cyan
    permutations = [(0, 1), (0, 2), (1, 2), (0, 1, 2)]
    prime_subsets = []    # a list of ResidueSubsets for the primary predictions
    secondary_subsets = []

    # cycles through the predictions dict to store the primary predictions as ResidueSubsets
    for i, (key, val) in enumerate(predictions_dict.items()):
        sub = ResidueSubset(key, prime_colors[i])
        sub.residues = val

        prime_subsets.append(sub)

    for i, permutation in enumerate(permutations):
        secondary_subsets.append(gen_overlap_subset(permutation, prime_subsets, second_colors[i]))

    all_subsets = []
    all_subsets.append(annotated)
    all_subsets.extend(prime_subsets)
    all_subsets.extend(secondary_subsets)

    for subset in all_subsets:
        subset.gen_selection_string()

    return all_subsets
    
def gen_overlap_subset(permutation, prime_subsets, color):
    name = ""
    overlapping_residues = []
    for i, num in enumerate(permutation):
        name += "-" + prime_subsets[num].name
        if i == 0:
            overlapping_residues = prime_subsets[num].residues
        else:
            overlapping_residues = get_intersection(overlapping_residues, prime_subsets[num].residues)
    
    subset = ResidueSubset(name, color, "SECONDARY")
    subset.residues = overlapping_residues
    
    return subset
            
def get_intersection(list1, list2):
    intersection = []
    for item in list2:
        if item in list1:
            intersection.append(item)
    return intersection

    # COLORS
# BLUE - 0x0000FF
# RED - 0XFF0000
# YELLOW - 0XFFFF00

# GREEN - 0x00FF00
# VIOLET - 0xEE82EE
# ORANGE - 0xFFA500
    

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
        # if protein != "8LYZ":
        #     continue  

        just_predicted = ResidueSubset("Predictions", "0x00FF00")
        wrong = ResidueSubset("False Positive","0xFF0000") # red
        correct = ResidueSubset("True Positive", "0x00FF00") # green
        annotated = ResidueSubset("Annotated", set_type="ANNOTATED") # blue

        residue_sets = [annotated, correct, wrong]
        residue_sets = [annotated, just_predicted]

        annotated.residues = ANNOTATED_DICT[protein]
        CUTOFF = len(annotated.residues)

        # list containing the top 10 predictions of each method (total of 30 predicted residues)
        combined_predictions = []
        predictions_dict = {} # will contain the predictions for this protein from each method

        for method in PREDICTION_METHODS:
            proteinFileString = PREDICTION_DIR/method.dir/f"{protein}_{method.dir}.csv"

            for res_set in residue_sets:
                res_set.clear()

            # takes the 'CUTOFF' number of highest scoring residues. E.g. if CUTOFF == 2, it takes the 2 highest 
            method_predictions = read_method_predictions(proteinFileString)[0:CUTOFF]
            non_duplicate_append(combined_predictions, method_predictions)


            method_predictions = remove_residue_score(method_predictions)


            predictions_dict.setdefault(method.name, method_predictions)
            just_predicted.residues = method_predictions

            # classify_predictions(protein, method_predictions, wrong, correct)

            for res_set in residue_sets:
                
                res_set.gen_selection_string()
            
            beautify_images(protein, residue_sets)

            # print("******************************")
            # print(residue_sets)
            # print("******************************")
            

            rotator = Rotator(OUTPUT_DIR,
                method, protein, residue_sets, GIF_FPS)

            rotator.generate_images(INCREMENT, WIDTH, HEIGHT)

        combined_predictions.sort(key=(lambda x: x[1]), reverse=True) # sorts using highest score
        combined_predictions = combined_predictions[0:CUTOFF]
        
        all_subsets = classify_many_methods(annotated, predictions_dict)

        # print("--------------------------------------------")
        # print(all_subsets)
        # print("--------------------------------------------")
        
        beautify_images(protein, all_subsets)

        combined = PredictMethod("Combined", "combined")


        rotator = Rotator(OUTPUT_DIR,
                combined, protein, all_subsets, GIF_FPS)

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
INCREMENT = 30
SPHERE_SIZE = 1.2
PROTEINS_TO_RUN = get_all_protein_names()

GIF_FPS = 1.5


delete_previous()
ANNOTATED_DICT = create_annotated_dict()


gen_prediction_images()

# COLORS
# BLUE - 0x0000FF
# RED - 0XFF0000
# YELLOW - 0XFFFF00

# GREEN - 0x00FF00
# VIOLET - 0xEE82EE
# ORANGE - 0xFFA500

# pymol -cq pymolimaging.py

#rotator = pymolpredus.Rotate(\"${proteinname}\", \"$correct_residue_comm\", \"$predus_residue_comm\")
#rotator.take_pictures()