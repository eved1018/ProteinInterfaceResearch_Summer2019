import pandas as pd
import numpy as np
import os 
import re 

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]

def RF_ROC_sort_cv():
    col_names = ['residue', 'predus', 'ispred', 'dockpred', 'annotated','score']
    os.mkdir("/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/CrossVal/Crossvaltest4/CVbyPDB")
    RF_dir="/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/CrossVal/Crossvaltest4/tests"
    for folder in os.listdir(RF_dir):
        if folder.startswith("CV")
            # print(folder)
            os.mkdir("/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/CrossVal/Crossvaltest4/CVbyPDB/{}".format(folder))
            folder_der = "/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/CrossVal/Crossvaltest4/tests/{}".format(folder)
            for filename in os.listdir(folder_der):
                if filename.startswith("RF"): 
                    print("{} in {}".format(filename, folder))
                    path ="/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/CrossVal/Crossvaltest4/tests/{}/{}".format(folder,filename)
                    results = pd.read_csv(path,header=0, names=col_names)
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
                    # print(proteinids)
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
                        path="/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/CrossVal/Crossvaltest4/CVbyPDB/{}/RFval{}.csv".format(folder,i)
                        printout.to_csv(path,sep=",", index=False, header=True)
# RF_ROC_sort_cv()

def RF_ROC_thresh():
    os.mkdir("/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/CrossVal/Crossvaltest4/RF/zeros")
    os.mkdir("/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/CrossVal/Crossvaltest4/RF/results")
    bypdbfolders = "/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/CrossVal/Crossvaltest4/RF/CVbyPDB"
    filelist =os.listdir(bypdbfolders)
    filelist.sort(key=natural_keys)
    for folder in filelist:
        if folder.startswith("CV"): 
            final_cols = ["threshold","TPR","FPR" ]
            final_results = pd.DataFrame(columns= final_cols)
            zero_col = ["protein", "TP", "N", "TPR" , "FP", "neg" , "FPR"]
            zero_results = pd.DataFrame(columns=zero_col)
            for i in np.arange(0.00, 1.02, .01):
                threshhold = float(str(round(i,2)))    
                all_res_sum = 0 # total res 
                N_sum = 0 # total annotated 
                pred_sum = 0 #total over threshold 
                TP_Total_sum = 0 #sum of TP
                FP_Total_sum = 0 #sum of FP
                Neg_Total_sum = 0 #sum of neg       
                proteinfolder = "{}/{}".format(bypdbfolders,folder)
                for filename in os.listdir(proteinfolder):
                    proteinname = filename.split("RFval")
                    proteinname = proteinname[1]
                    proteinname = proteinname.split(".csv")
                    proteinname = proteinname[0]
                    predictedframe = pd.read_csv("{}/{}".format(proteinfolder,filename))
                    predictedframe.rename({"residue": "residue", "prediction score": "score"}, axis='columns', inplace=True)
                    pred_res = predictedframe.residue
                    seq_res = predictedframe['residue'].values.tolist()
                    seqnum = len(seq_res)
                    pred_score= predictedframe.score
                    predictedframesort = predictedframe.sort_values(by=['score'], inplace =False, ascending=False)
                    thresholdframe= predictedframesort[predictedframesort.score >= threshhold] 
                    # print(thresholdframe.head())
                    predicted_res = thresholdframe['residue'].values.tolist()
                    predicted_res = [str(i) for i in predicted_res]
                    # print(predicted_res) 
                    # print(annotated_res) 
                    
                    annotatedfile = "/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Annotated_Residues/AnnotatedTotal/{}_Interface_Residues".format(proteinname)
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
                    # print("protein {}".format(proteinname))
                    # print("threshold {}".format(threshhold))
                    # print("pred: {}".format(pred))
                    # print("TPR: {}".format(TPR))
                    # print("FPR: {}".format(FPR))
                    TP_Total_sum += TP
                    FP_Total_sum += FP
                    all_res_sum += seqnum # total res 
                    N_sum  += N # total annotated 
                    pred_sum += pred #total over threshold 
                    Neg_Total_sum += neg
                    if threshhold == 0 :
                        to_append = [proteinname, TP, N, TPR, FP, neg, FPR]
                        a_series = pd.Series(to_append, index = zero_results.columns)
                        zero_results = zero_results.append(a_series, ignore_index=True)
                        # print(results.head())
                        path="/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/CrossVal/Crossvaltest4/RF/zeros/{}ZeroThresholdtest.csv".format(folder)
                        zero_results.to_csv(path,sep=",", index=False, header=True)
                    
                Global_TPR = TP_Total_sum / N_sum
                Global_FPR = FP_Total_sum / Neg_Total_sum
                # print("test number: {}".format(folder))
                # print("threshold:{}".format(threshhold))
                # print("Global_TPR : {} ".format(Global_TPR))
                # print("Global_FPR : {} ".format(Global_FPR))
                to_append = [threshhold,Global_TPR,Global_FPR]
                a_series = pd.Series(to_append, index = final_results.columns)
                final_results = final_results.append(a_series, ignore_index=True)
                path="/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/CrossVal/Crossvaltest4/RF/results/{}results.csv".format(folder)
                final_results.to_csv(path,sep=",", index=False, header=True)                       
