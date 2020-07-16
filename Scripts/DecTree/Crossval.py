
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



#  StAR analysis preperation. fits the data in the correct format for StAR
# params 
#   frame is the pandas dataframe with columns residue, predus, ispred, dockpred, annotated, RFscore and MetaDPI(logreg) 
#   code is a number used to keep track of the test number, ie which params are used in what 
#   time is the time of itteration, ie which K-1 set is being used 
# returns:
#       two file: eahc with rows  predus, ispred, dockpred, RFscore and MetaDPI(logreg) 
#       one file is interface (annotated == 1) the other is noninterface (annotated == 0) 
#       * the colums are changed to short forms to comply with Star  -> 'predus':"T1", 'ispred': "T2", 'dockpred':"T3", 'rfscore':"T4",'logreg': 'T5'}
#       * the data in the files are tab separated and are '.txt' files



def ROC_Star(data, code,time):
    # print("star set up")
    # print(data.head())
    data = data.round({'predus': 3, 'ispred': 3, 'dockpred': 3, 'rfscore': 3,"logreg":3})
    Star_interface = data[data.annotated == 1] 
    Star_non_interface = data[data.annotated == 0]
    Star_interface = Star_interface.drop(columns="annotated")
    Star_non_interface = Star_non_interface.drop(columns="annotated")
    Star_interface = Star_interface.rename(columns={'predus':"T1", 'ispred': "T2", 'dockpred':"T3", 'rfscore':"T4",'logreg': 'T5'})
    Star_non_interface =Star_non_interface.rename(columns={'predus':"T1", 'ispred': "T2", 'dockpred':"T3", 'rfscore':"T4",'logreg': 'T5'})
    os.mkdir("/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/CrossVal_logreg_RF/Crossvaltest{}/Star/CV{}".format(code,time))
    path = "/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/CrossVal_logreg_RF/Crossvaltest{}/Star/CV{}/StarinterfaceCV{}.txt".format(code,time,time)
    Star_interface.to_csv(path,sep="\t", index=False, header=True)
    path = "/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/CrossVal_logreg_RF/Crossvaltest{}/Star/CV{}/StarnoninterfaceCV{}.txt".format(code,time,time)
    Star_non_interface.to_csv(path,sep="\t", index=False, header=True)



# ROC calculation ONLY FOR RF NEED TO ADD FOR META-DPI
# params: 
    # frame is the pandas dataframe with columns residue, predus, ispred, dockpred, annotated, RFscore and MetaDPI(logreg) score
    # protein_in_cv is a list of the proteins in the K-1 set 
    # code is a number used to keep track of the test number, ie which params are used in what 
    # time is the time of itteration, ie which K-1 set is being used 
# returns:
    # The AUC for that K-1 set, which is then returned to the CrossVal function to calculate the STD and Average  

