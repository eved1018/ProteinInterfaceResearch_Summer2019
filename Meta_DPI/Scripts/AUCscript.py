import pandas as pd
import numpy as np
import concurrent.futures
import multiprocessing
from pathlib import Path
# ROC and PR per predictor 

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
    return predictor , ROC_AUC ,PR_AUC
    
# if __name__ == '__main__':
#     Main()