RF_ROC_thresh()

def Log_ROC_sort_cv():
    col_names = ['residue', 'predus', 'ispred', 'dockpred', 'annotated','score']
    os.mkdir("/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/CrossVal/Crossvaltest4/Log/CVbyPDB")
    RF_dir="/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/CrossVal/Crossvaltest4/tests"
    for folder in os.listdir(RF_dir):
        if folder.startswith("CV"):
            # print(folder)
            os.mkdir("/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/CrossVal/Crossvaltest4/Log/CVbyPDB/{}".format(folder))
            folder_der = "/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/CrossVal/Crossvaltest4/tests/{}".format(folder)
            for filename in os.listdir(folder_der):
                if filename.startswith("pred"): 
                    print("{} in {}".format(filename, folder))
                    path ="/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/CrossVal/Crossvaltest4/tests/{}/{}".format(folder,filename)
                    results = pd.read_csv(path,header=0, names=col_names)
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
                    # print(proteinids)
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
                        path="/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/CrossVal/Crossvaltest4/Log/CVbyPDB/{}/RFval{}.csv".format(folder,i)
                        printout.to_csv(path,sep=",", index=False, header=True)
# Log_ROC_sort_cv()
def Log_ROC_thresh():
    os.mkdir("/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/CrossVal/Crossvaltest4/Log/zeros")
    os.mkdir("/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/CrossVal/Crossvaltest4/Log/results")
    bypdbfolders = "/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/CrossVal/Crossvaltest4/Log/CVbyPDB"
    filelist =os.listdir(bypdbfolders)
    filelist.sort(key=natural_keys)
    for folder in filelist:
        if folder.startswith("CV"): 
            final_cols = ["threshold","TPR","FPR" ]
            final_results = pd.DataFrame(columns= final_cols)
            zero_col = ["protein", "TP", "N", "TPR" , "FP", "neg" , "FPR"]
            zero_results = pd.DataFrame(columns=zero_col)
            for i in np.arange(0.00, 1.02, .01):
                threshhold = float(str(round(i,2)))    
                all_res_sum = 0 # total res 
                N_sum = 0 # total annotated 
                pred_sum = 0 #total over threshold 
                TP_Total_sum = 0 #sum of TP
                FP_Total_sum = 0 #sum of FP
                Neg_Total_sum = 0 #sum of neg       
                proteinfolder = "{}/{}".format(bypdbfolders,folder)
                for filename in os.listdir(proteinfolder):
                    proteinname = filename.split("RFval")
                    proteinname = proteinname[1]
                    proteinname = proteinname.split(".csv")
                    proteinname = proteinname[0]
                    predictedframe = pd.read_csv("{}/{}".format(proteinfolder,filename))
                    predictedframe.rename({"residue": "residue", "prediction score": "score"}, axis='columns', inplace=True)
                    pred_res = predictedframe.residue
                    seq_res = predictedframe['residue'].values.tolist()
                    seqnum = len(seq_res)
                    pred_score= predictedframe.score
                    predictedframesort = predictedframe.sort_values(by=['score'], inplace =False, ascending=False)
                    thresholdframe= predictedframesort[predictedframesort.score >= threshhold] 
                    # print(thresholdframe.head())
                    predicted_res = thresholdframe['residue'].values.tolist()
                    predicted_res = [str(i) for i in predicted_res]
                    # print(predicted_res) 
                    # print(annotated_res) 
                    
                    annotatedfile = "/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Annotated_Residues/AnnotatedTotal/{}_Interface_Residues".format(proteinname)
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
                    # print("protein {}".format(proteinname))
                    # print("threshold {}".format(threshhold))
                    # print("pred: {}".format(pred))
                    # print("TPR: {}".format(TPR))
                    # print("FPR: {}".format(FPR))
                    TP_Total_sum += TP
                    FP_Total_sum += FP
                    all_res_sum += seqnum # total res 
                    N_sum  += N # total annotated 
                    pred_sum += pred #total over threshold 
                    Neg_Total_sum += neg
                    if threshhold == 0 :
                        to_append = [proteinname, TP, N, TPR, FP, neg, FPR]
                        a_series = pd.Series(to_append, index = zero_results.columns)
                        zero_results = zero_results.append(a_series, ignore_index=True)
                        # print(results.head())
                        path="/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/CrossVal/Crossvaltest4/Log/zeros/{}ZeroThresholdtest.csv".format(folder)
                        zero_results.to_csv(path,sep=",", index=False, header=True)
                    
                Global_TPR = TP_Total_sum / N_sum
                Global_FPR = FP_Total_sum / Neg_Total_sum
                # print("test number: {}".format(folder))
                # print("threshold:{}".format(threshhold))
                # print("Global_TPR : {} ".format(Global_TPR))
                # print("Global_FPR : {} ".format(Global_FPR))
                to_append = [threshhold,Global_TPR,Global_FPR]
                a_series = pd.Series(to_append, index = final_results.columns)
                final_results = final_results.append(a_series, ignore_index=True)
                path="/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/CrossVal/Crossvaltest4/Log/results/{}results.csv".format(folder)
                final_results.to_csv(path,sep=",", index=False, header=True)   
# Log_ROC_thresh()