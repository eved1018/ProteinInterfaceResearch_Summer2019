import pandas as pd
import numpy as np
import statsmodels.api as sm
import os 
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.tree import export_graphviz
import graphviz
import pydot 
from sklearn.metrics import roc_auc_score
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.tree import plot_tree
from sklearn.model_selection import RandomizedSearchCV
def Benchstar():
    colums = ['residue', 'predus', 'ispred', 'dockpred', 'score','annotated']
    star = pd.DataFrame(columns= colums)
    cols = ['residue','score']
    columns =['residue', 'predus', 'ispred', 'dockpred', 'meta','annotated']
    col_names = ['residue', 'predus', 'ispred', 'dockpred', 'annotated']
    benchframe  = pd.read_csv("/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/benchmarkdata.csv", names = col_names)
    predframe = pd.read_csv("/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/predictionvalues/predus_ispred_dockpred/benchmarkpredictionvalues.csv",header = 0,names = cols)
    scores = predframe["score"]
    data = benchframe.join(scores)
    data = data.round({'predus': 3, 'ispred': 3, 'dockpred': 3, 'score': 3})
    star = pd.concat([star,data], axis=0)
    star = star.drop(columns ="residue")
    starinterface = star[star.annotated == 1] 
    starnonintr = star[star.annotated == 0] 
    starinterface = starinterface.drop(columns="annotated")
    starnonintr  = starnonintr.drop(columns="annotated")
    starinterface= starinterface.rename(columns={'predus':"T1", 'ispred': "T2", 'dockpred':"T3", 'score':"T4"})
    starnonintr = starnonintr.rename(columns={'predus':"T1", 'ispred': "T2", 'dockpred':"T3", 'score':"T4"})
    path = "/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Results/Star/NoxDB/DBlogStarinterface.txt"
    starinterface.to_csv(path,sep="\t", index=False, header=True)
    path = "/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Results/Star/NoxDB/DBlogStarnoninterface.txt"
    starnonintr.to_csv(path,sep="\t", index=False, header=True)
    star = star.iloc[0:0]
    # path = "/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Results/Star/NoxDB/benchstar.csv"
    # benchframe.to_csv(path,sep=",", index=True, header=True)
    noxframe  = pd.read_csv("/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/noxdata.csv", names = col_names)
    predframe = pd.read_csv("/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/predictionvalues/predus_ispred_dockpred/noxpredictionvalues.csv",header = 0,names = cols)
    scores = predframe["score"]
    data = noxframe.join(scores)
    data = data.round({'predus': 3, 'ispred': 3, 'dockpred': 3, 'score': 3})
    star = pd.concat([star,data], axis=0)
    star = star.drop(columns ="residue")
    starinterface = star[star.annotated == 1] 
    starnonintr = star[star.annotated == 0] 
    starinterface = starinterface.drop(columns="annotated")
    starnonintr  = starnonintr.drop(columns="annotated")
    starinterface =starinterface.rename(columns={'predus':"T1", 'ispred': "T2", 'dockpred':"T3", 'score':"T4"})
    starnonintr=starnonintr.rename(columns={'predus':"T1", 'ispred': "T2", 'dockpred':"T3", 'score':"T4"})
    path = "/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Results/Star/NoxDB/NoxlogStarinterface.txt"
    starinterface.to_csv(path,sep="\t", index=False, header=True)
    path = "/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Results/Star/NoxDB/NOxlogStarnoninterface.txt"
    starnonintr.to_csv(path,sep="\t", index=False, header=True)
    # print(benchframe.head())
    # path = "/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Results/Star/NoxDB/noxstar.csv"
    # noxframe.to_csv(path,sep=",", index=True, header=True)
    

Benchstar()