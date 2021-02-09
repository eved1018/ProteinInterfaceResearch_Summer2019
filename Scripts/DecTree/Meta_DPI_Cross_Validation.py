# most of these arent used one day ill go through them 
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
import re 
import time 
import concurrent.futures
import multiprocessing
import subprocess
import re
import streamlit as st
import imgkit
import matplotlib.pyplot as plt

# main function, set all parameters here!
# code is just used to keep track of multiple runs
# trees, depthy, ccp are RF parametres
# size is the number of priteins in each bin (automaticly set to 1 for antigens)
# viz enables the tree vizualation 
# Antigen uses the antigen annotated as refrence
# set all paths 

def main():
    start = time.perf_counter()
    code = 1
    # add error message
    trees = 100
    depth  = 10 
    ccp = 0.0000400902332
    # for 5 fold use 44 for 10 use 22  
    size = 22
    viz = False 
    Antigen = True  
    # set col names
    col_names = ['residue', 'predus', 'ispred', 'dockpred', 'annotated']
    # which columns to look at (ie which dependent variables to use)
    # var_col_names =['predus', 'ispred', 'dockpred']
    var_col_names = ['predus',"ispred"]
    # change to where u need it to to go 
    results_path = "/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/CrossVal_logreg_RF/"
    # path to star, get it here http://melolab.org/star/download.php
    Star_path= "/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Scripts/star-v.1.0/"

    if Antigen is True:
        size = 1 
        data_path = "/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Antogen/predictionvalue/res_pred/test.csv"
        annotated_path = "/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Antogen/InterfaceResidues/"
    else:
        # change based on where the files are the first should be the final_sort.csv and second should be teh annoatted 
        data_path = "/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/final_sort.csv"
        annotated_path = "/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Annotated_Residues/AnnotatedTotal/"

    folder = "{}Crossvaltest{}" .format(results_path,code)
    while os.path.isdir(folder) is True:
        code = code + 1 
        folder = "{}Crossvaltest{}" .format(results_path,code)


    CrossVal(viz, code, trees, depth, ccp,size, start,results_path,data_path,Antigen,annotated_path,col_names,var_col_names )
    try:
        Star(results_path,code,Star_path)
    except:
        print("Star not working")
    finish = time.perf_counter()
    print(f"finished in {round((finish - start)/60,2 )} minutes(s)")

# core of the program, creates the chunks of proteins and runs programs in parrelel
# then unpacks data and computes AUC and ROC image

