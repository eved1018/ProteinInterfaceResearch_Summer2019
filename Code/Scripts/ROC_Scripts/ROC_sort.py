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

def ROC_Sort_bench():
    # set up DataFrame 
    aucframe= pd.DataFrame({})
    col_names = ['residue', 'score']

    results = pd.read_csv("/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/CrossVal/CVNOXBenchtest/RFvalBench.csv",header=0, names=col_names)
    # results.set_index('residue', inplace= True )
    results.set_index('residue', inplace= True )
    proteinname = results.index
    proteinids = []
    residue = []
    for resprot in proteinname: 
        res_prot = resprot.split("_")
        # print(res_prot[-1])
        proteinid = res_prot[1]
        if proteinid not in proteinids:
             proteinids.append(proteinid)
    print(proteinids)
    for i in proteinids : 
        framecol_names=['score']
        protienframe = pd.DataFrame(columns = framecol_names) 
        for protein_res in proteinname: 
                if i in protein_res:
                    rows = results.loc[protein_res]
                    protienframe = protienframe.append(rows)
        protein = protienframe.index 
        res = []
        for pdb in protein:
            sep = '_'
            rest = pdb.split(sep, 1)[0]
            res.append(rest)
        protienframe.insert(0,'residue',res,True)
        score = protienframe.score
        residues = protienframe.residue
        printout = pd.DataFrame({"residue": residues, "prediction score": score})
        path="/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/CrossVal/CVNOXBenchtest/RFBenchbypdb/RFval{}.csv".format(i)
        printout.to_csv(path,sep=",", index=False, header=True)
    
    
                    
# ROC_Sort_bench()

def ROC_Sort_Nox():
    # set up DataFrame 
    aucframe= pd.DataFrame({})
    col_names = ['residue', 'score']

    results = pd.read_csv("/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/CrossVal/CVNOXBenchtest/RFvalNox.csv",header=0, names=col_names)
    # results.set_index('residue', inplace= True )
    results.set_index('residue', inplace= True )
    proteinname = results.index
    proteinids = []
    residue = []
    for resprot in proteinname: 
        res_prot = resprot.split("_")
        # print(res_prot[-1])
        proteinid = res_prot[1]
        if proteinid not in proteinids:
             proteinids.append(proteinid)
    print(proteinids)
    for i in proteinids : 
        framecol_names=['score']
        protienframe = pd.DataFrame(columns = framecol_names) 
        for protein_res in proteinname: 
                if i in protein_res:
                    rows = results.loc[protein_res]
                    protienframe = protienframe.append(rows)
        protein = protienframe.index 
        res = []
        for pdb in protein:
            sep = '_'
            rest = pdb.split(sep, 1)[0]
            res.append(rest)
        protienframe.insert(0,'residue',res,True)
        score = protienframe.score
        residues = protienframe.residue
        printout = pd.DataFrame({"residue": residues, "prediction score": score})
        path="/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/CrossVal/CVNOXBenchtest/RFNoxbypdb/RFval{}.csv".format(i)
        printout.to_csv(path,sep=",", index=False, header=True)


    
# ROC_Sort_Nox()

