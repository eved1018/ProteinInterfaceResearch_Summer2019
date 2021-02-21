import numpy as np
import pandas as pd 
import os 
import concurrent.futures
import multiprocessing
from numpy import sqrt

def Main():
    predictors = ['predus', 'ispred', 'dockpred', 'rfscore','logreg']
    path ="/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Meta_DPI/META_DPI_RESULTS2/Meta_DPi_result.csv"
    result_path = "/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Fscore_MCC/results/"
    cutoff_path = "/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Fscore_MCC/All_protein_cutoffs.csv"
    # F_score(predictors,path,cutoff_path)
    cutoff_csv = pd.read_csv(cutoff_path)
    df = pd.read_csv(path)
    df["protein"] = [x.split('_')[1] for x in df['residue']]
    proteins = df["protein"].unique()
    cols = ["protein"] + predictors 
    f_score_per_protein = pd.DataFrame(columns = cols)
    f_score_per_protein["protein"] = proteins
    f_score_per_protein.set_index('protein', inplace=True)
    mcc_score_per_protein = pd.DataFrame(columns = cols)
    mcc_score_per_protein["protein"] = proteins
    mcc_score_per_protein.set_index('protein', inplace=True)
    for predictor in predictors:
            # print(predictor)
            TP_sum = 0
            FP_sum =0
            Ns_sum = 0
            threshold_sum = 0
            FN_sum = 0
            TN_sum = 0
            params_list = []
            for protein in proteins:
                frame = df[df["protein"] == protein] 
                params = [predictor,protein,cutoff_csv,frame] 
                params_list.append(params)
            with concurrent.futures.ProcessPoolExecutor() as executor:
                params_list = params_list
                results = executor.map( Run, params_list)
                for i in results:
                    (TP, TN, FP, FN, threshhold, N,predictor, protein) = i
                    TP_sum += TP
                    FP_sum += FP
                    Ns_sum += N
                    FN_sum += FN
                    TN_sum += TN
                    threshold_sum += threshhold
                    recall_p = TP/N
                    precision_p = TP/threshhold
                    f_score = (2 * recall_p *precision_p)/(recall_p + precision_p)
                    # print("{} fscore: {}".format(predictor,np.round(f_score,3)))
                    # df.loc[row_indexer,column_indexer]=value
                    f_score_per_protein.loc[protein,predictor] = f_score

                    MCC_num = (TP * TN) - (FP * FN)
                    mcc_denom = sqrt((TP + FN) * (TP + FP) * (TN + FP) * (TN + FN))
                    mcc = MCC_num / mcc_denom
                    # print("mcc", mcc, protein, predictor)
                    # print("{} MCC: {}".format(predictor,np.round(mcc,3)) )
                    mcc_score_per_protein.loc[protein,predictor] = mcc 


            recall = TP_sum/Ns_sum
            precision = TP_sum/threshold_sum
            f_score = (2 * recall *precision)/(recall + precision)
            print("{} fscore: {}".format(predictor,np.round(f_score,3)))

            MCC_num = (TP_sum * TN_sum) -(FP_sum * FN_sum)
            mcc_denom = sqrt((TP_sum + FN_sum) * (TP_sum + FP_sum) * (TN_sum + FP_sum) * (TN_sum + FN_sum))
            mcc = MCC_num / mcc_denom
            print("{} MCC: {}".format(predictor,np.round(mcc,3)) ) 

            f_score_per_protein.to_csv("{}fscore.csv".format(result_path))
            mcc_score_per_protein.to_csv("{}mcc.csv".format(result_path))

def Run(params): 
    (predictor,protein,cutoff_csv,frame) = params
    total_res = len(frame.index)
    annotated_frame = frame[frame['annotated'] == 1]
    annotated_res_prot = annotated_frame.index.tolist()
    cutoff_row = cutoff_csv[cutoff_csv["Protein"] == protein]
    threshhold = cutoff_row["cutoff res"].values[0]
    N = cutoff_row["annotated res"].values[0]
    predictedframesort = frame.sort_values(by=[predictor], inplace =False, ascending=False)
    thresholdframe = predictedframesort.head(threshhold) 
    predicted_res = thresholdframe.index.values.tolist()
    predicted_res = [str(i) for i in predicted_res]
    pred_res = []
    for i in predicted_res: 
        res_prot = i.split("_")
        res = res_prot[0]
        pred_res.append(int(res))

    
    Truepos = []
    for res in annotated_res_prot:
        if res in pred_res:
            Truepos.append(res)

    pred = len(pred_res)
    TP = len(Truepos)
    FP = pred - TP
    neg = total_res - threshhold
    FN = N - TP
    TN = neg - FN
    return TP, TN, FP, FN, threshhold, N ,predictor, protein
    
           


if __name__ == '__main__':
    Main()