def CrossVal(viz, code, trees, depth, ccp,size, start,results_path,data_path, Antigen, annotated_path,col_names,var_col_names):
    # params to adjust RF
    Master= {}

    folder = "{}Crossvaltest{}" .format(results_path,code)
    os.mkdir(folder)
    folder = "{}/Crossvaltest{}/tests" .format(results_path,code)
    os.mkdir(folder)
    os.mkdir("{}Crossvaltest{}/Star".format(results_path,code))
    os.mkdir( "{}Crossvaltest{}/Trees".format(results_path,code))
    # set up DataFrame 
    aucframe= pd.DataFrame({})
    # col_names = ['residue', 'predus', 'ispred', 'dockpred', 'annotated']
    # load dataset which is a csv file containing all the residues in Nox and Benchmark as well as predus, ispred, and dockpred scores. 
    # The last column is a binary annotated classifier, 0 is noninetrface 1 is interface. 
    if Antigen is True: 
        df = pd.read_csv("{}".format(data_path), header=0)
    else:
        df = pd.read_csv("{}".format(data_path), header=None, names=col_names)
    # df = pd.read_csv("/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Antogen/predictionvalue/res_pred/test.csv", header=0)
    # set the residue_protein ID as the index of the DataFrame 
    df.set_index('residue', inplace= True )
    # remove any null or missing data from the dataset
    df.isnull().any()
    data = df.fillna(method='ffill')
    col_namestest = var_col_names + ["annotated"]
    data = data[col_namestest]
    # set X as the three prediction scores and y as the true annotated value 
    # feature_cols = ['predus','ispred','dockpred']
    # feature_cols = data.columns[0:-1]
    feature_cols = var_col_names
    proteinname = data.index
    # print(proteinname)
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
    n = size
    chunks = [lst[i:i + n] for i in range(0, len(lst), n)]
    # checks to make sure the last set contains n number of proteins in it, if not it will give one of its proteins to each previous set.
    # that is if teh last chunk contains 3 proteins, the last three chunks will conatin 23 instead of 22 proteins in them. 
    sets = 0 

    for i in range(0,len(chunks[-1])):
        if len(chunks[-1]) != n:
            pdbs = chunks[-1]
            itt = -(i+2)
            firstlist = []
            firstlist.append(pdbs[0])
            chunks[itt].extend(firstlist)
            chunks[-1].remove(pdbs[0])
    # the last set is now empty so it is removed. 
    if len(chunks[-1]) == 0:
        del chunks[-1]
    # set teh column names for the new trainng and test sets, same as feature_cols but residue si removed bc it is already the index. 
    # col_namestest = ['predus', 'ispred', 'dockpred', 'annotated']
    
    
    # each subset(or chunk) of proteins is used to create a training set containing the residues for the proteins in the subset as a test set with all other residues
    train_test_frames= []
    for i in range(0,len(chunks)):
        test_frame = pd.DataFrame(columns = col_namestest)
        train_frame = pd.DataFrame(columns = col_namestest)
        train_frame = data.copy()
        rows = []
        for pdbid in chunks[i]:
            for protein_res in proteinname: 
                if pdbid in protein_res:
                    rows.append(protein_res)
        test_frame = data[data.index.isin(rows)]
        print("test 1:", test_frame.columns.tolist())
        protein_in_cv = chunks[i]
        timer = i+1
        train_frame = train_frame.drop(test_frame.index)
        toappend = (train_frame,test_frame,timer,protein_in_cv)
        train_test_frames.append(toappend)
        # set variabel for iteration, to keep track of each test set, since i in range(0,k) includes zero, i is incresased by 1 for readabilty
        sets = timer
    param_list = []
    cpus = multiprocessing.cpu_count()
    print("starting parellel \n number of cpus {}".format(cpus))
    
    for t in train_test_frames:
        (train_frame, test_frame,timer,protein_in_cv) = t
        params = (test_frame,train_frame,timer,feature_cols,code,protein_in_cv,trees,depth,ccp,viz,results_path,data_path,Antigen,annotated_path)
        param_list.append(params)
    coefs = {}
    rfscore_ROC = []
    # print(param_list)
    dict_timer = 0
    with concurrent.futures.ProcessPoolExecutor() as executor:
        param_list = param_list
        results = executor.map( Run, param_list)
        for i in results:
            (results_dic,timer, treeparams,Dict2,coefficients , Dict4) = i 
            
            for key in Dict4:
                # print(key)
                TP_Total_sums = Dict4[key]["TP_Total_sum"]
                # locals()[key]["tps"].append(TP_Total_sums)
                

                Ns_Total_sums = Dict4[key]["N_sum"]
                # locals()[key]["ns"].append(Ns_Total_sums)

                FPS_Total_sums = Dict4[key]["FP_Total_sum"]
                # locals()[key]["fps"].append(FPS_Total_sums)

                Negs_Total_sums = Dict4[key]["Neg_Total_sum"]
                # locals()[key]["negs"].append(Negs_Total_sums)

                if key in Master:
                    # print("adding to  {}".format(key))

                    Master[key]["ns"].append(Ns_Total_sums)
                    Master[key]["tps"].append(TP_Total_sums)
                    Master[key]["negs"].append(Negs_Total_sums)
                    Master[key]["fps"].append(FPS_Total_sums)
                else:
                    # print("making dict for {}".format(key))
                    D = {
                    "name": key,
                    "TPRS" : [],
                    "FPRS" : [],
                    "tps" : [TP_Total_sums],
                    "fps":  [FPS_Total_sums],            
                    "negs": [Negs_Total_sums],
                     "ns" : [Ns_Total_sums], 
                    "AUC": []
                    }
                    Master[key] = D
    for key in Dict4:
        
        tps = Master[key]["tps"] 
        fps = Master[key]["fps"] 
        ns = Master[key]["ns"] 
        negs = Master[key]["negs"] 
        negs_2 = Master[key]["negs"]
        
        globaltps = []
        globalfps = []
        globalnegs = []
        globalns = []
        TPRS = []
        FPRS = []

        for i in zip(*tps):
            tpr = sum(i)
            globaltps.append(tpr)
        for i in zip(*ns):
            N = sum(i)
            globalns.append(N)
        for i in zip(*fps):
            N = sum(i)
            globalfps.append(N)
        for i in zip(*negs):
            N = sum(i)
            globalnegs.append(N)
        for i,j in zip(globaltps,globalns):
            TPR = i/j
            TPRS.append(TPR)
            # print(TPR)
        for i,j in zip(globalfps,globalnegs):
            FPR = i/j
            FPRS.append(FPR)
            # print(FPR)
        final_results = pd.DataFrame({
            'TPR': TPRS,
            'FPR': FPRS
            })
            # print(final_results.head())
        distance = final_results["FPR"].diff()
        midpoint  = final_results["TPR"].rolling(2).sum()
        distance = distance * -1
        AUC = (distance) * (midpoint)
        AUC = AUC/2
        sum_AUC = AUC.sum()
        print(key)
        print(sum_AUC)
        
        Master[key]["AUC"].append(sum_AUC)
        Master[key]["TPRS"].append(TPRS)
        Master[key]["FPRS"].append(FPRS)

    # ROC plot
    ROC_Plt(Master,code,results_path)

    # Tree vizualization 
    if viz == False :
        pass
    else:
        treeviz(treeparams,params,results_path) 

