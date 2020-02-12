#!/usr/bin/env python

# imports
import pandas as pd
from sklearn.linear_model import LogisticRegression, LogisticRegressionCV 
from sklearn.linear_model import LassoCV, LassoLarsCV, LassoLarsIC
from sklearn import metrics
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from random import *
import statsmodels.api as sm

# set table of data

aucframe= pd.DataFrame({})

#  create logistic regresion function

def log_reg_nox():
    col_names = ['residue', 'predus', 'ispred', 'dockpred', 'annotated']
    # load dataset
    df = pd.read_csv("/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/noxdata.csv", header=None, names=col_names)
    # print(df.head())
    df.isnull().any()
    data = df.fillna(method='ffill')
    feature_cols = ['predus', 'ispred', 'dockpred']
    protein = data.residue
    X = data[feature_cols] # Features
    y = data.annotated # Target variable
    # X_train,X_test,y_train,y_test=train_test_split(X,y)
    # instantiate the model (using the default parameters)
    logreg = LogisticRegression()
    # fit the model with data
    logreg.fit(X,y)
    x = sm.add_constant(X)
    logit_model=sm.Logit(y,x)
    result=logit_model.fit()
    print(result.summary2())
    print(logreg.coef_)
    print(logreg.intercept_)
    coefficients = result.params
    print(coefficients)
    #output
    benchmark= pd.read_csv('/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/benchmarkdata.csv', header=None, names=col_names)
    protein= benchmark.residue
    predusval = benchmark.predus
    ispredval = benchmark.ispred
    dockpred = benchmark.dockpred
    predcoef = logreg.coef_[0,0]
    ispredcoef = logreg.coef_[0,1]
    dockpredcoef= logreg.coef_[0,2]
    val = (logreg.intercept_ + predcoef * predusval + ispredval* ispredcoef +dockpred * dockpredcoef)*(-1)
    # print(val)
    exponent = np.exp(val)
    # print(exponent)
    pval = (1/(1+exponent))
    results = pd.DataFrame({"residue": protein, "prediction value": pval})
    path="/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/predictionvalues/benchmarkpredictionvalues.csv"
    results.to_csv(path,sep=",", index=False, header=True)
    

    # #auc
    # y_pred_proba = logreg.predict_proba(X_test)[::,1]
    # print(y_pred_proba)
    # fpr, tpr, threshold = metrics.roc_curve(y_test,  y_pred_proba)
    # final = pd.DataFrame({"fpr": fpr, "tpr": tpr,"threshold": threshold})
    # # print(final)
    # auc = metrics.roc_auc_score(y_test, y_pred_proba)
    # plt.plot(fpr,tpr,label="data 1, auc="+str(auc))
    # plt.legend(loc=4)
    # results = pd.DataFrame({"predicted": y_pred, "annotated": y)
    # print(auc)
    # path="/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/regresiondatanox.txt"
    # results.to_csv(path,sep=",", index=False, header=True)
    # plt.show()
    # return auc

log_reg_nox()


def log_reg_bnch():
    col_names = ['residue', 'predus', 'ispred', 'dockpred', 'annotated']
    # load dataset
    df = pd.read_csv("/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/benchmarkdata.csv", header=None, names=col_names)
    df.isnull().any()
    data = df.fillna(method='ffill')
    feature_cols = ['predus', 'ispred','dockpred']
    protein = data.residue
    X = data[feature_cols] # Features
    y = data.annotated # Target variable
    # X_train,X_test,y_train,y_test=train_test_split(X,y)
    # instantiate the model (using the default parameters)
    logreg = LogisticRegression()
    # fit the model with data
    logreg.fit(X,y)
    # import statsmodels.api as sm
    x = sm.add_constant(X)
    logit_model=sm.Logit(y,x)
    result=logit_model.fit()
    print(result.summary2())
    print(logreg.coef_)
    print(logreg.intercept_)
    coefficients = result.params
    print(coefficients)
    #prediction
    # prediction value 
    nox= pd.read_csv('/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/noxdata.csv', header=None, names=col_names)
    protein= nox.residue
    predusval = nox.predus
    ispredval = nox.ispred
    dockpred = nox.dockpred
    predcoef = logreg.coef_[0,0]
    ispredcoef = logreg.coef_[0,1]
    dockpredcoef= logreg.coef_[0,2]
    val = (logreg.intercept_ + predcoef * predusval + ispredval* ispredcoef +dockpred * dockpredcoef)*(-1)
    exponent = np.exp(val)
    pval = (1/(1+exponent))
    results = pd.DataFrame({"residue": protein, "prediction value": pval})
    path="/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/predictionvalues/noxpredictionvalues.csv"
    results.to_csv(path,sep=",", index=False, header=True)
log_reg_bnch()