def ROC_calc(frame,protein_in_cv,code,time):
    # final_cols = ["threshold","TPR","FPR" ]
    # final_results = pd.DataFrame(columns= final_cols)
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
        log_TP_Total_sum, log_FP_Total_sum ,log_all_res_sum, log_N_sum ,log_pred_sum , log_Neg_Total_sum = logregroc(threshhold,frame,protein_in_cv,code,time)
        for protein in protein_in_cv:
            # col_names = [ 'residue','predus', 'ispred', 'dockpred', 'annotated','rfscore','logreg']
            # counterframe = pd.DataFrame(columns = col_names)
            rows = []
            for protein_res in proteinname: 
                if protein in protein_res:
                    row = frame.loc[protein_res]
                    rows.append(row)
            
            counterframe = pd.DataFrame(rows,columns = ['predus','ispred','dockpred','annotated', 'rfscore','logreg'])
            # print(counterframe.head())
            cols = ['residue', 'rfscore']
            counterframerf = pd.DataFrame(columns = cols)
            # counterframerf = counterframe.index
            counterframerf = counterframe[['rfscore']] 
            # counterframerf.reset_index(level=0, inplace=True)
            # counterframerf.rename({"index": "residue", " rfscore": "rfscore"}, axis='columns', inplace=True)
            # print(counterframerf.head())
            # pred_res = counterframerf.index
            seq_res = counterframerf.index.values.tolist()
            seqnum = len(seq_res)
            pred_score= counterframerf.rfscore
            predictedframesort = counterframerf.sort_values(by=['rfscore'], inplace =False, ascending=False)
            
            thresholdframe= predictedframesort[predictedframesort.rfscore >= threshhold] 
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
    log_Global_TPR = log_TP_Total_sum / log_N_sum
    log_TPRS.append(log_Global_TPR)
    log_Global_FPR = log_FP_Total_sum / log_Neg_Total_sum
    log_FPRS.append(log_Global_FPR)
    log_threshholds.append(threshhold)
    log_final_results = pd.DataFrame(
    {'threshold': log_threshholds,
     'TPR': log_TPRS,
     'FPR': log_FPRS
    })

    distance = log_final_results["FPR"].diff()
    midpoint  = log_final_results["TPR"].rolling(2).sum()
    distance = distance * -1
    log_AUC = (distance) * (midpoint)
    log_AUC = AUC/2
    log_sum_AUC = log_AUC.sum()
    

    return sum_AUC , log_sum_AUC


def logregroc(threshhold,frame,protein_in_cv,code,time):
    proteinname = frame.index 
    log_all_res_sum = 0 # total res 
    log_N_sum = 0 # total annotated 
    log_pred_sum = 0 #total over threshold 
    log_TP_Total_sum = 0 #sum of TP
    log_FP_Total_sum = 0 #sum of FP
    log_Neg_Total_sum = 0 #sum of neg 
    for protein in protein_in_cv:
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
            # counterframerf = counterframe.index
            counterframerf = counterframe[['logreg']] 
            # counterframerf.reset_index(level=0, inplace=True)
            # counterframerf.rename({"index": "residue", " rfscore": "rfscore"}, axis='columns', inplace=True)
            # print(counterframerf.head())
            # pred_res = counterframerf.index
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


                

# ROC calculation ONLY FOR RF NEED TO ADD FOR META-DPI
# params: 
    # frame is the pandas dataframe with columns residue, predus, ispred, dockpred, annotated, RFscore and MetaDPI(logreg) score
    # protein_in_cv is a list of the proteins in the K-1 set 
    # code is a number used to keep track of the test number, ie which params are used in what 
    # time is the time of itteration, ie which K-1 set is being used 
# returns:
    # The AUC for that K-1 set, which is then returned to the CrossVal function to calculate the STD and Average  

