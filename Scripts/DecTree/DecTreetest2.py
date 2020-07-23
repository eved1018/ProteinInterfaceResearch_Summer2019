 #!/usr/bin/env python
# imports
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
import math 
from sklearn.datasets import *
from sklearn import tree
from dtreeviz.trees import *


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
    
    y_predict = model.predict(X_bench)
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

# Ranfor()

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
def logregroc(threshhold,frame,proteinids):
    proteinname = frame.index 
    log_all_res_sum = 0 # total res 
    log_N_sum = 0 # total annotated 
    log_pred_sum = 0 #total over threshold 
    log_TP_Total_sum = 0 #sum of TP
    log_FP_Total_sum = 0 #sum of FP
    log_Neg_Total_sum = 0 #sum of neg 
    for protein in proteinids:
        # col_names = [ 'residue','predus', 'ispred', 'dockpred', 'annotated','rfscore','logreg']
        # counterframe = pd.DataFrame(columns = col_names)
        rows = []
        for protein_res in proteinname: 
            if protein in protein_res:
                row = frame.loc[protein_res]
                rows.append(row)
        
        counterframe = pd.DataFrame(rows,columns = ['predus','ispred','dockpred','annotated', 'rfscore','logreg'])
        # print(counterframe.head())
        cols = ['residue', 'logreg']
        counterframerf = pd.DataFrame(columns = cols)
        counterframerf = counterframe[['logreg']] 
        seq_res = counterframerf.index.values.tolist()
        seqnum = len(seq_res)
        pred_score= counterframerf.logreg
        predictedframesort = counterframerf.sort_values(by=['logreg'], inplace =False, ascending=False)
        
        thresholdframe= predictedframesort[predictedframesort.logreg >= threshhold] 
        # print(thresholdframe.head())
        
        predicted_res = thresholdframe.index.values.tolist()
        predicted_res = [str(i) for i in predicted_res]
        pred_res = []
        for i in predicted_res: 
            res_prot = i.split("_")
            res = res_prot[0]
            pred_res.append(res)
        

        # annotatedfile = "/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Annotated_Residues/AnnotatedTotal/{}_Interface_Residues".format(protein)
        annotatedfile = "/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Antogen/InterfaceResidues/{}_sorted".format(protein)

        N = 0
        annotated_res =[]
        with open(annotatedfile) as AnnFile:
            for line in AnnFile:
                line = line.strip("\n")
                N +=1
                line = line.split("_")
                line = line[0]
                annotated_res.append(line)
        Truepos = []
        for res in annotated_res:
            if res in pred_res:
                Truepos.append(res)
        pred = len(pred_res)
        TP = len(Truepos)
        TPR = TP/N 
        FP = pred - TP
        neg = seqnum - N
        FPR = FP/neg
        # print("protein {}".format(protein))
        # print("threshold {}".format(threshhold))
        # print("pred: {}".format(pred))
        # print("annotated: {}".format(N))
        # print("True pos: {}".format(TP))
        # print("TPR: {}".format(TPR))
        # print("FPR: {}".format(FPR))
        log_TP_Total_sum += TP
        log_FP_Total_sum += FP
        log_all_res_sum += seqnum # total res 
        log_N_sum  += N # total annotated 
        log_pred_sum += pred #total over threshold 
        log_Neg_Total_sum += neg
    return log_TP_Total_sum, log_FP_Total_sum ,log_all_res_sum, log_N_sum ,log_pred_sum , log_Neg_Total_sum


