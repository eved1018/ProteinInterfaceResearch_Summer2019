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
    # use benchmark as test 
    benchmarkna= pd.read_csv('/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/benchmarkdata.csv', header=None, names=col_names)
    benchmarkna.isnull().any()
    benchmark = benchmarkna.fillna(method='ffill')
    X_bench= benchmark[feature_cols]
    y_bench= benchmark.annotated 
    protienname_bench= benchmark.residue
    # implemmet DT
    model = tree.DecisionTreeClassifier(ccp_alpha=0.00105)
    model.fit(X, y)
    y_predict = model.predict(X_bench)
    class_name= ['Non-interface', 'interface']
    plot_tree(model, feature_names= feature_cols, filled = True)
    plt.show()
    # Accurecy 
    # print(accuracy_score(y_bench, y_predict))
    # print(protienname_bench, y_bench, y_predict)
    # results = pd.DataFrame({"residue": protienname_bench, "exp value":y_bench, "prediction value": y_predict})
    # print(results)
    # from sklearn.metrics import confusion_matrix
    # print(pd.DataFrame(confusion_matrix(y_bench, y_predict)))
     # tree viz 
    # dot_data = tree.export_graphviz(model, out_file=None) 
    # graph = graphviz.Source(dot_data) 
    # graph.render("DTtree")    


            



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
    model = RandomForestClassifier(n_estimators = 10, random_state = 42)
    model.fit(X, y)
    
    # y_predict = model.predict(X_bench)
    y_prob = model.predict_proba(X_bench)
        # create a new variable with only the inetrface prediction for each residue 
        y_prob_interface = [p[1] for p in y_prob]
        # optional, set a decimal place cutoff, d, for the probability score 
        # d = 4
        # y_prob_intr_dec = [round(prob, d) for prob in y_prob_interface]
        # save the residue and probabilty score of the test set to the same folder as the logistic regresion 
        results= pd.DataFrame({"residue": protein, "prediction score": y_prob_interface})
        path="/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/CrossVal/CVNOXBenchtest/RFvalBench.csv".format(time,time)
        results.to_csv(path,sep=",", index=False, header=True)
    # y_prob = model.predict_proba(X_bench)
    # y_prob_intr = [p[1] for p in y_prob]
    # y_prob_intr_dec = [round(prob, 3) for prob in y_prob_intr[:50]]
    # print(y_predict[:50])
    # print(y_prob_intr_dec)

    # counter = 0 
    # for i in y_predict:
    #     if i == 1:
    #         counter += 1 
    # print(counter)
    # y_prob = model.predict_proba(X_bench)
    # y_prob_intr = [p[1] for p in y_prob]
    # print(y_prob_intr[:5])
    # print( roc_auc_score(y_bench, y_prob) )
   

    # accuracy metric 
    print(accuracy_score(y_bench, y_predict))
    # # Classification metric
    # print(classification_report(y_bench,y_predict))
    # visualize results 
    # results = pd.DataFrame({"residue": protienname_bench, "exp value":y_bench, "prediction value": y_predict})
    # print(results)
    # confusion matrix 
    # print(pd.DataFrame(confusion_matrix(y_bench, y_predict)))
    # # # Get numerical feature importances
    # importances = list(model.feature_importances_)# List of tuples with variable and importance
    # feature_importances = [(feature, round(importance, 2)) for feature, importance in zip(feature_cols, importances)]# Sort the feature importances by most important first
    # feature_importances = sorted(feature_importances, key = lambda x: x[1], reverse = True)# Print out the feature and importances 
    # [print('Variable: {:20} Importance: {}'.format(*pair)) for pair in feature_importances];
    # tree viz  
    # for i in range(1,3):
    #     tree = model.estimators_[i]
    #     outfilename= "/Users/evanedelstein/Desktop/Rftree{}.dot".format(i)
    #     export_graphviz(tree, out_file = outfilename, feature_names = feature_cols, rounded = True, precision = 1)
    #     (graph, ) = pydot.graph_from_dot_file(outfilename)
    #     graph.write_png('/Users/evanedelstein/Desktop/RFtree{}.png'.format(i))
    # small tree viz 
    # model_small = RandomForestClassifier(n_estimators=10, max_depth = 3)
    # model_small.fit(X, y)
    # tree_small = model_small.estimators_[5]
    # export_graphviz(tree_small, out_file = '/Users/evanedelstein/Desktop/small_tree.dot', feature_names = feature_cols, rounded = True, precision = 1)
    # (graph, ) = pydot.graph_from_dot_file('/Users/evanedelstein/Desktop/small_tree.dot')
    # graph.write_png('/Users/evanedelstein/Desktop/small_tree.png');




    # Number of trees in random forest
    n_estimators = [int(x) for x in np.linspace(start = 200, stop = 2000, num = 10)]
    # Number of features to consider at every split
    max_features = ['auto', 'sqrt']
    # Maximum number of levels in tree
    max_depth = [int(x) for x in np.linspace(10, 110, num = 11)]
    max_depth.append(None)
    # Minimum number of samples required to split a node
    min_samples_split = [2, 5, 10]
    # Minimum number of samples required at each leaf node
    min_samples_leaf = [1, 2, 4]
    # Method of selecting samples for training each tree
    bootstrap = [True, False]
    # train on dif alpha val
    ccp_alpha= [0,0.005,0.1, 0.015,0.02, 0.025, 0.03, 0.035]
    # Create the random grid
    random_grid = {'n_estimators': n_estimators,
                'max_features': max_features,
                'max_depth': max_depth,
                'min_samples_split': min_samples_split,
                'min_samples_leaf': min_samples_leaf,
                'bootstrap': bootstrap,
                }
    rf = RandomForestClassifier()
    # Random search of parameters, using 3 fold cross validation, 
    # search across 100 different combinations, and use all available cores
    rf_random = RandomizedSearchCV(estimator = rf, param_distributions = random_grid, n_iter = 100, cv = 3, verbose=2, random_state=42, n_jobs = -1)
    # Fit the random search model
    rf_random.fit(X,y)
    print(rf_random.best_params_)
    y_predict = rf_random.best_estimator_.predict(X_bench)
    print(accuracy_score(y_bench, y_predict))

