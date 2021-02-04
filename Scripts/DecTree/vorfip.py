import pandas as pd
import numpy as np
import statsmodels.api as sm
import os 
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import graphviz
import pydot 
from sklearn import tree
import matplotlib.pyplot as plt
import math 
from sklearn.datasets import *
from dtreeviz.trees import *
import re 
import time 
import concurrent.futures
import subprocess
import re
import streamlit as st
import imgkit

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]


def vorfip_setup():
    annotated_path = "/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Annotated_Residues/AnnotatedTotal"
   
    annlist =os.listdir(annotated_path)
    annlist.sort(key=natural_keys)
    vorfip_path = "/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Vorfip/vorffip_proteins"
    vorlist =os.listdir(vorfip_path)
    vorlist.sort(key=natural_keys)
    proteins = []

    for filename in annlist: 
        tosplit = filename.split("_")
        proteinname = tosplit[0]
        proteins.append(proteinname)
    print(len(proteins))
    for filename in vorlist:
        tosplit =  filename.split(".")
        proteinname = f"{tosplit[0]}.{tosplit[1]}"
        proteinname =proteinname.upper()
        if proteinname in proteins:
            path = f"{vorfip_path}/{filename}"
            endpath = f"/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Vorfip/vorfip_223/{proteinname}.txt"
            subprocess.call(["cp",path,endpath])
# vorfip_setup()

def ROC_Curve(frame,protein_list,annotated_res_prot):
    TPRS = []
    FPRS = []
    threshholds= []
    for i in np.arange(0.00, 1.02, .01):
        threshhold = float(str(round(i,2)))    
        proteinname = frame.index 
        all_res_sum = 0 # total res 
        N_sum = 0 # total annotated 
        pred_sum = 0 #total over threshold 
        TP_Total_sum = 0 #sum of TP
        FP_Total_sum = 0 #sum of FP
        Neg_Total_sum = 0 #sum of neg st)
        for protein in protein_list:
            # print(protein)
            # col_names = [ 'residue','predus', 'ispred', 'dockpred', 'annotated','rfscore','logreg']
            # counterframe = pd.DataFrame(columns = col_names)
            rows = []
            for protein_res in proteinname: 
                if protein in protein_res:
                    rows.append(protein_res)
            counterframe = frame[frame.index.isin(rows)]
            # print(counterframe.head())
            cols = ['residue', 'vorfip']
            counterframerf = pd.DataFrame(columns = cols)
            # counterframerf = counterframe.index
            counterframerf = counterframe[['vorfip']] 
            # counterframerf.reset_index(level=0, inplace=True)
            # counterframerf.rename({"index": "residue", " rfscore": "rfscore"}, axis='columns', inplace=True)
            # print(counterframerf.head())
            # pred_res = counterframerf.index
            seq_res = counterframerf.index.values.tolist()
            seqnum = len(seq_res)
            pred_score= counterframerf.vorfip
            predictedframesort = counterframerf.sort_values(by=['vorfip'], inplace =False, ascending=False)
            
            thresholdframe= predictedframesort[predictedframesort.vorfip >= threshhold] 
            # print(thresholdframe.head())
            
            predicted_res = thresholdframe.index.values.tolist()
            predicted_res = [str(i) for i in predicted_res]
            pred_res = []
            for i in predicted_res: 
                res_prot = i.split("_")
                res = res_prot[0]
                pred_res.append(res)
            N = 0
            annotated_res =[]
            for i in annotated_res_prot:
                if protein in i:
                    tosplit = i.split("_")
                    res = tosplit[0]
                    # print(res)
                    annotated_res.append(res)
                    N +=1
            
            Truepos = []
            for res in annotated_res:
                if res in pred_res:
                    Truepos.append(res)
            pred = len(pred_res)
            TP = len(Truepos)
            N = len(annotated_res)
            TPR = TP/N 
            FP = pred - TP
            neg = seqnum - N
            FPR = FP/neg
            TP_Total_sum += TP
            FP_Total_sum += FP
            all_res_sum += seqnum # total res 
            N_sum += N # total annotated 
            pred_sum += pred #total over threshold 
            Neg_Total_sum += neg  
        Global_TPR = TP_Total_sum / N_sum
        TPRS.append(Global_TPR)
        Global_FPR = FP_Total_sum / Neg_Total_sum
        FPRS.append(Global_FPR)
        threshholds.append(threshhold)
    print(len(TPRS))
    print(len(FPRS))
    print(len(threshholds))
    final_results = pd.DataFrame(
    {'threshold': threshholds,
     'TPR': TPRS,
     'FPR': FPRS
    })
    
    distance = final_results["FPR"].diff()
    midpoint  = final_results["TPR"].rolling(2).sum()
    distance = distance * -1
    AUC = (distance) * (midpoint)
    AUC = AUC/2
    sum_AUC = AUC.sum()
    print(sum_AUC)