def ROC_thresh_Nox_bench():
    zero_col = ["protein", "TP", "N", "TPR" , "FP", "neg" , "FPR"]
    zero_results = pd.DataFrame(columns=zero_col)
    col_names = ['residue', 'score']
    final_cols = ["threshold","Global_Dbmark_TPR","Global_Dbmark_FPR" ,"Pred_Dbmark_sum","Ressum_Dbmark","Global_NOX_TPR","Global_NOX_FPR","Global_Total_TPR"," Global_Total_FPR"]
    final_results = pd.DataFrame(columns= final_cols)
    Dbmark_annotateddir = "/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Annotated_Residues/Dbmark_Annotated_Residues"
    for i in np.arange(0.00, 1.02, .01):
        threshhold = float(str(round(i,2)))
        # print(threshhold)
        TP_Dbmark_sum = 0
        TP_NOX_sum = 0
        FP_Dbmark_sum = 0
        FP_NOX_sum = 0
        Ressum_Dbmark = 0
        Ressum_NOX = 0
        Neg_Dbmark_sum = 0
        Neg_NOX_sum = 0
        for filename in os.listdir(Dbmark_annotateddir):
            if filename.endswith("Residues"):
                N = 0
                annotated_res =[]
                with open("{}/{}".format(Dbmark_annotateddir,filename)) as AnnFile:
                    for line in AnnFile:
                        line = line.strip("\n")
                        N +=1
                        line = line.split("_")
                        line = line[0]
                        annotated_res.append(line)
                # print("{} {}".format(filename , N))
                name = filename.split("_")
                protienname = name[0]
                prefix = "RFval"
                suffix = ".csv"
                proteinfile= "{}{}{}".format(prefix, protienname, suffix)
                benchframe = pd.read_csv("/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/CrossVal/CVNOXBenchtest/RFBenchbypdb/{}".format(proteinfile))
                benchframe.rename({"residue": "residue", "prediction score": "score"}, axis='columns', inplace=True)
                # print(benchframe.head())
                bench_res = benchframe.residue
                seq_res = benchframe['residue'].values.tolist()
                seqnum = len(seq_res)
                bench_score= benchframe.score
                benchframesort = benchframe.sort_values(by=['score'], inplace =False, ascending=False)
                thresholdframe= benchframesort[benchframe.score >= threshhold] 
                # print(thresholdframe.head())
                predicted_res = thresholdframe['residue'].values.tolist()
                predicted_res = [str(i) for i in predicted_res]
                # print(predicted_res) 
                # print(annotated_res)  
                Truepos = []
                for res in annotated_res:
                    if res in predicted_res:
                        Truepos.append(res)
                # print(Truepos)
                # print(len(Truepos))
                
                pred = len(predicted_res)
                TP = len(Truepos)
                TPR = TP/N 
                FP = pred - TP
                neg = seqnum - N
                FPR = FP/neg
                # print("threshold {}".format(threshhold))
                # print("pred: {}".format(pred))
                # print("TPR: {}".format(TPR))
                # print("FPR: {}".format(FPR))
            if threshhold == 0 :
                to_append = [protienname, TP, N, TPR, FP, neg, FPR]
                a_series = pd.Series(to_append, index = zero_results.columns)
                zero_results = zero_results.append(a_series, ignore_index=True)
                # print(results.head())
                path="/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/CrossVal/CVNOXBenchtest/ZeroThresholdtest/DBZeroThresholdtest.csv"
                zero_results.to_csv(path,sep=",", index=False, header=True)
            TP_Dbmark_sum += TP
            FP_Dbmark_sum += FP
            Ressum_Dbmark += N
            Neg_Dbmark_sum += neg
            Seq_Dbmark_sum = Neg_Dbmark_sum + Ressum_Dbmark
            Pred_Dbmark_sum = TP_Dbmark_sum + FP_Dbmark_sum
            Global_Dbmark_TPR = TP_Dbmark_sum/Ressum_Dbmark
            Global_Dbmark_FPR = FP_Dbmark_sum/Neg_Dbmark_sum
            # print("Global_Dbmark_TPR: {}".format(Global_Dbmark_TPR))
            # print("Global_Dbmark_FPR: {}".format(Global_Dbmark_FPR)) 
        nox_annotateddir = "/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Annotated_Residues/NOX_Annotated_Residues"
        for filename in os.listdir(nox_annotateddir):
            if filename.endswith("Residues"):
                N = 0
                annotated_res =[]
                with open("{}/{}".format(nox_annotateddir,filename)) as AnnFile:
                    for line in AnnFile:
                        line = line.strip("\n")
                        N +=1
                        line = line.split("_")
                        line = line[0]
                        annotated_res.append(line)
                # print("{} {}".format(filename , N))
                name = filename.split("_")
                protienname = name[0]
                prefix = "RFval"
                suffix = ".csv"
                proteinfile= "{}{}{}".format(prefix, protienname, suffix)
                Noxframe = pd.read_csv("/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/CrossVal/CVNOXBenchtest/RFNoxbypdb/{}".format(proteinfile))
                Noxframe.rename({"residue": "residue", "prediction score": "score"}, axis='columns', inplace=True)
                # print(benchframe.head())
                Nox_res = Noxframe.residue
                seq_res = Noxframe['residue'].values.tolist()
                seqnum = len(seq_res)
                Nox_score= Noxframe.score
                Noxframesort = Noxframe.sort_values(by=['score'], inplace =False, ascending=False)
                thresholdframe= Noxframesort[Noxframe.score >= threshhold] 
                # print(thresholdframe.head())
                predicted_res = thresholdframe['residue'].values.tolist()
                predicted_res = [str(i) for i in predicted_res]
                # print(predicted_res) 
                # print(annotated_res)  
                Truepos = []
                for res in annotated_res:
                    if res in predicted_res:
                        Truepos.append(res)
                # print(Truepos)
                # print(len(Truepos))
                
                pred = len(predicted_res)
                TP = len(Truepos)
                TPR = TP/N 
                FP = pred - TP
                neg = seqnum - N
                FPR = FP/neg
                # print("threshold {}".format(threshhold))
                # print("pred: {}".format(pred))
                # print("TPR: {}".format(TPR))
                # print("FPR: {}".format(FPR))
            if threshhold == 0 :
                to_append = [protienname, TP, N, TPR, FP, neg, FPR]
                a_series = pd.Series(to_append, index = zero_results.columns)
                zero_results = zero_results.append(a_series, ignore_index=True)
                # print(results.head())
                path="/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/CrossVal/CVNOXBenchtest/ZeroThresholdtest/NOXZeroThresholdtest.csv"
                zero_results.to_csv(path,sep=",", index=False, header=True)
            TP_NOX_sum += TP
            FP_NOX_sum += FP
            Ressum_NOX += N
            Neg_NOX_sum += neg
            Seq_NOX_sum = Neg_NOX_sum + Ressum_NOX
            Pred_NOX_sum = TP_NOX_sum + FP_NOX_sum
            Global_NOX_TPR = TP_NOX_sum/Ressum_NOX
            Global_NOX_FPR = FP_NOX_sum/ Neg_NOX_sum
            # print("Global_Nox_TPR: {}".format(Global_NOX_TPR))
            # print("Global_Nox_FPR: {}".format(Global_NOX_FPR)) 
            TP_Total_sum = TP_NOX_sum + TP_Dbmark_sum
            FP_Total_sum = FP_NOX_sum + FP_Dbmark_sum
            Ressum_Total = Ressum_NOX + Ressum_Dbmark
            Neg_Total_sum = Neg_NOX_sum + Neg_Dbmark_sum
            Global_Total_TPR = TP_Total_sum/Ressum_Total
            Global_Total_FPR = FP_Total_sum/Neg_Total_sum
        to_append = [threshhold,Global_Dbmark_TPR,Global_Dbmark_FPR,Pred_Dbmark_sum,Ressum_Dbmark,Global_NOX_TPR,Global_NOX_FPR,Global_Total_TPR,Global_Total_FPR]
        a_series = pd.Series(to_append, index = final_results.columns)
        final_results = final_results.append(a_series, ignore_index=True)
        path="/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/CrossVal/CVNOXBenchtest/final/ROCfinalResults.csv"
        final_results.to_csv(path,sep=",", index=False, header=True)
                        

ROC_thresh_Nox_bench()