def ROC_calc(frame,protein_in_cv,code,time):
    # final_cols = ["threshold","TPR","FPR" ]
    # final_results = pd.DataFrame(columns= final_cols)
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
        log_TP_Total_sum, log_FP_Total_sum ,log_all_res_sum, log_N_sum ,log_pred_sum , log_Neg_Total_sum = logregroc(threshhold,frame,protein_in_cv,code,time)
        for protein in protein_in_cv:
            # col_names = [ 'residue','predus', 'ispred', 'dockpred', 'annotated','rfscore','logreg']
            # counterframe = pd.DataFrame(columns = col_names)
            rows = []
            for protein_res in proteinname: 
                if protein in protein_res:
                    row = frame.loc[protein_res]
                    rows.append(row)
            
            counterframe = pd.DataFrame(rows,columns = ['predus','ispred','dockpred','annotated', 'rfscore','logreg'])
            # print(counterframe.head())
            cols = ['residue', 'rfscore']
            counterframerf = pd.DataFrame(columns = cols)
            # counterframerf = counterframe.index
            counterframerf = counterframe[['rfscore']] 
            # counterframerf.reset_index(level=0, inplace=True)
            # counterframerf.rename({"index": "residue", " rfscore": "rfscore"}, axis='columns', inplace=True)
            # print(counterframerf.head())
            # pred_res = counterframerf.index
            seq_res = counterframerf.index.values.tolist()
            seqnum = len(seq_res)
            pred_score= counterframerf.rfscore
            predictedframesort = counterframerf.sort_values(by=['rfscore'], inplace =False, ascending=False)
            
            thresholdframe= predictedframesort[predictedframesort.rfscore >= threshhold] 
            # print(thresholdframe.head())
            
            predicted_res = thresholdframe.index.values.tolist()
            predicted_res = [str(i) for i in predicted_res]
            pred_res = []
            for i in predicted_res: 
                res_prot = i.split("_")
                res = res_prot[0]
                pred_res.append(res)
            

            annotatedfile = "/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Annotated_Residues/AnnotatedTotal/{}_Interface_Residues".format(protein)
            

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
            # print("in")
            # print(all_res_sum , N_sum ,pred_sum,TP_Total_sum,FP_Total_sum,Neg_Total_sum,threshhold)

        Global_TPR = TP_Total_sum / N_sum
        TPRS.append(Global_TPR)
        Global_FPR = FP_Total_sum / Neg_Total_sum
        FPRS.append(Global_FPR)
        threshholds.append(threshhold)
        # print("out")
        # print(all_res_sum , N_sum ,pred_sum,TP_Total_sum,FP_Total_sum,Neg_Total_sum,threshhold)

    final_results = pd.DataFrame(
    {'threshold': threshholds,
     'TPR': TPRS,
     'FPR': FPRS
    })
    # print(final_results.head)

    distance = final_results["FPR"].diff()
    midpoint  = final_results["TPR"].rolling(2).sum()
    distance = distance * -1
    AUC = (distance) * (midpoint)
    AUC = AUC/2
    sum_AUC = AUC.sum()

    log_Global_TPR = log_TP_Total_sum / log_N_sum
    log_TPRS.append(log_Global_TPR)
    log_Global_FPR = log_FP_Total_sum / log_Neg_Total_sum
    log_FPRS.append(log_Global_FPR)
    log_threshholds.append(threshhold)
    log_final_results = pd.DataFrame(
    {'threshold': log_threshholds,
     'TPR': log_TPRS,
     'FPR': log_FPRS
    })

    distance = log_final_results["FPR"].diff()
    midpoint  = log_final_results["TPR"].rolling(2).sum()
    distance = distance * -1
    log_AUC = (distance) * (midpoint)
    log_AUC = AUC/2
    log_sum_AUC = log_AUC.sum()
    return sum_AUC , log_sum_AUC


         
# Logistic regresion function
# params:
#     test_frame is the pandas dataframe that the regresion predicts interface scores for 
#     train_frame is the andas dataframe that the regresion fits to 
#     time is an iterirator used to keep track of each implementation of the regresion 
#     cols is the feature columns of the dataframe, ie what each column is data for 
# returns
#     three files:
#         1) the coeficants for the regresion fitting 
#         2) the predction scores for the test_frame 
#         3) the dataframe used to train the regresion


def LogReg(test_frame, train_frame,time,cols,code):
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
        folder = "/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/CrossVal_logreg_RF/Crossvaltest{}/tests/CV{}" .format(code,time)
        os.mkdir(folder)
        file1 = open("/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/CrossVal_logreg_RF/Crossvaltest{}/tests/CV{}/cvcoef{}.txt" .format(code,time,time), "w")
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
        # results = pd.DataFrame({"residue": protein, "prediction value": pval})
        results = test_frame.assign(logreg = pval)
        path="/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/CrossVal_logreg_RF/Crossvaltest{}/tests/CV{}/predval{}.csv".format(code,time,time)
        results.to_csv(path,sep=",", index=True, header=True)
        # pathtest="/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/CrossVal_logreg_RF/Crossvaltest2/CV{}/trainframe{}.csv".format(time,time)
        # train_frame.to_csv(pathtest,sep=",", index=True, header=True)
        