# Runs data programs, including logreg, RF and ROC 
def Run(params):

    (test_frame,train_frame,timer,feature_cols,code,protein_in_cv,trees,depth,ccp,viz,results_path,data_path,Antigen,annotated_path) =  params
    log_results , coefficients = LogReg(test_frame,train_frame,timer,feature_cols,code,results_path )
    totalframe, treeparams = RandomFor(test_frame,train_frame,timer,feature_cols,code,protein_in_cv,trees,depth,ccp,viz,results_path,data_path,Antigen,annotated_path,log_results)
    results_dic ,Dict2 , Dict4 = ROC_calc(totalframe,protein_in_cv,code,timer,results_path,data_path,Antigen,annotated_path)
    ROC_Star(totalframe,code,timer,results_path)

    # move roc and star here
    return results_dic, timer ,treeparams ,Dict2 ,coefficients ,Dict4


# Logistic regression
def LogReg(test_frame, train_frame,timer,cols,code,results_path):
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
        folder = "{}Crossvaltest{}/tests/CV{}" .format(results_path,code,timer)
        os.mkdir(folder)
        # file1 = open("{}Crossvaltest{}/tests/CV{}/cvcoef{}.txt" .format(results_path,code,timer,timer), "w")
        # print(coefficients, file=file1 )
        # file1.close()
        # prediction score calc. 
        protein= test_frame.index
        # predusval = test_frame.predus
        # ispredval = test_frame.ispred
        # dockpred = test_frame.dockpred
        # predcoef = coefficients[1]
        # ispredcoef = coefficients[2]
        # dockpredcoef= coefficients[3]
        vals = []
        num = 1
        for pred in cols:
            v1 = test_frame[pred]
            v2 = coefficients[num]
            num += 1
            v3 = v1 * v2
            vals.append(v3)

        sum_pred = sum(vals)
        val = -1 *(coefficients[0] + sum_pred)
        # val = (coefficients[0] + predcoef * predusval + ispredval* ispredcoef)*(-1)
        # val = (coefficients[0] + predcoef * predusval + ispredval* ispredcoef+dockpred * dockpredcoef)*(-1)

        exponent = np.exp(val)
        pval = (1/(1+exponent))
        # save prediction scores and training set to same folder as coefs 
        # results = pd.DataFrame({"residue": protein, "prediction value": pval})
        log_results = test_frame.assign(logreg = pval)
        # path="{}Crossvaltest{}/tests/CV{}/predval{}.csv".format(results_path,code,timer,timer)
        # results.to_csv(path,sep=",", index=True, header=True)
        # pathtest="/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/CrossVal_logreg_RF/Crossvaltest2/CV{}/trainframe{}.csv".format(timer,timer)
        # train_frame.to_csv(pathtest,sep=",", index=True, header=True)
        return log_results , coefficients

