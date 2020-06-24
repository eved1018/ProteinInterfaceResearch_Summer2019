
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

# Logistic regresion function
# params:
#     test_frame is the pandas dataframe that the regresion predicts interface scores for 
#     train_frame is the andas dataframe that the regresion fits to 
#     time is an iterirator used to keep track of each implementation of the regresion 
#     cols is the feature columns of the dataframe, ie what each column is data for 
# returns
#     three files:
#         1) the coeeficants for the regresion fitting 
#         2) the predction scores for the test_frame 
#         3) the dataframe used to train the regresion

def LogReg(test_frame, train_frame,time,cols):
        # set columns 
        feature_cols = cols
        # split traing data into the depednent and indepdent variables 
        # X includes the predus, ispred and dockpred score 
        # y is a binary classifier, 0 is non interface 1 is interface 
        X = train_frame[feature_cols]
        y = train_frame.annotated
        # fit the logistic regresion ot the training data and save the results and coef as variables 
        x = sm.add_constant(X)
        logit_model=sm.Logit(y,x)
        result=logit_model.fit()
        coefficients = result.params
        # create folder for output data and save the coef in it 
        folder = "/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/CrossVal/CV{}" .format(time)
        os.mkdir(folder)
        file1 = open("/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/CrossVal/CV{}/cvcoef{}.txt" .format(time,time), "w")
        print(coefficients, file=file1 )
        file1.close()
        # prediction score calc. 
        protein= test_frame.index
        predusval = test_frame.predus
        ispredval = test_frame.ispred
        dockpred = test_frame.dockpred
        predcoef = coefficients[1]
        ispredcoef = coefficients[2]
        dockpredcoef= coefficients[3]
        val = (coefficients[0] + predcoef * predusval + ispredval* ispredcoef+dockpred * dockpredcoef)*(-1)
        exponent = np.exp(val)
        pval = (1/(1+exponent))
        # save prediction scores and training set to same folder as coefs 
        results = pd.DataFrame({"residue": protein, "prediction value": pval})
        path="/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/CrossVal/CV{}/predval{}.csv".format(time,time)
        results.to_csv(path,sep=",", index=False, header=True)
        pathtest="/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/CrossVal/CV{}/testframe{}.csv".format(time,time)
        train_frame.to_csv(pathtest,sep=",", index=True, header=True)


# Random Forest function 
# params:
#   test_frame is the pandas dataframe that the regresion predicts interface scores for 
#     train_frame is the andas dataframe that the regresion fits to 
#     time is an iterirator used to keep track of each implementation of the regresion 
#     cols is the feature columns of the dataframe, ie what each column is data for 
# returns:
#     a file with the residue and prediction score of the test set, to the same folder as the logistic regresion data
    
def RandomFor(test_frame, train_frame,time,cols): 
        # set columns 
        feature_cols = cols
        # split traing and test data into the depednent and indepdent variables 
        # X includes the predus, ispred and dockpred score 
        # y is a binary classifier, 0 is non interface 1 is interface 
        X = train_frame[feature_cols]
        y = train_frame.annotated
        X_test = test_frame[feature_cols]
        y_test = test_frame.annotated
        protein = test_frame.index 
        # create the random forest model
        # n_estimators is the number of trees in each forest
        # random_state is a intiger that keeps the randomness in the RF teh same over multiple iterations
        # bootstrap, when false, means all the data in teh training set is used to produce each tree 
        model = RandomForestClassifier(n_estimators = 10, random_state = 0, bootstrap=False)
        model.fit(X, y)
        # save probability score for test set as a list with indeces [noninterface, interface]
        y_prob = model.predict_proba(X_test)
        # create a new variable with only the inetrface prediction for each residue 
        y_prob_interface = [p[1] for p in y_prob]
        # optional, set a decimal place cutoff, d, for the probability score 
        # d = 4
        # y_prob_intr_dec = [round(prob, d) for prob in y_prob_interface]
        # save the residue and probabilty score of the test set to the same folder as the logistic regresion 
        results= pd.DataFrame({"residue": protein, "prediction score": y_prob_interface})
        path="/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/CrossVal/CV{}/RFval{}.csv".format(time,time)
        results.to_csv(path,sep=",", index=False, header=True)
        
        


# Cross validation function: 
# splits up the data into ten test sets with corresponding traingin set, whcih includes all the data except the test set. 
# then sends each test/train pair into the logistic regresion and random forest functions. 


