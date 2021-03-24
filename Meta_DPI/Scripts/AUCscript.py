# from pandas.core import frame
# from Meta_DPI.Scripts.Meta_DPI import Meta_DPI
import pandas as pd
import numpy as np
import concurrent.futures
# import multiprocessing
from pathlib import Path
# ROC and PR per predictor 

# def test_wrap():
#     path = Path(__file__).parents[2]
#     predictors = ["vorffip","meta_ppisp"]
#     Meta_ppisp_frame = pd.read_csv("/Users/user/Desktop/Research_Evan/MetaDPI/Meta_DPI/Data/Test_data/meta-ppisp-results-comma-new.txt")
#     vorffip_frame = pd.read_csv("/Users/user/Desktop/Research_Evan/MetaDPI/Meta_DPI/Data/Test_data/vorffip_renumbered.txt")
#     # predictors = ["rfscore"]
#     # path ="/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Meta_DPI/META_DPI_RESULTS3/Meta_DPI_result.csv"
#     # path = "/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/PDBtest.csv"
#     # data_path = f"{path}/Meta_DPI/Results/MetaDPIResults"
#     # frame = pd.read_csv(data_path
#     frame = pd.DataFrame()
#     frame["residue"] = Meta_ppisp_frame["residue"]
#     frame["vorffip"] = vorffip_frame["vorffip"]
#     frame["meta_ppisp"] = Meta_ppisp_frame["meta-ppisp"]
#     frame["residue"] = Meta_ppisp_frame["residue"]
#     frame["annotated"] = Meta_ppisp_frame["annotated"]
#     frame.set_index('residue', inplace= True )
#     print(frame.head()) 
#     param_list = [] 
#     for i in predictors:
#         param = (i,frame)
#         param_list.append(param)
#     # print(param_list)
#     roc_cols = [[f"{key}_FPR",f"{key}_TPR"] for key in predictors]
#     roc_excel = pd.DataFrame(columns = roc_cols)
#     pr_cols = [[f"{key}_Recall",f"{key}_Precsion"] for key in predictors]
#     pr_excel = pd.DataFrame(columns = pr_cols)
#     with concurrent.futures.ProcessPoolExecutor() as executor:
#         param_list = param_list
#         results = executor.map( ROC, param_list)
#         for i in results:
#             (predictor, ROC_AUC,PR_AUC, PR_frame,results_frame) = i
#             roc_excel[f"{predictor}_TPR"]=results_frame["TPR"]
#             roc_excel[f"{predictor}_FPR"]=results_frame["FPR"]
#             pr_excel[f"{predictor}_Precsion"] = PR_frame["Precision"]
#             pr_excel[f"{predictor}_Recall"] = PR_frame["Recall"]
#             print(f"{predictor} ROC AUC: {ROC_AUC}")
#             print(f"{predictor} PR AUC: {PR_AUC}")
#     roc_excel.to_csv("/Users/user/Desktop/Research_Evan/MetaDPI/Meta_DPI/Data/Test_data/roc_results.csv")
#     pr_excel.to_csv("/Users/user/Desktop/Research_Evan/MetaDPI/Meta_DPI/Data/Test_data/pr_resulst.csv")
def test_wrap2():
    path = Path(__file__).parents[2]
    predictors = ["vorffip"]
    # data_path = "/Users/user/Desktop/Research_Evan/Raji_Summer2019_atom/Meta_DPI/Results/MetaDPIResults/Meta_DPI_results6/Meta_DPI_result.csv"
    data_path = f"{path}/Meta_DPI/Data/Test_data/vorffip_columns.txt"
    frame = pd.read_csv(data_path)
    frame.set_index('residue', inplace= True )
    print(frame.head()) 
    param_list = [] 
    for i in predictors:
        param = (i,frame)
        param_list.append(param)
    # print(param_list)
    roc_cols = [[f"{key}_FPR",f"{key}_TPR"] for key in predictors]
    roc_excel = pd.DataFrame(columns = roc_cols)
    pr_cols = [[f"{key}_Recall",f"{key}_Precsion"] for key in predictors]
    pr_excel = pd.DataFrame(columns = pr_cols)
    with concurrent.futures.ProcessPoolExecutor() as executor:
        param_list = param_list
        results = executor.map( ROC, param_list)
        for i in results:
            (predictor, ROC_AUC,PR_AUC, PR_frame,results_frame) = i
            roc_excel[f"{predictor}_TPR"]=results_frame["TPR"]
            roc_excel[f"{predictor}_FPR"]=results_frame["FPR"]
            pr_excel[f"{predictor}_Precsion"] = PR_frame["Precision"]
            pr_excel[f"{predictor}_Recall"] = PR_frame["Recall"]
            print(f"{predictor} ROC AUC: {ROC_AUC}")
            print(f"{predictor} PR AUC: {PR_AUC}")
    roc_excel.to_csv("/Users/user/Desktop/Research_Evan/Raji_Summer2019_atom/Meta_DPI/Results/MetaDPIResults/Meta_DPI_results6/roc_results.csv")
    pr_excel.to_csv("/Users/user/Desktop/Research_Evan/Raji_Summer2019_atom/Meta_DPI/Results/MetaDPIResults/Meta_DPI_results6/pr_resulst.csv")
    