# Random Forest function 
# params:
#   test_frame is the pandas dataframe that the regresion predicts interface scores for 
#     train_frame is the andas dataframe that the regresion fits to 
#     timer is an iterirator used to keep track of each implementation of the regresion 
#     cols is the feature columns of the dataframe, ie what each column is data for 
#     code is the interer code to deisgnate the test run 
#      protein_in_cv is a list of all the proteins in the K-1 set 
#      trees is the number of trees in the forest 
#      depth is the number of layers in eahc tree 
#      ccp is a pruning parameter 
# returns:
#     a file with the residue and prediction score of the test set, to the same folder as the logistic regresion data
#     The results frame is redirected to the Star function 
#     The AUC results for each run is retruned to the CrossVal function to determine the standard of deviation and avarage. 
    
def RandomFor(test_frame, train_frame,timer,cols,code,protein_in_cv,trees,depth,ccp,viz,results_path,data_path,Antigen,annotated_path,log_results): 
        # set columns 
        print("test frame:", test_frame.columns.tolist())
        feature_cols = cols
        print("f cols:",feature_cols)
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
        model = RandomForestClassifier(n_estimators = trees, random_state = 0, bootstrap=False, max_depth=depth, ccp_alpha= ccp)
        model.fit(X, y)
        # save probability score for test set as a list with indeces [noninterface, interface]
        y_prob = model.predict_proba(X_test)
        # create a new variable with only the inetrface prediction for each residue 
        y_prob_interface = [p[1] for p in y_prob]
        # optional, set a decimal place cutoff, d, for the probability score 
        # d = 4
        # y_prob_intr_dec = [round(prob, d) for prob in y_prob_interface]
        # save the residue and probabilty score of the test set to the same folder as the logistic regresion 

        df2 = test_frame.assign(rfscore = y_prob_interface )
        
        
        if timer == 1 and viz is True:
            # for i in range(0,100):
            #     tree = model.estimators_[i]
            #     print(tree.get_depth())
            tree = model.estimators_[0]
        else:
            tree = False  
        treeparams = (X, y, tree)
        totalframe = df2.copy()
    
        logframe = log_results
        logs = logframe["logreg"]
        totalframe = totalframe.join(logs)
        path="{}Crossvaltest{}/tests/CV{}/vals{}.csv".format(results_path,code,timer,timer)
        totalframe.to_csv(path,sep=",", index=True, header=True)
        # results_dic ,Dict2 , Dict4 = ROC_calc(totalframe,protein_in_cv,code,timer,results_path,data_path,Antigen,annotated_path)
        # ROC_Star(totalframe,code,timer,results_path)
        return totalframe ,treeparams 


