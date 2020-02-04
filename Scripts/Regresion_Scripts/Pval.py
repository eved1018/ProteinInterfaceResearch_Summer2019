#!/usr/bin/env python
import pandas as pd

fileA="/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion/noxdata.csv"



col_names = ['residue', 'predus', 'ispred', 'dockpred', 'annotated']
# load dataset
df = pd.read_csv(fileA, header=None, names=col_names)
# print(df.head())
df.isnull().any()
data = df.fillna(method='ffill')

feature_cols = ['predus', 'ispred', 'dockpred']
predus = data.predus
ispred = data.ispred
dockpred = data.ispred

print(predus)
