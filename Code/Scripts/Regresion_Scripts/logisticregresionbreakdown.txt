#!/usr/bin/env python

# imports 
import pandas as pd
# pandas dataframe is used to read the csv file 
import numpy as np
# numpy is used to compute exponents for the pval 
import statsmodels.api as sm
# statsmodel includes the logistic regresion script 

# set table of data

aucframe= pd.DataFrame({})

#  create logistic regresion function

def log_reg_nox():
    col_names = ['residue', 'predus', 'ispred', 'dockpred', 'annotated']
     # read the csv file and assign column names 
    df = pd.read_csv("/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/noxdata.csv", header=None, names=col_names)
    # if any data is empty it is changed to null and not computed into the logistic regresion algorithim  
    df.isnull().any()
    data = df.fillna(method='ffill')
    # sets which columns are used in the logistic regresion 
    feature_cols = ['predus','ispred','dockpred']
     # defines var protein as the first column of the cvs file 
    protein = data.residue
    #  sets x as the dependent variables and y and the dependent variable 
    X = data[feature_cols] # Features - prediction score for each prediction algorithims 
    y = data.annotated # Target variable - 0 for non0interface 1 for interface 
    # implimentation of teh logistic regresion from statsmodel 
    x = sm.add_constant(X)
    logit_model=sm.Logit(y,x)
    result=logit_model.fit()
    # print out the summery of teh regresion 
    print(result.summary2())
    # set the transformation coefficiants as variables 
    coefficients = result.params
    # read in the benchmark data to compute Pval 
    benchmark= pd.read_csv('/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/benchmarkdata.csv', header=None, names=col_names)
    # assign variables for each column 
    protein= benchmark.residue
    predusval = benchmark.predus
    ispredval = benchmark.ispred
    dockpred = benchmark.dockpred
    # assigns transformation coeeficiants for each prediction algorithim 
    predcoef = coefficients[1]
    ispredcoef = coefficients[2]
    dockpredcoef= coefficients[3]
    # compute Pval 
    val = (coefficients[0] + predcoef * predusval + ispredval* ispredcoef+dockpred * dockpredcoef)*(-1)
    exponent = np.exp(val)
    pval = (1/(1+exponent))
    # save results 
    results = pd.DataFrame({"residue": protein, "prediction value": pval})
    path="/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/predictionvalues/predus_ispred_dockpred/benchmarkpredictionvalues.csv"
    results.to_csv(path,sep=",", index=False, header=True)
log_reg_nox()