# ROC calculator 
def ROC_calc(frame,protein_in_cv,code,timer,results_path,data_path,Antigen,annotated_path):
    proteinname = frame.index 
    predictors = frame.columns.tolist()
    print("pred:", predictors)
    annotated_frame = frame[frame['annotated'] ==1]
    annotated_res_prot = annotated_frame.index.tolist()
    predictors.remove('annotated')
    ROC_total_dic = {}
    vals = [ 0 , 0 ,0,0,0,0,0]
    ROC_dic = {key: vals for key in predictors}  
    Rates_dic = {}
    Dict = {}
    Dict2 = {}
    Dict3 = {}
    Dict4 = {}
    
    for i in predictors:
        Dict[i] = {}
        Dict2[i] = {}
        Dict3[i] = {}
        Dict4[i] = {}
    for i in predictors: 
        Dict2[i]['threshholds'] = []
        Dict2[i]['TPR'] = []
        Dict2[i]['FPR'] = []
    for i in predictors: 
        Dict4[i]['threshholds'] = []
        Dict4[i]['N_sum'] = []
        Dict4[i]['TP_Total_sum'] = []
        Dict4[i]['FP_Total_sum'] = []
        Dict4[i]['Neg_Total_sum'] = []   

    for i in np.arange(0.00, 1.02, .01):
        threshhold = float(str(round(i,2)))  
        
        for predictor in predictors:
            vals = ROC_dic.get(predictor)
            all_res_sum = vals[0] # total res 
            N_sum = vals[1] # total annotated 
            pred_sum = vals[2] #total over threshold 
            TP_Total_sum = vals[3] #sum of TP
            FP_Total_sum = vals[4] #sum of FP
            Neg_Total_sum = vals[5] #sum of neg 
            for protein in protein_in_cv:

                rows = []
                for protein_res in proteinname: 
                    if protein in protein_res:
                        rows.append(protein_res)
                
                counterframe = frame[frame.index.isin(rows)]
                cols = ['residue', predictor]
                counterframerf = pd.DataFrame(columns = cols)
                counterframerf = counterframe[[predictor]] 
                
                seq_res = counterframerf.index.values.tolist()
                seqnum = len(seq_res)
                pred_score= counterframerf[predictor]
                predictedframesort = counterframerf.sort_values(by=[predictor], inplace =False, ascending=False)
                
                thresholdframe= predictedframesort[predictedframesort[predictor] >= threshhold] 
                
                predicted_res = thresholdframe.index.values.tolist()
                predicted_res = [str(i) for i in predicted_res]
                pred_res = []
                for i in predicted_res: 
                    res_prot = i.split("_")
                    res = res_prot[0]
                    pred_res.append(res)
            
                N = 0
                annotated_res =[]
                for i in annotated_res_prot:
                    if protein in i:
                        tosplit = i.split("_")
                        res = tosplit[0]
                        annotated_res.append(res)
                        N +=1
                
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
              
                TP_Total_sum += TP
                FP_Total_sum += FP
                all_res_sum += seqnum # total res 
                N_sum += N # total annotated 
                pred_sum += pred #total over threshold 
                Neg_Total_sum += neg        
                predictor = "{}".format(predictor)
                diclist = [ all_res_sum , N_sum ,pred_sum,TP_Total_sum,FP_Total_sum, Neg_Total_sum]
                Dict[predictor][threshhold] = diclist
                
            all_res_sum = Dict[predictor][threshhold][0]
            TP_Total_sum = Dict[predictor][threshhold][3]
            FP_Total_sum = Dict[predictor][threshhold][4]
            Neg_Total_sum = Dict[predictor][threshhold][5]
            N_sum = Dict[predictor][threshhold][1]
            FPR = FP_Total_sum / Neg_Total_sum
            TPR = TP_Total_sum / N_sum
            Dict2[predictor]['threshholds'].append(threshhold)
            Dict2[predictor]['TPR'].append(TPR)
            Dict2[predictor]['FPR'].append(FPR)
            Dict4[predictor]['threshholds'].append(threshhold)
            Dict4[predictor]['Neg_Total_sum'].append(Neg_Total_sum)
            Dict4[predictor]['FP_Total_sum'].append(FP_Total_sum)
            Dict4[predictor]['N_sum'].append(N_sum)
            Dict4[predictor]['TP_Total_sum'].append(TP_Total_sum)
    return Dict3 , Dict2 , Dict4
def atoi(text):
    return int(text) if text.isdigit() else text

# ROC plot 
def ROC_Plt(Master, code,results_path):
    predictors = []
    for key in Master:
        predictors.append(key)
    color_index = 0    
    colors = ["#0000FF","#ff8333","#008000","#FFFF00","#800080","#00FF00","#808000","#00FFFF","#FF0000","#008080","#000080","#FF00FF"]
    plt.title('Receiver Operating Characteristic')
    plt.title('Receiver Operating Characteristic')
    for key in predictors:
        AUC = Master[key]["AUC"][0]
        AUC = AUC.round(3)
        TPRS = Master[key]['TPRS'][0]
        FPRS = Master[key]['FPRS'][0]
        plt.plot(FPRS, TPRS, c=colors[color_index], label = '{}: AUC = {}'.format(Master[key]["name"],AUC))
        color_index += 1
    plt.style.use("fivethirtyeight")
    plt.legend(loc = 'lower right')
    plt.plot([0, 1], [0, 1],'r--')
    plt.xlim([0, 1])
    plt.ylim([0, 1])
    plt.ylabel('True Positive Rate')
    plt.xlabel('False Positive Rate')
    plt.savefig( "{}/Crossvaltest{}/ROC.png" .format(results_path,code))
    plt.clf()

