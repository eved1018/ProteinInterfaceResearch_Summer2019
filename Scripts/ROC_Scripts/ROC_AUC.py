import pandas as pd
import numpy as np
import os 
import re 
import math 
def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]


def Rf_AUC_Calc():
    path= "/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/CrossVal/Crossvaltest4/Rf/results"
    filelist = os.listdir(path)
    filelist.sort(key=natural_keys)
    global_AUC = 0
    AUCs =[]
    for filename in filelist:
        if filename.startswith("CV"):
            print(filename)
            path = "/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/CrossVal/Crossvaltest4/Rf/results/{}".format(filename)
            data= pd.read_csv(path, header= 0)
            distance = data["FPR"].diff()
            midpoint  = data["TPR"].rolling(2).sum()
            distance = distance * -1
            AUC = (distance) * (midpoint)
            AUC = AUC/2
            sum_AUC = AUC.sum()
            print(sum_AUC)
            global_AUC += sum_AUC
            AUCs.append(sum_AUC)

    avrg = global_AUC/ len(AUCs)
    omega = 0
    for i in AUCs:
        omega += (i - avrg) **2
    omega = omega/10
    omega = math.sqrt(omega)
    print(omega)
    print(avrg)

def Log_AUC_Calc():
    path= "/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/CrossVal/Crossvaltest4/Log/results"
    filelist = os.listdir(path)
    filelist.sort(key=natural_keys)
    global_AUC = 0
    AUCs =[]
    for filename in filelist:
        if filename.startswith("CV"):
            print(filename)
            path = "/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/CrossVal/Crossvaltest4/Log/results/{}".format(filename)
            data= pd.read_csv(path, header= 0)
            distance = data["FPR"].diff()
            midpoint  = data["TPR"].rolling(2).sum()
            distance = distance * -1
            AUC = (distance) * (midpoint)
            AUC = AUC/2
            sum_AUC = AUC.sum()
            print(sum_AUC)
            global_AUC += sum_AUC
            AUCs.append(sum_AUC)

    avrg = global_AUC/ len(AUCs)
    omega = 0
    for i in AUCs:
        omega += (i - avrg) **2
    omega = omega/10
    omega = math.sqrt(omega)
    print(omega)
    print(avrg)
    
    
                   
Rf_AUC_Calc()                   
# Log_AUC_Calc()