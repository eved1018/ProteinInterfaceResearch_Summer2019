#!/usr/bin/env python

# imports
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from random import *

# set table of data

aucframe= pd.DataFrame({})

#  create logistic regresion function

def log_reg(numb):
    col_names = ['residue', 'predus', 'ispred', 'dockpred', 'annotated']
    # load dataset
    df = pd.read_csv("/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/ROC_241/final_sort_noheader.csv", header=None, names=col_names)
    # print(df.head())
    df.isnull().any()
    data = df.fillna(method='ffill')

    feature_cols = ['predus', 'ispred', 'dockpred']
    X = data[feature_cols] # Features
    y = data.annotated # Target variable
    X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=numb)

    # instantiate the model (using the default parameters)
    logreg = LogisticRegression()

    # fit the model with data
    logreg.fit(X_train,y_train)

    #prediction
    y_pred=logreg.predict(X_test)
    #output
    cnf_matrix = metrics.confusion_matrix(y_test, y_pred)
    # print(cnf_matrix)
    # print(logreg.coef_)
    # print(logreg.intercept_)

    #auc
    y_pred_proba = logreg.predict_proba(X_test)[::,1]
    fpr, tpr, threshold = metrics.roc_curve(y_test,  y_pred_proba)
    final = pd.DataFrame({"fpr": fpr, "tpr": tpr,"threshold": threshold})
    # print(final)
    auc = metrics.roc_auc_score(y_test, y_pred_proba)
    plt.plot(fpr,tpr,label="data 1, auc="+str(auc))
    plt.legend(loc=4)
    results = pd.DataFrame({"predicted": y_pred_proba, "actual" : y_test})
    # print(auc)
    path="/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/ROC_241/data_241.txt"
    # results.to_csv(path,sep=",", index=False, header=True)
    # plt.show()
    return auc



def main():
    appended_data = []
    for i in range(1,5):
        numb = randrange(10)
        # print(numb)
        result = log_reg(numb)
        print(result)
        data = pd.DataFrame({"trail":[i],"auc":result})

        appended_data.append(data)
    appended_data = pd.concat(appended_data)
    path="/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/ROC_241/auc_random_test.txt"
    appended_data.to_csv(path,sep=",", index=False, header=True)
    print("data was output to" + path)


main()