# Random Forest function 
# params:
#   test_frame is the pandas dataframe that the regresion predicts interface scores for 
#     train_frame is the andas dataframe that the regresion fits to 
#     time is an iterirator used to keep track of each implementation of the regresion 
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
    
def RandomFor(test_frame, train_frame,time,cols,code,protein_in_cv,trees,depth,ccp): 
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
        # results= pd.DataFrame({"residue": protein, "prediction score": y_prob_interface})
        # path="/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/CrossVal_logreg_RF/Crossvaltest2/CV{}/RFval{}.csv".format(time,time)
        # results.to_csv(path,sep=",", index=False, header=True)
        df2 = test_frame.assign(rfscore = y_prob_interface )
        path="/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/CrossVal_logreg_RF/Crossvaltest{}/tests/CV{}/RFval{}.csv".format(code,time,time)
        df2.to_csv(path,sep=",", index=True, header=True)
        if time == 1:
                # for i in range(0,100):
                #     tree = model.estimators_[i]
                #     print(tree.get_depth())
                tree = model.estimators_[0]
                # path = tree.cost_complexity_pruning_path(X, y)
                # ccp_alphas, impurities = path.ccp_alphas, path.impurities
                # print(ccp_alphas)
                # plt.figure(figsize=(10, 6))
                # plt.plot(ccp_alphas, impurities)
                # plt.xlabel("effective alpha")
                # plt.ylabel("total impurity of leaves")
                # plt.show()
                # clfs = []
                # for ccp_alpha in ccp_alphas:
                #     clf = DecisionTreeClassifier(random_state=0, ccp_alpha=ccp_alpha)
                #     clf.fit(X, y)
                #     clfs.append(clf)

                # from sklearn.metrics import accuracy_score
                # acc_scores = [accuracy_score(y_test, tree.predict(X_test)) for tree in clfs]
                # plt.figure(figsize=(10,  6))
                # plt.grid()
                # plt.plot(ccp_alphas[:-1], acc_scores[:-1])
                # plt.xlabel("effective alpha")
                # plt.ylabel("Accuracy scores")
                # max_y = max(acc_scores[:-1])
                # xpos = acc_scores[:-1].index(max_y)
                # max_x = ccp_alphas[:-1][xpos]
                # print(max_x, max_y)
                # plt.show()
                viz = dtreeviz(tree, 
                X, 
                y,
                target_name='Interface',
                feature_names= ['predus','ispred','dockpred'], 
                class_names= ["non_interface", "interface"], 
                show_node_labels= True, 
                fancy=False 
                )  
                savefile = "/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/CrossVal_logreg_RF/Crossvaltest{}/Trees/Rftree_CV{}.svg".format(code,time)
                viz.save(savefile)

        
        totalframe = df2.copy()
        logpath = "/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/CrossVal_logreg_RF/Crossvaltest{}/tests/CV{}/predval{}.csv".format(code,time,time)
        log_cols = ['predus', 'ispred', 'dockpred', 'annotated','logreg']
        logframe = pd.read_csv(logpath, header =0 , names =log_cols)
        logs = logframe["logreg"]
        totalframe = totalframe.join(logs)
        # print(totalframe.head())
        # path = "/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/CrossVal_logreg_RF/Crossvaltest{}/tests/CV{}/totalframe{}.csv".format(time,time)
        # totalframe.to_csv(path,sep=",", index=True, header=True)
        sum_AUC, log_sum_AUC = ROC_calc(totalframe,protein_in_cv,code,time)
        # ROC_Star(totalframe,code,time)
        return sum_AUC , log_sum_AUC



# Cross validation function: 
# splits up the data into ten test sets with corresponding traingin set, whcih includes all the data except the test set. 
# then sends each test/train pair into the logistic regresion and random forest functions. 
# it then takes in the AUC's and returns the avarage and standard deviation  
# finaly the results are outputed as a '.txt' file 



