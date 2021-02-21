import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import roc_auc_score
def Main():
    predictor = "rfscore"
    ROC(predictor)
    path ="/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Meta_DPI/META_DPI_RESULTS3/Meta_DPI_result.csv"
    frame = pd.read_csv(path)

def ROC(predictor,frame):
    # predictor = "rfscore"
    # path = '/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/CrossVal_logreg_RF/meta-ppisp/meta-ppisp-results-comma.csv'
    # path = '/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/CrossVal_logreg_RF/meta-ppisp/meta-pisp-test.csv'
    
    frame.set_index('residue', inplace= True )
    # print(frame.head())
    frame = frame[frame['annotated'] != "ERROR"]    
    # print(frame)
    proteinname = frame.index
    proteins = frame.index.tolist()
    proteins = list(set([i.split("_")[1] for i in proteins]))
    frame["annotated"] = pd.to_numeric(frame["annotated"])
    annotated_frame = frame[frame['annotated'] == 1]
    annotated_res_prot = annotated_frame.index.tolist()
    TPRS = []
    FPRS = []
    threshholds= []
    
    for i in np.arange(0.00, 1.02, .01):
        threshhold = float(str(round(i,2)))  
        TP_sum = 0
        FP_sum =0
        negs_sum = 0
        Ns_sum = 0
        
        for protein in proteins:
            # print(protein)
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
            # pred_score= counterframerf[predictor]
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
            # print(annotated_res)
            Truepos = []
            for res in annotated_res:
                if res in pred_res:
                    Truepos.append(res)
            pred = len(pred_res)
            TP = len(Truepos)
            # TPR = TP/N 
            FP = pred - TP
            neg = seqnum - N
            TP_sum += TP
            FP_sum += FP
            negs_sum += neg
            Ns_sum += N

        TPR = TP_sum / Ns_sum
        FPR = FP_sum / negs_sum
        TPRS.append(TPR)
        FPRS.append(FPR)


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
    print(sum_AUC)
    plt.title('Receiver Operating Characteristic')
    plt.title('Receiver Operating Characteristic')
    AUC = sum_AUC
    AUC = AUC.round(3)
    plt.plot(FPRS, TPRS, c="#00FF00", label = '{}: AUC = {}'.format(predictor,AUC))
    plt.style.use("fivethirtyeight")
    plt.legend(loc = 'lower right')
    plt.plot([0, 1], [0, 1],'r--')
    plt.xlim([0, 1])
    plt.ylim([0, 1])
    plt.ylabel('True Positive Rate')
    plt.xlabel('False Positive Rate')
    # savepath =""
    # plt.savefig(savepath)
    plt.show()
    # plt.clf()
    




