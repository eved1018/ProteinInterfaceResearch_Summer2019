#!/usr/bin/env python

# imports
import pandas as pd
import numpy as np
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
    feature_cols = ['predus','ispred','dockpred']
    protein = data.residue
    X = data[feature_cols] # Features
    y = data.annotated # Target variable
    # X_train,X_test,y_train,y_test=train_test_split(X,y)
    # instantiate the model (using the default parameters)
    # logreg = LogisticRegression()
    # fit the model with data
    # logreg.fit(X,y)
    x = sm.add_constant(X)
    logit_model=sm.Logit(y,x)
    result=logit_model.fit()
    print(result.summary2())
    # print(logreg.coef_)
    # print(logreg.intercept_)
    coefficients = result.params
    benchmark= pd.read_csv('/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/benchmarkdata.csv', header=None, names=col_names)
    protein= benchmark.residue
    predusval = benchmark.predus
    ispredval = benchmark.ispred
    dockpred = benchmark.dockpred
    predcoef = coefficients[1]
    ispredcoef = coefficients[2]
    dockpredcoef= coefficients[3]
    val = (coefficients[0] + predcoef * predusval + ispredval* ispredcoef+dockpred * dockpredcoef)*(-1)
    # print(val)
    exponent = np.exp(val)
    # print(exponent)
    pval = (1/(1+exponent))
    results = pd.DataFrame({"residue": protein, "prediction value": pval})
    path="/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/predictionvalues/predus_ispred_dockpred/benchmarkpredictionvalues.csv"
    results.to_csv(path,sep=",", index=False, header=True)
log_reg_nox()
def log_reg_bnch():
    col_names = ['residue', 'predus', 'ispred', 'dockpred', 'annotated']
    # load dataset
    df = pd.read_csv("/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/benchmarkdata.csv", header=None, names=col_names)
    df.isnull().any()
    data = df.fillna(method='ffill')
    feature_cols = ['predus','ispred','dockpred']
    protein = data.residue
    X = data[feature_cols] # Features
    y = data.annotated # Target variable
    # X_train,X_test,y_train,y_test=train_test_split(X,y)
    # instantiate the model (using the default parameters)
    # logreg = LogisticRegression()
    # fit the model with data
    # logreg.fit(X,y)
    # import statsmodels.api as sm
    x = sm.add_constant(X)
    logit_model=sm.Logit(y,x)
    result=logit_model.fit()
    print(result.summary2())
    coefficients = result.params
    print(coefficients)
    # prediction value 
    nox= pd.read_csv('/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/noxdata.csv', header=None, names=col_names)
    protein= nox.residue
    protein= nox.residue
    predusval = nox.predus
    ispredval = nox.ispred
    dockpred = nox.dockpred
    predcoef = coefficients[1]
    ispredcoef = coefficients[2]
    dockpredcoef= coefficients[3]
    val = (coefficients[0] + predcoef * predusval +  ispredval* ispredcoef+dockpred * dockpredcoef )*(-1)
    exponent = np.exp(val)
    pval = (1/(1+exponent))
    results = pd.DataFrame({"residue": protein, "prediction value": pval})
    path="/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/predictionvalues/predus_ispred_dockpred/noxpredictionvalues.csv"
    results.to_csv(path,sep=",", index=False, header=True)
log_reg_bnch()
def log_reg_nox_ispred_dockpred():
    col_names = ['residue', 'predus', 'ispred', 'dockpred', 'annotated']
    # load dataset
    df = pd.read_csv("/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/noxdata.csv", header=None, names=col_names)
    # print(df.head())
    df.isnull().any()
    data = df.fillna(method='ffill')
    feature_cols = ['ispred','dockpred']
    protein = data.residue
    X = data[feature_cols] # Features
    y = data.annotated # Target variable
    # X_train,X_test,y_train,y_test=train_test_split(X,y)
    # instantiate the model (using the default parameters)
    # logreg = LogisticRegression()
    # fit the model with data
    # logreg.fit(X,y)
    x = sm.add_constant(X)
    logit_model=sm.Logit(y,x)
    result=logit_model.fit()
    print(result.summary2())
    # print(logreg.coef_)
    # print(logreg.intercept_)
    coefficients = result.params
    benchmark= pd.read_csv('/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/benchmarkdata.csv', header=None, names=col_names)
    protein= benchmark.residue
    predusval = benchmark.predus
    ispredval = benchmark.ispred
    dockpredval = benchmark.dockpred
    ispredcoef = coefficients[1]
    dockpredcoef = coefficients[2]
    val = (coefficients[0] + dockpredcoef * dockpredval + ispredval* ispredcoef)*(-1)
    # print(val)
    exponent = np.exp(val)
    # print(exponent)
    pval = (1/(1+exponent))
    results = pd.DataFrame({"residue": protein, "prediction value": pval})
    path="/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/predictionvalues/ispred_dockpred/benchmarkpredictionvalues_ispred_dockpred.csv"
    results.to_csv(path,sep=",", index=False, header=True)
