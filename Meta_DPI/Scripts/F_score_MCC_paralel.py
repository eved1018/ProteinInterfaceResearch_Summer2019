import numpy as np
import pandas as pd 
import os 
import concurrent.futures
import multiprocessing
from numpy import sqrt
from pathlib import Path


# fscore and mcc  per protein(saved as csv) and per predictor (printed)


def Main(predictors,df,result_path,code):
    results_folder = f"{result_path}/Meta_DPI_results{code}/Fscore_MCC/"
    path = Path(__file__).parents[2]
#   predictors = ["vorffip"]
#   check that predictor is in columns
    # predictors = ['vorffip']
    # path ="/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Meta_DPI/META_DPI_RESULTS3/Meta_DPi_result.csv"
    # data_path = f"{path}/Meta_DPI/Data/Test_data/vorffip_columns.txt" #<- TODO change to metta ppisp 
    # path = "/Users/evanedelstein/Desktop/1p_test.csv"
    # result_path = f"{path}/Meta_DPI/Results/Fscore_MCC/"
    # result_path = f"{path}/Meta_DPI/Results/Fscore_MCC/Zerotest/" 
    cutoff_path = f"{path}/Meta_DPI/Data/Test_data/All_protein_cutoffs.csv"
    # cutoff = (6.1^-residues)(constant) # <- TODO make dynamic cutoff in script 
    cutoff_csv = pd.read_csv(cutoff_path)
    
    cut_off_protein = cutoff_csv["Protein"].tolist()
    # df = pd.read_csv(data_path)
    # df.set_index('residue', inplace= True )
    df["protein"] = [x.split('_')[1] for x in df.index]
    proteins = df["protein"].unique()
    proteins = [i for i in proteins if i in cut_off_protein]
    cols = ["protein"] + predictors 
    f_score_per_protein = pd.DataFrame(columns = cols)
    f_score_per_protein["protein"] = proteins
    f_score_per_protein.set_index('protein', inplace=True)
    mcc_score_per_protein = pd.DataFrame(columns = cols)
    mcc_score_per_protein["protein"] = proteins
    mcc_score_per_protein.set_index('protein', inplace=True)
    np.seterr(all='raise')
    for predictor in predictors:
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
                results = executor.map(Run, params_list)
                for i in results:
                    (TP, TN, FP, FN, threshhold, N,predictor, protein) = i
                    TP_sum += TP
                    FP_sum += FP
                    Ns_sum += N
                    FN_sum += FN
                    TN_sum += TN
                    threshold_sum += threshhold
                    recall_f_score = TP/N
                    precision_f_score = TP/threshhold
                    
                    if TP != 0:
                        f_score = (2 * recall_f_score *precision_f_score)/(recall_f_score + precision_f_score)
                        MCC_num = (TP * TN) - (FP * FN)
                        mcc_denom = sqrt((TP + FP) * (TP + FN)  * (TN + FP) * (TN + FN))
                        mcc = MCC_num / mcc_denom
                        
                    else:
                        f_score = 0
                        mcc = 0 # <- TODO do once with 0 and another wiht undefinded 
                        
                    f_score_per_protein.loc[protein,predictor] = f_score
                    mcc_score_per_protein.loc[protein,predictor] = mcc 


            recall = TP_sum/Ns_sum
            precision = TP_sum/threshold_sum
            f_score = (2 * recall * precision)/(recall + precision)
            print("{} Global f_score: {}".format(predictor,np.round(f_score,3)))

            MCC_num = (TP_sum * TN_sum) -(FP_sum * FN_sum)
            mcc_denom = sqrt((TP_sum + FN_sum) * (TP_sum + FP_sum) * (TN_sum + FP_sum) * (TN_sum + FN_sum))
            mcc = MCC_num / mcc_denom
            print("{} Global MCC: {}".format(predictor,np.round(mcc,3)) ) 

            f_score_per_protein.to_csv(f"{results_folder}fscore_per_protein.csv")
            mcc_score_per_protein.to_csv(f"{results_folder}mcc_per_protein.csv")

def Run(params): 
    (predictor,protein,cutoff_csv,frame) = params
    total_res = len(frame.index)
    annotated_frame = frame[frame['annotated'] == 1]
    annotated_res_prot = annotated_frame.index.tolist()
    annotated_res = [x.split('_')[0] for x in annotated_res_prot]
    cutoff_row = cutoff_csv[cutoff_csv["Protein"] == protein]
    threshhold = cutoff_row["cutoff res"].values[0]
    N = cutoff_row["annotated res"].values[0]
    predictedframesort = frame.sort_values(by=[predictor], inplace =False, ascending=False)
    thresholdframe = predictedframesort.head(threshhold) 
    predicted_res = thresholdframe.index.values.tolist()
    predicted_res = [str(i) for i in predicted_res]
    pred_res = [i.split("_")[0] for i in predicted_res]
    Truepos = [i for i in annotated_res if str(i) in pred_res]
    pred = len(pred_res)
    TP = len(Truepos)
    FP = pred - TP
    neg = total_res - threshhold
    FN = N - TP
    TN = neg - FN
    return TP, TN, FP, FN, threshhold, N ,predictor, protein


           


# if __name__ == '__main__':
#     Main()