# RF tree vizualizer
def treeviz(treeparams, params,results_path):
    (X, y, tree) = treeparams
    (results_path,code,timer) = params
    viz = dtreeviz(tree, 
        X, 
        y,
        target_name='Interface',
        feature_names= ['predus','ispred','dockpred'], 
        class_names= ["non_interface", "interface"], 
        show_node_labels= True, 
        fancy=False 
        )  
    savefile = "{}Crossvaltest{}/Trees/Rftree_CV{}.svg".format(results_path,code,timer)
    viz.save(savefile)

#  three functions that perfrom star covariance plot 
def ROC_Star(data, code,timer,results_path):
    
    data = data.round({'predus': 3, 'ispred': 3, 'dockpred': 3, 'rfscore': 3,"logreg":3})
    Star_interface = data[data.annotated == 1] 
    Star_non_interface = data[data.annotated == 0]
    Star_interface = Star_interface.drop(columns="annotated")
    Star_non_interface = Star_non_interface.drop(columns="annotated")
    Star_interface = Star_interface.rename(columns={'predus':"T1", 'ispred': "T2", 'dockpred':"T3", 'rfscore':"T4",'logreg': 'T5'})
    Star_non_interface =Star_non_interface.rename(columns={'predus':"T1", 'ispred': "T2", 'dockpred':"T3", 'rfscore':"T4",'logreg': 'T5'})
    os.mkdir("{}Crossvaltest{}/Star/CV{}".format(results_path,code,timer))
    path = "{}Crossvaltest{}/Star/CV{}/StarinterfaceCV.txt".format(results_path,code,timer)
    Star_interface.to_csv(path,sep="\t", index=False, header=True)
    path = "{}Crossvaltest{}/Star/CV{}/StarnoninterfaceCV.txt".format(results_path, code,timer)
    Star_non_interface.to_csv(path,sep="\t", index=False, header=True)

def Star(results_path,code,Star_path):
    path = "{}Crossvaltest{}/Star".format(results_path, code)
    pathlist = os.listdir(path)
    pathlist.sort(key=natural_keys)
    for filename in pathlist:
        if filename.startswith("CV"):
            interface = f"{path}/{filename}/StarinterfaceCV.txt"
            non_int = f"{path}/{filename}/StarnoninterfaceCV.txt" 
            cmd ='./star --sort StarinterfaceCV.txt StarnoninterfaceCV.txt 0.05'
            subprocess.call(["cp",interface,Star_path])
            subprocess.call(["cp",non_int,Star_path])
            os.chdir(Star_path)
            subprocess.run(cmd, shell= True)
            data = pd.read_csv("{}results_sorted.txt".format(Star_path),header =1,engine='python',index_col = 0 , sep = '\t')
            pd.set_option('display.float_format', lambda x: '%.5f' % x)
            data = data.rename(columns={'T1':"predus", 'T2': "ispred", 'T3':"dockpred", 'T4':"rfscore",'T5': 'logreg'})
            for col in data.columns:
                data[col] = pd.to_numeric(data[col], errors='coerce')
                data[col] = data[col].replace(np.nan, col , regex=True)
            data = data.rename({'T1':"predus", 'T2': "ispred", 'T3':"dockpred", 'T4':"rfscore",'T5': 'logreg'},axis = 'index')
            values = data.values
            lower_triangular = values[np.tril_indices(values.shape[0], -1)]
            html = data.style.applymap(Color,lower_range =lower_triangular)
            html = html.render()
            imgkit.from_string(html,'{}Crossvaltest{}/tests/{}/{}.jpg'.format(results_path,code,filename,filename))
            
def Color(val,lower_range):
    if val in lower_range: 
        if val <= 0.05:
            color = 'green'
        else:
            color = 'red'
    else:
        color = "black"
    return 'color: %s' % color           

# used to sort by natural language for paths and directories 
def natural_keys(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]


if __name__ == '__main__':
    main()