def Main():
    path = Path(__file__).resolve().parent.parent.parent
    predictors = ['predus', 'ispred', 'dockpred',"rfscore","logreg"]
    # predictors = ["rfscore"]
    # path ="/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Meta_DPI/META_DPI_RESULTS3/Meta_DPI_result.csv"
    # path = "/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/PDBtest.csv"
    data_path = f"{path}/Meta_DPI/Results/MetaDPIResults"
    frame = pd.read_csv(data_path)
    frame.set_index('residue', inplace= True )
    param_list = []
    for i in predictors:
        param = (i,frame)
        param_list.append(param)
    # print(param_list)
    with concurrent.futures.ProcessPoolExecutor() as executor:
        param_list = param_list
        results = executor.map( ROC, param_list)
        for i in results:
            (predictor, ROC_AUC,PR_AUC) = i
            print(f"{predictor} ROC AUC: {ROC_AUC}")
            print(f"{predictor} PR AUC: {PR_AUC}")
    
    

def ROC(params):
    results_dict= {}
    pr_dict = {}
    (predictor,df) = params    
    df["protein"] = [x.split('_')[1] for x in df.index]
    proteins = df["protein"].unique()
    df = df[df['annotated'] != "ERROR"]    
    for i in np.arange(0.00, 1.02, .01):
        threshhold = float(str(round(i,2)))  
        TP_sum = 0
        FP_sum =0
        negs_sum = 0
        Ns_sum = 0
        threshold_sum = 0 
        pred_sum = 0
        all_res_sum = 0
        for protein in proteins:
            frame = df[df["protein"] == protein] 
            # to numeric 
            annotated_frame = frame[frame['annotated'] == 1]
            annotated_res_prot = annotated_frame.index.tolist()
            annotated_res = [x.split('_')[0] for x in annotated_res_prot] 
            N = len(annotated_res)          
            total_res = len(frame.index)
            predictedframesort = frame.sort_values(by=[predictor], inplace =False, ascending=False)
            thresholdframe= predictedframesort[predictedframesort[predictor] >= threshhold] 
            threshold_sum += threshhold
            predicted_res = thresholdframe.index.values.tolist()
            predicted_res = [str(i) for i in predicted_res]
            pred_res = [i.split("_")[0] for i in predicted_res]
            Truepos = [i for i in pred_res if i in annotated_res]
            
            pred = len(pred_res)
            TP = len(Truepos)
            
            FP = pred - TP
            neg = total_res - N
            # FN = N - TP
            # TN = neg - FN
            TP_sum += TP
            FP_sum += FP
            negs_sum += neg
            Ns_sum += N
            pred_sum += pred
            all_res_sum += total_res
            # FN_sum += FN
            # TN_sum += TN
            # print("hello")
        TPR = TP_sum / Ns_sum
        FPR = FP_sum / negs_sum
        # Recall = TP_sum/Ns_sum
        # Precision = TP_sum/pred_sum
        # pr_dict[threshhold] = [Precision,Recall]
        if pred_sum == 0:
            Recall = 0
            Precision = 0
            pr_dict[threshhold] = [Precision,Recall]
        else:
            Recall = TP_sum/Ns_sum
            Precision = TP_sum/pred_sum
            pr_dict[threshhold] = [Precision,Recall]
        results_dict[threshhold] = [TPR,FPR]
    # print("done")
    # print(results_dict)
    results_frame= pd.DataFrame.from_dict(results_dict,columns = ["TPR","FPR"],orient= 'index')
    # print(results_frname)
    distance = results_frame["FPR"].diff()
    midpoint  = results_frame["TPR"].rolling(2).sum()
    distance = distance * -1
    AUC = (distance) * (midpoint)
    AUC = AUC/2
    sum_AUC = AUC.sum()
    ROC_AUC = sum_AUC



    PR_frame = pd.DataFrame.from_dict(pr_dict,columns = ["Precision","Recall"],orient= 'index')
    # print(results_frname)
    distance = PR_frame["Recall"].diff()
    midpoint  = PR_frame["Precision"].rolling(2).sum()
    distance = distance * -1
    PR_AUC = (distance) * (midpoint)
    PR_AUC = PR_AUC/2
    sum_AUC = PR_AUC.sum()
    PR_AUC = sum_AUC
    return predictor , ROC_AUC ,PR_AUC, PR_frame,results_frame
    
if __name__ == '__main__':
    # Main()
    test_wrap2()