def vorfip_allign():
    path = "/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/PDB_Files/NoxDBbypdb"
    pathlist = os.listdir(path)
    pathlist.sort(key=natural_keys)
    vorfip_frame_total = pd.DataFrame()
    residues_total =[]
    vals_total =[]
    protein_list = []
    for i in pathlist:
        len_path = f"{path}/{i}"
        len_frame = pd.read_csv(len_path, header =0 )
        len_list = len_frame.residue.values.tolist()
        length  = len(len_list)
        to_split = i.split("RFval")
        to_split_2 = to_split[1]
        to_split_3 = to_split_2.split(".")
        proteinname = f"{to_split_3[0]}.{to_split_3[1]}"
        
        vorfip_path = f"/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Vorfip/vorfip_223/{proteinname}.txt"
        cols = ["a","b","c"]
        vorfip_frame = pd.read_csv(vorfip_path, delimiter="\t", names= cols)
        vorfip_scores = vorfip_frame['a'].values.tolist()
        vorfip_len = len(vorfip_scores)
        # if proteinname == "1BML.A":
        #     print(proteinname)
        #     print(len_list)
        #     print(vorfip_scores)
        #     print(length)
        #     print(vorfip_len)

        if vorfip_len == length:
            protein_list.append(proteinname)
            # print(proteinname, "alligned")
            for i in len_list:
                # print(i)
                res_prot = f"{i}_{proteinname}"
                residues_total.append(res_prot)
            vals_total.extend(vorfip_scores)     

        else:
            pass
            # print(proteinname, "not alligned")
    vorfip_frame_total['residue'] = residues_total
    vorfip_frame_total['vorfip'] = vals_total
    # print(vorfip_frame_total.head())
    data_path = "/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/final_sort.csv"
    cols = ['residue', 'predus', 'ispred', 'dockpred', 'annotated']
    frame = pd.read_csv(data_path,names = cols)
    vorfip_join_frame = pd.merge(frame, vorfip_frame_total, on='residue', how='inner')
    vorfip_join_frame.set_index('residue', inplace= True )
    path = "/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Vorfip/223_data_allign.csv"
    vorfip_join_frame.to_csv(path,sep=",", index=True, header=True)
    annotated_frame = vorfip_join_frame[vorfip_join_frame['annotated'] == 1 ]
    annotated_res_prot = annotated_frame.index.tolist()
    print(len(protein_list))
    ROC_Curve(vorfip_join_frame,protein_list,annotated_res_prot)

vorfip_allign()


def vorfip_load():
    proteins_list = []
    endpath = "/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Vorfip/vorfip_223"
    pathlist =os.listdir(endpath)
    pathlist.sort(key=natural_keys)
    
    data = pd.DataFrame()
    residues = []
    vals = []
    for filename in pathlist:
        tosplit = filename.split(".txt")
        proteinname = tosplit[0]
        proteins_list.append(proteinname)       
        # print(proteinname)
        path = f"{endpath}/{filename}"
        cols = ["a","b","c"]
        protein_data = pd.read_csv(path, delimiter="\t", names= cols)
        # print(protein_data.head())
        res = protein_data["c"].values
        for i in res:
            prot_res = f"{i}_{proteinname}"
            residues.append(prot_res)
        val = protein_data["a"].tolist()
        for i in val:
            vals.append(i)
    print(len(residues))
    print(len(vals))
    

    data["residue"] = residues
    data["vorfip"] = vals
    # print(data.head())
    data_path = "/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/final_sort.csv"
    cols = ['residue', 'predus', 'ispred', 'dockpred', 'annotated']
    frame = pd.read_csv(data_path,names = cols)
    print(len(frame))
    frame = frame.merge(data, on="residue")
    frame = frame[['residue', 'predus', 'ispred', 'dockpred', "vorfip", 'annotated']]
    frame.set_index('residue', inplace= True )
    
    annotated_frame = frame[frame['annotated'] == 1 ]
    annotated_res_prot = annotated_frame.index.tolist()


    path = "/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Vorfip/223_data.csv"
    frame.to_csv(path,sep=",", index=True, header=True)
    ROC_Curve(frame,proteins_list,annotated_res_prot)







# vorfip_load()



    