def ROC_single(frame,proteinids):
    # print(proteinids)
    TPRS = []
    FPRS = []
    threshholds= []
    log_threshholds = []
    log_TPRS = []
    log_FPRS = []
    log_threshholds =[]
    for i in np.arange(0.00, 1.02, .01):
        threshhold = float(str(round(i,2)))   
        proteinname = frame.index 
        all_res_sum = 0 # total res 
        N_sum = 0 # total annotated 
        pred_sum = 0 #total over threshold 
        TP_Total_sum = 0 #sum of TP
        FP_Total_sum = 0 #sum of FP
        Neg_Total_sum = 0 #sum of neg 
        log_TP_Total_sum, log_FP_Total_sum ,log_all_res_sum, log_N_sum ,log_pred_sum , log_Neg_Total_sum = logregroc(threshhold,frame,proteinids)
        for protein in proteinids:
            rows = []
            for protein_res in proteinname: 
                if protein in protein_res:
                    row = frame.loc[protein_res]
                    rows.append(row)
            counterframe = pd.DataFrame(rows,columns = ['predus','ispred','dockpred','annotated', 'rfscore','logreg'])
            cols = ['residue', 'rfscore']
            counterframerf = pd.DataFrame(columns = cols)
            # counterframerf = counterframe.index
            counterframerf = counterframe[['rfscore']] 
            seq_res = counterframerf.index.values.tolist()
            seqnum = len(seq_res)
            pred_score= counterframerf.rfscore
            predictedframesort = counterframerf.sort_values(by=['rfscore'], inplace =False, ascending=False)
            thresholdframe= predictedframesort[predictedframesort.rfscore >= threshhold] 
            predicted_res = thresholdframe.index.values.tolist()
            predicted_res = [str(i) for i in predicted_res]
            pred_res = []
            for i in predicted_res: 
                res_prot = i.split("_")
                res = res_prot[0]
                pred_res.append(res)
            
            # annotatedfile = "/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Annotated_Residues/AnnotatedTotal/{}_Interface_Residues".format(protein)
            annotatedfile = "/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Antogen/InterfaceResidues/{}_sorted".format(protein)
            N = 0
            annotated_res =[]
            with open(annotatedfile) as AnnFile:
                for line in AnnFile:
                    line = line.strip("\n")
                    N +=1
                    line = line.split("_")
                    line = line[0]
                    annotated_res.append(line)
            Truepos = []
            for res in annotated_res:
                if res in pred_res:
                    Truepos.append(res)
            pred = len(pred_res)
            TP = len(Truepos)
            TPR = TP/N 
            FP = pred - TP
            neg = seqnum - N
            FPR = FP/neg
            # print("protein {}".format(protein))
            # print("threshold {}".format(threshhold))
            # print("pred: {}".format(pred))
            # print("annotated: {}".format(N))
            # print("True pos: {}".format(TP))
            # print("TPR: {}".format(TPR))
            # print("FPR: {}".format(FPR))
            TP_Total_sum += TP
            FP_Total_sum += FP
            all_res_sum += seqnum # total res 
            N_sum  += N # total annotated 
            pred_sum += pred #total over threshold 
            Neg_Total_sum += neg
        Global_TPR = TP_Total_sum / N_sum
        TPRS.append(Global_TPR)
        Global_FPR = FP_Total_sum / Neg_Total_sum
        FPRS.append(Global_FPR)
        threshholds.append(threshhold)
        log_Global_TPR = log_TP_Total_sum / log_N_sum
        log_TPRS.append(log_Global_TPR)
        log_Global_FPR = log_FP_Total_sum / log_Neg_Total_sum
        log_FPRS.append(log_Global_FPR)
        log_threshholds.append(threshhold)
    final_results = pd.DataFrame(
    {'threshold': threshholds,
     'TPR': TPRS,
     'FPR': FPRS
    })

    distance = final_results["FPR"].diff()
    midpoint  = final_results["TPR"].rolling(2).sum()
    distance = distance * -1
    AUC = (distance) * (midpoint)
    AUC = AUC/2
    sum_AUC = AUC.sum()
        
    log_final_results = pd.DataFrame(
    {'threshold': log_threshholds,
     'TPR': log_TPRS,
     'FPR': log_FPRS
    })

    distance = log_final_results["FPR"].diff()
    midpoint  = log_final_results["TPR"].rolling(2).sum()
    distance = distance * -1
    log_AUC = (distance) * (midpoint)
    log_AUC = log_AUC/2
    log_sum_AUC = log_AUC.sum()
    

    return sum_AUC , log_sum_AUC


