 #!/usr/bin/env python
# imports
import pandas as pd
import numpy as np
import statsmodels.api as sm
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.tree import export_graphviz
import pydot 

# set table of data

aucframe= pd.DataFrame({})

#  

def DecTree():
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
    # from sklearn.model_selection import train_test_split 
    # X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)
    benchmarkna= pd.read_csv('/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/benchmarkdata.csv', header=None, names=col_names)
    benchmarkna.isnull().any()
    benchmark = benchmarkna.fillna(method='ffill')
    X_bench= benchmark[feature_cols]
    y_bench= benchmark.annotated 
    protienname_bench= benchmark.residue
    from sklearn import tree
    model = tree.DecisionTreeClassifier()
    model.fit(X, y)
    y_predict = model.predict(X_bench)
    from sklearn.metrics import accuracy_score
    print(accuracy_score(y_bench, y_predict))
    # print(protienname_bench, y_bench, y_predict)
    results = pd.DataFrame({"residue": protienname_bench, "exp value":y_bench, "prediction value": y_predict})
    print(results)
    from sklearn.metrics import confusion_matrix
    print(pd.DataFrame(confusion_matrix(y_bench, y_predict)))



# DecTree()
def Ranfor():
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
    model = RandomForestClassifier(n_estimators = 1000, random_state = 42)
    model.fit(X, y)
    y_predict = model.predict(X_bench)
    # accuracy metric 
    print(accuracy_score(y_bench, y_predict))
    # Classification metric
    print(classification_report(y_bench,y_predict))
    # visualize results 
    results = pd.DataFrame({"residue": protienname_bench, "exp value":y_bench, "prediction value": y_predict})
    print(results)
    # confusion matrix 
    # print(pd.DataFrame(confusion_matrix(y_bench, y_predict)))
    # # # Get numerical feature importances
    # importances = list(model.feature_importances_)# List of tuples with variable and importance
    # feature_importances = [(feature, round(importance, 2)) for feature, importance in zip(feature_cols, importances)]# Sort the feature importances by most important first
    # feature_importances = sorted(feature_importances, key = lambda x: x[1], reverse = True)# Print out the feature and importances 
    # [print('Variable: {:20} Importance: {}'.format(*pair)) for pair in feature_importances];
    # # tree viz 
    # tree = model.estimators_[5]
    # export_graphviz(tree, out_file = '/Users/evanedelstein/Desktop/tree.dot', feature_names = feature_cols, rounded = True, precision = 1)
    # (graph, ) = pydot.graph_from_dot_file('/Users/evanedelstein/Desktop/tree.dot')
    # graph.write_png('/Users/evanedelstein/Desktop/tree.png')
    # # small tree viz 
    # model_small = RandomForestClassifier(n_estimators=10, max_depth = 3)
    # model_small.fit(X, y)
    # tree_small = model_small.estimators_[5]
    # export_graphviz(tree_small, out_file = '/Users/evanedelstein/Desktop/small_tree.dot', feature_names = feature_cols, rounded = True, precision = 1)
    # (graph, ) = pydot.graph_from_dot_file('/Users/evanedelstein/Desktop/small_tree.dot')
    # graph.write_png('/Users/evanedelstein/Desktop/small_tree.png');
    



Ranfor()

    