def F_score(predictors,df,cutoff_csv):
    df["protein"] = [x.split('_')[1] for x in df['residue']]
    proteins = df["protein"].unique()
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
            total_res = len(frame.index)
            cutoff_row = cutoff_csv[cutoff_csv["Protein"] == protein]
            threshhold = cutoff_row["cutoff res"].values[0]
            N = cutoff_row["annotated res"].values[0]
            threshold_sum += threshhold
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
        # print("{} fscore: {}".format(predictor,f_score))
        # print("{} MCC: {}".format(predictor,mcc))
        dict[predictor] = [f_score,mcc]
    print(dict)
    return dict 