def CrossVal():
    # params to adjust RF
    trees = 100
    depth  = 10 
    ccp = 0.0000400902332
    AUCS_CVS = []
    log_AUCS_CVS = []
    AUCs = []
    log_AUCs = []
    global_AUC= 0
    log_global_AUC = 0
    # test run code
    code = 32

    folder = "/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/CrossVal_logreg_RF/Crossvaltest{}" .format(code)
    os.mkdir(folder)
    folder = "/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/CrossVal_logreg_RF/Crossvaltest{}/tests" .format(code)
    os.mkdir(folder)
    os.mkdir("/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/CrossVal_logreg_RF/Crossvaltest{}/Star".format(code))
    os.mkdir( "/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/CrossVal_logreg_RF/Crossvaltest{}/Trees".format(code))
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
    n = 1
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
    if len(chunks[-1]) == 0:
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
        protein_in_cv = chunks[i]
        train_frame = train_frame.drop(test_frame.index)
        # set variabel for iteration, to keep track of each test set, since i in range(0,k) includes zero, i is incresased by 1 for readabilty
        time = i+1
        
        # perfroms logistic regresion and random forest for each test and training set.
        LogReg(test_frame,train_frame,time,feature_cols,code )
        sum_AUC , log_sum_AUC = RandomFor(test_frame,train_frame,time,feature_cols,code,protein_in_cv,trees,depth,ccp)
        AUCs.append(sum_AUC)
        print(sum_AUC)
        global_AUC += sum_AUC
        Cv = "CV{}".format(i)
        to_append = (Cv,sum_AUC)
        AUCS_CVS.append(to_append)
        log_AUCs.append(log_sum_AUC)
        log_global_AUC += log_sum_AUC
        Cv = "CV{}".format(i)
        to_append = (Cv,log_sum_AUC)
        log_AUCS_CVS.append(to_append)
    avrg = global_AUC/ len(AUCs)
    omega = 0
    for i in AUCs:
        omega += (i - avrg) **2
    omega = omega/10
    omega = math.sqrt(omega)
    # log
    log_avrg = log_global_AUC/ len(log_AUCs)
    log_omega = 0
    for i in log_AUCs:
        log_omega += (i - avrg) **2
    log_omega = log_omega/10
    log_omega = math.sqrt(log_omega)

    # print("params:") 
    # print("     number of trees:{}".format(trees))
    # print("     depth of trees:{}".format(depth))
    # print("     Pruning paramter:{}".format(ccp))
    # for i in AUCS_CVS:
    #     print("set:{}  AUC:{}".format(i[0],i[1]))
    # print("STDD: {}".format(omega))
    # print("avrg: {}".format(avrg))
    file1 = open("/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/CrossVal_logreg_RF/Crossvaltest{}/results.txt".format(code),"w")
    params = ["params: \n", "\t number of trees: {} \n".format(trees),"\t depth of trees: {}\n".format(depth),"\t pruning paramter: {} \n".format(ccp),"AUCs: \n"]
    file1.writelines(params)
    file1.write("Random Forest\n")
    for i in AUCS_CVS:
        aucs = "set:{}  AUC:{} \n".format(i[0],i[1])
        file1.write(aucs)
    stats = "STD:{}\nAVRG: {}".format(omega, avrg)
    file1.writelines(stats)
    file1.write("\nLogreg\n")
    for i in log_AUCS_CVS:
        aucs = "set:{}  AUC:{} \n".format(i[0],i[1])
        file1.write(aucs)
    stats = "STD:{}\nAVRG: {}".format(log_omega, log_avrg)
    file1.writelines(stats)
    file1.close()
    


   
CrossVal()

def NoxRF():
    # folder = "/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/CrossVal_logreg_RF/CVNOXBenchtest"
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
    path="/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/CrossVal_logreg_RF/CVNOXBenchtest/RFvalBench.csv"
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
    path="/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/CrossVal_logreg_RF/CVNOXBenchtest/RFvalNox.csv"
    results.to_csv(path,sep=",", index=False, header=True)

# NoxRF()
# BenchRF()







    