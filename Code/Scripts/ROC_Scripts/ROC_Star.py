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
    # os.mkdir("/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/CrossVal/Crossvaltest5/Log/star")
    star = pd.DataFrame(columns= cols)
    col_names = ['residue', 'predus', 'ispred', 'dockpred', 'annotated','logreg']
    RF_dir="/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/CrossVal/Crossvaltest5/tests"
    for folder in os.listdir(RF_dir):
        if folder.startswith("CV"):
            path = "/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/CrossVal/Crossvaltest5/tests/{}".format(folder)
            for filename in os.listdir(path):
                if filename.startswith("pred"):
                    path = "/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/CrossVal/Crossvaltest5/tests/{}/{}".format(folder,filename)
                    data = pd.read_csv(path, header=0 ,names=col_names)
                    data = data[cols]
                    data = data.round({'predus': 3, 'ispred': 3, 'dockpred': 3, 'logreg': 3})
                    star = pd.concat([star,data], axis=0)
        star = star.drop(columns ="residue")
        starinterface = star[star.annotated == 1] 
        starnonintr = star[star.annotated == 0] 
        starinterface = starinterface.drop(columns="annotated")
        starnonintr  = starnonintr.drop(columns="annotated")
        path = "/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/CrossVal/Crossvaltest5/Log/star/logStarinterface{}.csv".format(folder)
        starinterface.to_csv(path,sep="\t", index=False, header=True)
        path = "/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/CrossVal/Crossvaltest5/Log/star/logStarnoninterface{}.csv".format(folder)
        starnonintr.to_csv(path,sep="\t", index=False, header=True)


# logreg_Star_set_up()

def RF_Star_set_up():
    os.mkdir("/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/CrossVal/Crossvaltest5/Star")
    cols = [ 'residue', 'predus', 'ispred', 'dockpred', 'rfscore','annotated']
    log_cols = ['residue', 'predus', 'ispred', 'dockpred', 'annotated','logreg']
    star = pd.DataFrame(columns= cols)
    col_names = ['residue', 'predus', 'ispred', 'dockpred', 'annotated','rfscore']
    RF_dir="/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/CrossVal/Crossvaltest5/tests"
    for folder in os.listdir(RF_dir):
        if folder.startswith("CV"):
            path = "/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/CrossVal/Crossvaltest5/tests/{}".format(folder)
            for filename in os.listdir(path):
                if filename.startswith("RF"):
                    nums = filename.split("val")
                    num = nums[1]
                    print(num)
                    path = "/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/CrossVal/Crossvaltest5/tests/{}/{}".format(folder,filename)
                    logpath = "/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/CrossVal/Crossvaltest5/tests/{}/predval{}".format(folder,num)
                    logframe = pd.read_csv(logpath, header =0 , names =log_cols)
                    logs = logframe["logreg"]
                    data = pd.read_csv(path, header=0 ,names=col_names)
                    # print(data.head())
                    data = data[cols]
                    # print(data.head())
                    data = data.join(logs)
                    data = data.round({'predus': 3, 'ispred': 3, 'dockpred': 3, 'rfscore': 3,"logreg":3})
                    star = star.append(data,ignore_index =True)
        star = star.drop(columns = 'residue')
        starinterface = star[star.annotated == 1] 
        starnonintr = star[star.annotated == 0] 
        starinterface = starinterface.drop(columns="annotated")
        starnonintr  = starnonintr.drop(columns="annotated")
        starinterface =starinterface.rename(columns={'predus':"T1", 'ispred': "T2", 'dockpred':"T3", 'rfscore':"T4",'logreg': 'T5'})
        starnonintr= starnonintr.rename(columns={'predus':"T1", 'ispred': "T2", 'dockpred':"T3", 'rfscore':"T4",'logreg': 'T5'})
        os.mkdir("/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/CrossVal/Crossvaltest5/Star/{}".format(folder))
        path = "/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/CrossVal/Crossvaltest5/Star/{}/RFStarinterface{}.txt".format(folder,folder)
        starinterface.to_csv(path,sep="\t", index=False, header=True)
        path = "/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/CrossVal/Crossvaltest5/Star/{}/RFStarnoninterface{}.txt".format(folder,folder)
        starnonintr.to_csv(path,sep="\t", index=False, header=True)
        star = star.iloc[0:0]
        


# RF_Star_set_up()