Ranfor()

def Alphatest():
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
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1)
    model = DecisionTreeClassifier(random_state=1).fit(X_train,y_train)
    y_predicted = model.predict(X_test)
    print('Training accuracy: ',model.score(X_train,y_train))
    print('Test Accuracy: ',model.score(X_test,y_test)) 
    path = model.cost_complexity_pruning_path(X_train,y_train)
    ccp_alphas, impurities = path.ccp_alphas, path.impurities
    # fig, ax = plt.subplots()
    # ax.plot(ccp_alphas[:-1], impurities[:-1], marker='o', drawstyle="steps-post")
    # ax.set_xlabel("effective alpha")
    # ax.set_ylabel("total impurity of leaves")
    # ax.set_title("Total Impurity vs effective alpha for training set")
    # # plt.show()
    clfs = []
    for ccp_alpha in ccp_alphas:
        model = DecisionTreeClassifier(random_state=0, ccp_alpha=ccp_alpha)
        model.fit(X_train,y_train)
        clfs.append(model)
    print("Number of nodes in the last tree is: {} with ccp_alpha: {}".format( clfs[-1].tree_.node_count, ccp_alphas[-1]))
    clfs = clfs[:-1]
    ccp_alphas = ccp_alphas[:-1]
    node_counts = [clf.tree_.node_count for clf in clfs]
    depth = [clf.tree_.max_depth for clf in clfs]
    train_scores = [clf.score(X_train,y_train) for clf in clfs]
    test_scores = [clf.score(X_test,y_test) for clf in clfs]
    fig, ax = plt.subplots()
    ax.set_xlabel("alpha")
    ax.set_ylabel("accuracy")
    ax.set_title("Accuracy vs alpha for training and testing sets")
    ax.plot(ccp_alphas, train_scores, marker='o', label="train",
    drawstyle="steps-post")
    ax.plot(ccp_alphas, test_scores, marker='o', label="test",
    drawstyle="steps-post")
    ax.legend()
    # plt.show()
    index_best_model = np.argmax(test_scores)
    best_model = clfs[index_best_model]
    print('Training accuracy of best model: ',best_model.score(X_train, y_train))
    print('Test accuracy of best model: ',best_model.score(X_test, y_test))
    print(best_model.get_params())
    dot_data = tree.export_graphviz(model, out_file=None) 
    graph = graphviz.Source(dot_data) 
    graph.render("DTtesttree") 
    benchmarkna= pd.read_csv('/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/benchmarkdata.csv', header=None, names=col_names)
    benchmarkna.isnull().any()
    benchmark = benchmarkna.fillna(method='ffill')
    X_bench= benchmark[feature_cols]
    y_bench= benchmark.annotated 
    protienname_bench= benchmark.residue
    y_predict_best= best_model.predict(X_bench)
    print(accuracy_score(y_bench, y_predict_best)) 
    model2 = tree.DecisionTreeClassifier(ccp_alpha=0.0010540940654176906)
    model2.fit(X, y)
    y_predict = model2.predict(X_bench)
    # Accurecy 
    print(accuracy_score(y_bench, y_predict))


# Alphatest()


    