log_reg_nox_ispred_dockpred()
def log_reg_bnch_ispred_dockpred():
    col_names = ['residue', 'predus', 'ispred', 'dockpred', 'annotated']
    # load dataset
    df = pd.read_csv("/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/benchmarkdata.csv", header=None, names=col_names)
    df.isnull().any()
    data = df.fillna(method='ffill')
    feature_cols = ['ispred','dockpred']
    protein = data.residue
    X = data[feature_cols] # Features
    y = data.annotated # Target variable
    # X_train,X_test,y_train,y_test=train_test_split(X,y)
    # instantiate the model (using the default parameters)
    # logreg = LogisticRegression()
    # fit the model with data
    # logreg.fit(X,y)
    # import statsmodels.api as sm
    x = sm.add_constant(X)
    logit_model=sm.Logit(y,x)
    result=logit_model.fit()
    print(result.summary2())
    coefficients = result.params
    print(coefficients)
    # prediction value 
    nox= pd.read_csv('/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/noxdata.csv', header=None, names=col_names)
    protein= nox.residue
    protein= nox.residue
    predusval = nox.predus
    ispredval = nox.ispred
    dockpredval = nox.dockpred
    ispredcoef = coefficients[1]
    dockcoef = coefficients[2]
    val = (coefficients[0] + dockcoef * dockpredval +  ispredval* ispredcoef)*(-1)
    exponent = np.exp(val)
    pval = (1/(1+exponent))
    results = pd.DataFrame({"residue": protein, "prediction value": pval})
    path="/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/predictionvalues/ispred_dockpred/noxpredictionvalues_ispred_dockpred.csv"
    results.to_csv(path,sep=",", index=False, header=True)
log_reg_bnch_ispred_dockpred()
def log_reg_nox_predus_dockpred():
    col_names = ['residue', 'predus', 'ispred', 'dockpred', 'annotated']
    # load dataset
    df = pd.read_csv("/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/noxdata.csv", header=None, names=col_names)
    # print(df.head())
    df.isnull().any()
    data = df.fillna(method='ffill')
    feature_cols = ['predus','dockpred']
    protein = data.residue
    X = data[feature_cols] # Features
    y = data.annotated # Target variable
    # X_train,X_test,y_train,y_test=train_test_split(X,y)
    # instantiate the model (using the default parameters)
    # logreg = LogisticRegression()
    # fit the model with data
    # logreg.fit(X,y)
    x = sm.add_constant(X)
    logit_model=sm.Logit(y,x)
    result=logit_model.fit()
    print(result.summary2())
    # print(logreg.coef_)
    # print(logreg.intercept_)
    coefficients = result.params
    benchmark= pd.read_csv('/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/benchmarkdata.csv', header=None, names=col_names)
    protein= benchmark.residue
    predusval = benchmark.predus
    ispredval = benchmark.ispred
    dockpred = benchmark.dockpred
    preduscoef = coefficients[1]
    dockpredcoef = coefficients[2]
    val = (coefficients[0] + preduscoef * predusval + dockpred* dockpredcoef)*(-1)
    # print(val)
    exponent = np.exp(val)
    # print(exponent)
    pval = (1/(1+exponent))
    results = pd.DataFrame({"residue": protein, "prediction value": pval})
    path="/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/predictionvalues/predus_dockpred/benchmarkpredictionvalues_predus_dockpred.csv"
    results.to_csv(path,sep=",", index=False, header=True)
log_reg_nox_predus_dockpred()
def log_reg_bnch__predus_dockpred():
    col_names = ['residue', 'predus', 'ispred', 'dockpred', 'annotated']
    # load dataset
    df = pd.read_csv("/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/benchmarkdata.csv", header=None, names=col_names)
    df.isnull().any()
    data = df.fillna(method='ffill')
    feature_cols = ['predus','dockpred']
    protein = data.residue
    X = data[feature_cols] # Features
    y = data.annotated # Target variable
    # X_train,X_test,y_train,y_test=train_test_split(X,y)
    # instantiate the model (using the default parameters)
    # logreg = LogisticRegression()
    # fit the model with data
    # logreg.fit(X,y)
    # import statsmodels.api as sm
    x = sm.add_constant(X)
    logit_model=sm.Logit(y,x)
    result=logit_model.fit()
    print(result.summary2())
    coefficients = result.params
    print(coefficients)
    # prediction value 
    nox= pd.read_csv('/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/noxdata.csv', header=None, names=col_names)
    protein= nox.residue
    protein= nox.residue
    predusval = nox.predus
    ispredval = nox.ispred
    dockpred = nox.dockpred
    predcoef = coefficients[1]
    ispredcoef = coefficients[2]
    val = (coefficients[0] + predcoef * predusval +  dockpred* predcoef)*(-1)
    exponent = np.exp(val)
    pval = (1/(1+exponent))
    results = pd.DataFrame({"residue": protein, "prediction value": pval})
    path="/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/predictionvalues/predus_dockpred/noxpredictionvalues_predus_dockpred.csv"
    results.to_csv(path,sep=",", index=False, header=True)
log_reg_bnch__predus_dockpred()