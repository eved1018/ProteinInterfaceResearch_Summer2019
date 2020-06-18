

# imports
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


def LogReg(test_frame, train_frame,time,cols):
        feature_cols = cols
        X = train_frame[feature_cols]
        y = train_frame.annotated
        x = sm.add_constant(X)
        logit_model=sm.Logit(y,x)
        result=logit_model.fit()
        coefficients = result.params
        folder = "/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/CrossVal/CV{}" .format(time)
        os.mkdir(folder)
        file1 = open("/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/CrossVal/CV{}/cvcoef{}.txt" .format(time,time), "w")
        print(coefficients, file=file1 )
        file1.close()
        protein= test_frame.index
        predusval = test_frame.predus
        ispredval = test_frame.ispred
        dockpred = test_frame.dockpred
        predcoef = coefficients[1]
        ispredcoef = coefficients[2]
        dockpredcoef= coefficients[3]
        val = (coefficients[0] + predcoef * predusval + ispredval* ispredcoef+dockpred * dockpredcoef)*(-1)
        # print(val)
        exponent = np.exp(val)
        # print(exponent)
        pval = (1/(1+exponent))
        results = pd.DataFrame({"residue": protein, "prediction value": pval})
        path="/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/CrossVal/CV{}/predval{}.csv".format(time,time)
        results.to_csv(path,sep=",", index=False, header=True)
        pathtest="/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/CrossVal/CV{}/testframe{}.csv".format(time,time)
        train_frame.to_csv(pathtest,sep=",", index=True, header=True)



def RandomFor(test_frame, train_frame,time,cols): 
        feature_cols = cols
        X = train_frame[feature_cols]
        y = train_frame.annotated
        X_test = test_frame[feature_cols]
        y_test = test_frame.annotated
        protein = test_frame.index 
        model = RandomForestClassifier(n_estimators = 10, random_state = 0, bootstrap=False)
        model.fit(X, y)
        y_prob = model.predict_proba(X_test)
        y_prob_interface = [p[1] for p in y_prob]
        # y_prob_intr_dec = [round(prob, 4) for prob in y_prob_interface]
        results= pd.DataFrame({"residue": protein, "prediction score": y_prob_interface})
        path="/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/CrossVal/CV{}/RFval{}.csv".format(time,time)
        results.to_csv(path,sep=",", index=False, header=True)
        
        


       


def CrossVal():

    aucframe= pd.DataFrame({})
    col_names = ['residue', 'predus', 'ispred', 'dockpred', 'annotated']
    # load dataset
    df = pd.read_csv("/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/final_sort.csv", header=None, names=col_names)
    df.set_index('residue', inplace= True )
    # print(df.head())
    df.isnull().any()
    data = df.fillna(method='ffill')
    feature_cols = ['predus','ispred','dockpred']
    proteinname = data.index
    X = data[feature_cols] # Features
    y = data.annotated # Target variable
    proteinids = []
    for resprot in proteinname: 
        res_prot = resprot.split("_")
        proteinid = res_prot[1]
        if proteinid not in proteinids:
             proteinids.append(res_prot[1])
    # print(len(proteinids))
    lst = proteinids
    n = 22
    chunks = [lst[i:i + n] for i in range(0, len(lst), n)]
    for i in range(0,len(chunks[-1])):
        if len(chunks[-1]) != n:
            pdbs = chunks[-1]
            itt = -(i+2)
            firstlist = []
            firstlist.append(pdbs[0])
            chunks[itt].extend(firstlist)
            chunks[-1].remove(pdbs[0])
    del chunks[-1]
    col_namestest = ['predus', 'ispred', 'dockpred', 'annotated']
    for i in range(0,len(chunks)):
        test_frame = pd.DataFrame(columns = col_namestest)
        train_frame = pd.DataFrame(columns = col_namestest)
        train_frame = data.copy()
        for pdbid in chunks[i]:
            for protein_res in proteinname: 
                if pdbid in protein_res:
                    rows = data.loc[protein_res]
                    test_frame= test_frame.append(rows)
            
        train_frame = train_frame.drop(test_frame.index)
        time = i+1
        # LogReg(test_frame,train_frame,time,feature_cols)
        RandomFor(test_frame,train_frame,time,feature_cols)
        


   
CrossVal()




    