from numpy import sqrt
import pandas as pd 
import os 

# fscore per predictor 

def Main():
    predictors = ['predus', 'ispred', 'dockpred', 'rfscore','logreg']
    # path ="/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Meta_DPI/META_DPI_RESULTS2/Meta_DPi_result.csv"
    path = "/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Meta_DPI/META_DPI_RESULTS3/Meta_DPi_result.csv"
    cutoff_path = "/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Fscore_MCC/All_protein_cutoffs.csv"
    cutoff_csv = pd.read_csv(cutoff_path)
    df = pd.read_csv(path)
    dict = F_score(predictors,df,cutoff_csv)
    for i in dict: 
        f_score, mcc = dict[i]
        print("{} fscore: {}".format(i,f_score))
        print("{} MCC: {}".format(i,mcc))


def F_score(predictors,df,cutoff_csv):
    df.set_index('residue', inplace= True )
    df["protein"] = [x.split('_')[1] for x in df.index]
    proteins = df["protein"].unique()
    # print(df)
    dict = {}
    
    for predictor in predictors:
        # print(predictor)
        TP_sum = 0
        FP_sum =0
        negs_sum = 0
        Ns_sum = 0
        threshold_sum = 0
        FN_sum = 0
        TN_sum = 0 
        for protein in proteins:
            frame = df[df["protein"] == protein] 
            annotated_frame = frame[frame['annotated'] == 1]
            annotated_res_prot = annotated_frame.index.tolist()
            annotated_res = [x.split('_')[0] for x in annotated_res_prot]
            # print(annotated_res)
            total_res = len(frame.index)
            cutoff_row = cutoff_csv[cutoff_csv["Protein"] == protein]
            threshhold = cutoff_row["cutoff res"].values[0]
            N = cutoff_row["annotated res"].values[0]
            threshold_sum += threshhold
            predictedframesort = frame.sort_values(by=[predictor], inplace =False, ascending=False)
            thresholdframe = predictedframesort.head(threshhold) 
            predicted_res = thresholdframe.index.values.tolist()
            predicted_res = [str(i) for i in predicted_res]
            pred_res = [i.split("_")[0] for i in predicted_res]
            Truepos = [i for i in annotated_res if i in pred_res]
            pred = len(pred_res)
            TP = len(Truepos)
            FP = pred - TP
            neg = total_res - threshhold
            FN = N - TP
            TN = neg - FN
            TP_sum += TP
            FP_sum += FP
            negs_sum += neg
            Ns_sum += N
            FN_sum += FN
            TN_sum += TN
            
        recall = TP_sum/Ns_sum
        precision = TP_sum/threshold_sum
        f_score = (2 * recall *precision)/(recall + precision)
        MCC_num = (TP_sum * TN_sum) -(FP_sum * FN_sum)
        mcc_denom = sqrt((TP_sum + FN_sum) * (TP_sum + FP_sum) * (TN_sum + FP_sum) * (TN_sum + FN_sum))
        mcc = MCC_num / mcc_denom
        dict[predictor] = [f_score,mcc]
    return dict       


if __name__ == '__main__':
    Main()