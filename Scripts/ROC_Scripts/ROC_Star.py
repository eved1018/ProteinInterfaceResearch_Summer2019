import pandas as pd
import numpy as np
import os 
import re 
def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]


def logreg_Star_set_up():
    cols = ['residue', 'predus', 'ispred', 'dockpred', 'logreg','annotated']
    star = pd.DataFrame(columns= cols)
    col_names = ['residue', 'predus', 'ispred', 'dockpred', 'annotated','logreg']
    RF_dir="/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/CrossVal/Crossvaltest2"
    for folder in os.listdir(RF_dir):
        if folder.startswith("CV"):
            path = "/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/CrossVal/Crossvaltest2/{}".format(folder)
            for filename in os.listdir(path):
                if filename.startswith("pred"):
                    path = "/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/CrossVal/Crossvaltest2/{}/{}".format(folder,filename)
                    data = pd.read_csv(path, header=0 ,names=col_names)
                    data = data[cols]
                    data = data.round({'predus': 3, 'ispred': 3, 'dockpred': 3, 'logreg': 3})
                    star = pd.concat([star,data], axis=0)
                star = star.drop(columns ="residue")
                starinterface = star[star.annotated == 1] 
                starnonintr = star[star.annotated == 0] 
                starinterface = starinterface.drop(columns="annotated")
                starnonintr  = starnonintr.drop(columns="annotated")
                path = "/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/CrossVal/star/logStarinterface.csv"
                starinterface.to_csv(path,sep="\t", index=False, header=True)
                path = "/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/CrossVal/star/logStarnoninterface.csv"
                starnonintr.to_csv(path,sep="\t", index=False, header=True)

    # star = star.drop(columns ="residue")
    # starinterface = star[star.annotated == 1] 
    # starnonintr = star[star.annotated == 0] 
    # starinterface = starinterface.drop(columns="annotated")
    # starnonintr  = starnonintr.drop(columns="annotated")
    # path = "/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/CrossVal/star/logStarinterface.csv"
    # starinterface.to_csv(path,sep="\t", index=False, header=True)
    # path = "/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/CrossVal/star/logStarnoninterface.csv"
    # starnonintr.to_csv(path,sep="\t", index=False, header=True)


# logreg_Star_set_up()

def RF_Star_set_up():
    cols = ['residue', 'predus', 'ispred', 'dockpred', 'rfscore','annotated']
    star = pd.DataFrame(columns= cols)
    col_names = ['residue', 'predus', 'ispred', 'dockpred', 'annotated','rfscore']
    RF_dir="/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/CrossVal/Crossvaltest2"
    for folder in os.listdir(RF_dir):
        if folder.startswith("CV"):
            path = "/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/CrossVal/Crossvaltest2/{}".format(folder)
            for filename in os.listdir(path):
                if filename.startswith("RF"):
                    path = "/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/CrossVal/Crossvaltest2/{}/{}".format(folder,filename)
                    data = pd.read_csv(path, header=0 ,names=col_names)
                    data = data[cols]
                    data = data.round({'predus': 3, 'ispred': 3, 'dockpred': 3, 'rfscore': 3})
                    # print(data.head())
                    star = pd.concat([star,data], axis=0)
    star = star.drop(columns ="residue")
    starinterface = star[star.annotated == 1] 
    starnonintr = star[star.annotated == 0] 
    starinterface = starinterface.drop(columns="annotated")
    starnonintr  = starnonintr.drop(columns="annotated")
    path = "/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/CrossVal/Star/RFStarinterface.csv"
    starinterface.to_csv(path,sep="\t", index=False, header=True)
    path = "/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/CrossVal/Star/RFStarnoninterface.csv"
    starnonintr.to_csv(path,sep="\t", index=False, header=True)

# RF_Star_set_up()

def funcname():
    for i in np.arange(0.00, 1.02, .01):
        print(i)

funcname()