def CrossVal():
    # set up DataFrame 
    aucframe= pd.DataFrame({})
    col_names = ['residue', 'predus', 'ispred', 'dockpred', 'annotated']
    # load dataset which is a csv file containing all the residues in Nox and Benchmark as well as predus, ispred, and dockpred scores. 
    # The last column is a binary annotated classifier, 0 is noninetrface 1 is interface. 
    df = pd.read_csv("/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/final_sort.csv", header=None, names=col_names)
    # set the residue_protein ID as the index of the DataFrame 
    df.set_index('residue', inplace= True )
    # remove any null or missing data from the dataset
    df.isnull().any()
    data = df.fillna(method='ffill')
    # set X as the three prediction scores and y as the true annotated value 
    feature_cols = ['predus','ispred','dockpred']
    proteinname = data.index
    # Features, ie prediction scores from predus, ispred and dockpred 
    X = data[feature_cols] 
     # Target variable, noninterface or interface 
    y = data.annotated
    # create list contaning only the protein ID's without the residue number
    proteinids = []
    for resprot in proteinname: 
        res_prot = resprot.split("_")
        proteinid = res_prot[1]
        if proteinid not in proteinids:
             proteinids.append(res_prot[1])
    # create sublist of sets conating 22 proteins in each set or "chunk"
    # n controls the number of proteins in each set
    lst = proteinids
    n = 22
    chunks = [lst[i:i + n] for i in range(0, len(lst), n)]
    # checks to make sure the last set contains n number of proteins in it, if not it will give one of its proteins to each previous set.
    # that is if teh last chunk contains 3 proteins, the last three chunks will conatin 23 instead of 22 proteins in them. 
    for i in range(0,len(chunks[-1])):
        if len(chunks[-1]) != n:
            pdbs = chunks[-1]
            itt = -(i+2)
            firstlist = []
            firstlist.append(pdbs[0])
            chunks[itt].extend(firstlist)
            chunks[-1].remove(pdbs[0])
    # the last set is now empty so it is removed. 
    del chunks[-1]
    # set teh column names for the new trainng and test sets, same as feature_cols but residue si removed bc it is already the index. 
    col_namestest = ['predus', 'ispred', 'dockpred', 'annotated']
    # each subset(or chunk) of proteins is used to create a training set containing the residues for the proteins in the subset as a test set with all other residues
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
        # set variabel for iteration, to keep track of each test set, since i in range(0,k) includes zero, i is incresased by 1 for readabilty
        time = i+1
        # perfroms logistic regresion and random forest for each test and training set.
        # LogReg(test_frame,train_frame,time,feature_cols)
        RandomFor(test_frame,train_frame,time,feature_cols)
        


   
# CrossVal()

def NoxRF():
    # folder = "/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/CrossVal/CVNOXBenchtest"
    # os.mkdir(folder)
    col_names = ['residue', 'predus', 'ispred', 'dockpred', 'annotated']
    # load dataset
    df = pd.read_csv("/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/noxdata.csv", header=None, names=col_names)
    #remove null data 
    df.isnull().any()
    data = df.fillna(method='ffill')
    # define dependent var columns 
    feature_cols = ['predus','ispred','dockpred']
    protein = data.residue
    X = data[feature_cols] # Features
    y = data.annotated # Target variable

    # load benchmark data as test set 
    benchmarkna= pd.read_csv('/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/benchmarkdata.csv', header=None, names=col_names)
    benchmarkna.isnull().any()
    benchmark = benchmarkna.fillna(method='ffill')
    X_bench= benchmark[feature_cols]
    y_bench= benchmark.annotated 
    protienname_bench= benchmark.residue

    # implement random forets 
    model = RandomForestClassifier(n_estimators = 10, random_state = 0, bootstrap=False)
    model.fit(X, y)
    
    # y_predict = model.predict(X_bench)
    y_prob = model.predict_proba(X_bench)
    # create a new variable with only the inetrface prediction for each residue 
    y_prob_interface = [p[1] for p in y_prob]
    # optional, set a decimal place cutoff, d, for the probability score 
    # d = 4
    # y_prob_intr_dec = [round(prob, d) for prob in y_prob_interface]
    # save the residue and probabilty score of the test set to the same folder as the logistic regresion 
    results= pd.DataFrame({"residue": protienname_bench, "prediction score": y_prob_interface})
    path="/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/CrossVal/CVNOXBenchtest/RFvalBench.csv"
    results.to_csv(path,sep=",", index=False, header=True)

def BenchRF():
    col_names = ['residue', 'predus', 'ispred', 'dockpred', 'annotated']
    # load dataset
    df = pd.read_csv("/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/benchmarkdata.csv", header=None, names=col_names)
    df.isnull().any()
    data = df.fillna(method='ffill')
    feature_cols = ['predus','ispred','dockpred']
    protein = data.residue
    X = data[feature_cols] # Features
    y = data.annotated # Target variable
    nox= pd.read_csv('/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/noxdata.csv', header=None, names=col_names)
    nox.isnull().any()
    nox = nox.fillna(method='ffill')
    X_nox= nox[feature_cols]
    y_nox= nox.annotated 
    protienname_nox= nox.residue
     # implement random forets 
    model = RandomForestClassifier(n_estimators = 10, random_state = 0, bootstrap=False)
    model.fit(X, y)
    # y_predict = model.predict(X_bench)
    y_prob = model.predict_proba(X_nox)
    # create a new variable with only the inetrface prediction for each residue 
    y_prob_interface = [p[1] for p in y_prob]
    # optional, set a decimal place cutoff, d, for the probability score 
    # d = 4
    # y_prob_intr_dec = [round(prob, d) for prob in y_prob_interface]
    # save the residue and probabilty score of the test set to the same folder as the logistic regresion 
    results= pd.DataFrame({"residue":  protienname_nox, "prediction score": y_prob_interface})
    path="/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/CrossVal/CVNOXBenchtest/RFvalNox.csv"
    results.to_csv(path,sep=",", index=False, header=True)

NoxRF()
BenchRF()

git test hello 






    