def ROC_Star(data):
    timer = 1 
    code = 1 
    print("star set up")
    # print(data.head())
    data = data.round({'predus': 3, 'ispred': 3, 'dockpred': 3, 'logreg': 3,"rfscore":3})
    Star_interface = data[data.annotated == 1] 
    Star_non_interface = data[data.annotated == 0]
    Star_interface = Star_interface.drop(columns="annotated")
    Star_non_interface = Star_non_interface.drop(columns="annotated")
    Star_interface = Star_interface.rename(columns={'predus':"T1", 'ispred': "T2", 'dockpred':"T3", 'logreg':"T4",'rfscore': 'T5'})
    Star_non_interface =Star_non_interface.rename(columns={'predus':"T1", 'ispred': "T2", 'dockpred':"T3", 'rfscore':"T4",'logreg': 'T5'})
    os.mkdir("/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/CrossVal_logreg_RF/Crossvaltest{}".format(code))
    os.mkdir("/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/CrossVal_logreg_RF/Crossvaltest{}/Star".format(code))
    os.mkdir("/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/CrossVal_logreg_RF/Crossvaltest{}/Star/CV{}".format(code,timer))

    path = "/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/CrossVal_logreg_RF/Crossvaltest{}/Star/CV{}/StarinterfaceCV{}.txt".format(code,timer,timer)
    Star_interface.to_csv(path,sep="\t", index=False, header=True)
    path = "/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/CrossVal_logreg_RF/Crossvaltest{}/Star/CV{}/StarnoninterfaceCV{}.txt".format(code,timer,timer)
    Star_non_interface.to_csv(path,sep="\t", index=False, header=True)

def Main():
    AUCS_CVS = []
    log_AUCS_CVS = []
    AUCs = []
    log_AUCs = []
    global_AUC= 0
    log_global_AUC = 0
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
    # print(proteinname)
    # Features, ie prediction scores from predus, ispred and dockpred 
    X = data[feature_cols] 
     # Target variable, noninterface or interface 
    y = data.annotated
    # testing antigens 

    df_ant = pd.read_csv("/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Antogen/predictionvalue/res_pred/test.csv", header=0)
    proteinname_ant = df_ant.residue
    X_ant = df_ant[feature_cols]
    y_ant = df_ant.annotated
    proteinids = []
    for resprot in proteinname_ant: 
        res_prot = resprot.split("_")
        proteinid = res_prot[1]
        if proteinid not in proteinids:
             proteinids.append(res_prot[1])
    x_ant = sm.add_constant(X_ant)
    logit_model=sm.Logit(y_ant,x_ant)
    result=logit_model.fit()
    coefficients = result.params
    # prediction score calc. 
    protein= df_ant.residue
    predusval = df_ant.predus
    ispredval = df_ant.ispred
    dockpred = df_ant.dockpred
    predcoef = coefficients[1]
    ispredcoef = coefficients[2]
    dockpredcoef= coefficients[3]
    val = (coefficients[0] + predcoef * predusval + ispredval* ispredcoef+dockpred * dockpredcoef)*(-1)
    exponent = np.exp(val)
    pval = (1/(1+exponent))
    # save prediction scores and training set to same folder as coefs 
    # results = pd.DataFrame({"residue": protein, "prediction value": pval})
    # print(coefficients)
    model = RandomForestClassifier(n_estimators = 100, max_depth =10, ccp_alpha = 0.0000400902332 , random_state = 0)
    model.fit(X, y)
    y_prob = model.predict_proba(X_ant)
    y_prob_intr = [p[1] for p in y_prob]
    df_ant = df_ant.assign(logreg = pval)
    df2 = df_ant.assign(rfscore = y_prob_intr )
    print(df2.head())
    df2.set_index('residue', inplace= True )

    sum_AUC,log_sum_AUC = ROC_single(df2,proteinids)
    ROC_Star(df2)
    # print (sum_AUC,log_sum_AUC)

   
    

Main()

