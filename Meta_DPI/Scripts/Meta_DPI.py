import pandas as pd
import numpy as np
import os 
import time 
import statsmodels.api as sm
from sklearn.ensemble import RandomForestClassifier
import concurrent.futures
import multiprocessing
import matplotlib.pyplot as plt
import Treeviz 
import AUCscript   
import Star 
import F_score_MCC_paralel 
import pymol_visualization
from pathlib import Path 
import os.path
import warnings
warnings.filterwarnings("ignore")

"""TODO:  
        1) make roc and pr graphs? or at least have that option , maybe put that in the AUCscript
        2) comment,clean up , spellcheck 
"""
"""
things to make this much faster:
1) have fscore run when auc threshold is alligned with dynamic cutoff
2) have pymol run when fscore runs, that way only one list of residues needs to be made
"""

"""
Instructions:
to download all the modules needed for this program dowload homebrew at https://brew.sh/ 
then cd into the project and run "pip3 install -r requirements.txt" followed by "brew bundle"
for protein visualization pymol is required. 
"""

# Runs Meta_DPI which performs logistic regresion (LR) and random forest(RF) to combine interface predictors into a single interface metric. 
# Takes in file of columns residue_protein | predictor 1 |predictor 2....| annotated
# annotated should be a binary classifier, 0 for non-interface and 1 for interface
# Returns 1 file and 2 directories:
#   (1) the input file appeneded with the LR score and RF score to the end as well as addition of columns names
#   (2) tests directory houses the output file 1 per each protein 
#   (3) trees directory houses RF tree images 
# set paramaters and file path in Main()
# Statistical tests can be performed by running the following modules: (path modification will be neccesery)
#   (A) ROC and Precision-Recall AUC per predictor: AUCscript.py 
#   (B) Fscore and MCC per protein and per predictor: F_score_MCC_paralel.py
#   (C) K-fold Cross-validation: Meta_DPI_Cross_Validation.py 

def Main(*kwargs):
    path = Path(__file__).parents[2]
    start = time.perf_counter()
    code = 1
    try:
        if len(kwargs) == 0:
            trees,depth, ccp = [int(x) for x in input("Enter random forest parameters: trees, depth, ccp:").split()]
            print_out = True if input("print out all results (y,n): ") == "y" else False
            param_test = True if input("run parameter tester (y,n): ") == "y" else False
            viz = True if input("run tree visualization (y,n): ") == "y" else False
            protein_viz = True if input("run protein visualization (y,n): ") == "y" else False
        else:
            (trees,depth, ccp,print_out,param_test,viz,protein_viz,data_path) = kwargs
            [int(i) for i in kwargs[0:3]]
            [bool(i) for i in kwargs[3:7]]
    except:
        print("Incorect parameters please try again")
        return  

    file_exists = False if type(data_path) != str else True
    if data_path == "test":
        data_path = f"{path}/Meta_DPI/Data/Test_data/final_sort_headers_test.csv"

    while file_exists is False:
        data_filename = input("file name of predictor csv with columns first column as res_proterin and last columns whetehr teh residue is annotated(1:yes, 0:no): ")
        data_path = f"{path}/Meta_DPI/Data/Test_data/final_sort_headers_test.csv" if data_filename == "test" else f"{path}/Meta_DPI/Data/Test_data/{data_filename}"
        file_exists = os.path.isfile(data_path)
    
    # load in dataset and get predictors 
    df = pd.read_csv(data_path)
    predictors = df.columns.tolist()[2:-1]
    # change to where u need it to to go 
    results_path = f"{path}/Meta_DPI/Results/MetaDPIResults"

    folder = f"{results_path}/Meta_DPI_results{code}" 
    while os.path.isdir(folder) is True:
        code = code + 1 
        folder = f"{results_path}/Meta_DPI_results{code}" 
    os.mkdir(folder)
    if param_test == True:
        Param_test(data_path,viz, code, trees, depth, ccp, start,results_path,predictors,print_out,path)
    else:
        vars = [depth,trees,ccp]
        result_list,roc_excel,pr_excel = Meta_DPI(df,data_path,viz, code, start,results_path,predictors,print_out,vars,path,protein_viz)
        for i in result_list:
            (predictor, ROC_AUC,PR_AUC) = i 
            print(f"{predictor} ROC AUC: {ROC_AUC}")
            print(f"{predictor} PR AUC: {PR_AUC}")
        pr_excel.to_csv(f"{folder}/pr_excel.csv")
        roc_excel.to_csv(f"{folder}/roc_excel.csv")
        finish = time.perf_counter()
        print(f"finished in {round((finish - start)/60,2 )} minutes(s)")
    return finish

# test params of RF 
def Param_test(data_path,viz, code, trees, depth, ccp, start,results_path,predictors,print_out,path):
    
    # ccps = [0.000025,0.00005, 0.000075]
    # trees = [500]
    # depth = [5,10,15,25,50]
    ccps = [0]
    results_frame = pd.DataFrame(columns=['param','ROC','PR'])
    for i in ccps:
        print("start")
        vars = [depth,trees,i]
        result_list,roc_excel,pr_excel = Meta_DPI(data_path,viz, code, start,results_path,predictors,print_out,vars,path)
        for i in result_list:
            (predictor, ROC_AUC,PR_AUC) = i 
            results_frame.loc[len(results_frame)] = [i,ROC_AUC,PR_AUC]
            print("ccp:",i)
            print("ROC AUC:", ROC_AUC)
        results_frame.plot.scatter(x="param",y="ROC",xlabel = "param" ) 
        plt.show()

# def Meta_DPI(data_path,viz, code, trees, depth, ccp, start,results_path,col_names,var_col_names,predictors,print_out,vars):

def Meta_DPI(df,data_path,viz, code,start,results_path,predictors,print_out,vars,path,protein_viz):
    (depth,trees,ccp) = vars
    if print_out == True:
        # folder = "{}/META_DPI_RESULTS{}" .format(results_path,code)
        # os.mkdir(folder)
        folder = "{}/META_DPI_RESULTS{}/By_protein" .format(results_path,code)
        os.mkdir(folder)
        os.mkdir( "{}/META_DPI_RESULTS{}/Trees".format(results_path,code))
        os.mkdir( "{}/META_DPI_RESULTS{}/Fscore_MCC".format(results_path,code))
    # set up DataFrame 
    # col_names = ['residue', 'predus', 'ispred', 'dockpred', 'annotated']
    # load dataset which is a csv file containing all the residues in Nox and Benchmark as well as predus, ispred, and dockpred scores. 
    # The last column is a binary annotated classifier, 0 is noninetrface 1 is interface. 

    # df = pd.read_csv("/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Antogen/predictionvalue/res_pred/test.csv", header=0)
    # set the residue_protein ID as the index of the DataFrame 
    df["protein"] = [x.split('_')[1] for x in df['residue']]
    proteins = df["protein"].unique()
    df.set_index('residue', inplace= True )
    # remove any null or missing data from the dataset and check that annoted is number 
    df.isnull().any()
    data = df.fillna(method='ffill')
    data = data[data['annotated'] != "ERROR"]
    data["annotated"] = pd.to_numeric(data["annotated"])
    # setup params for process pool 
    param_list = []
    for count, protein in enumerate(proteins):
        test = data[data["protein"] == protein] 
        train = data[data["protein"] != protein] 
        col_namestest = predictors + ["annotated"]
        test = test[col_namestest]
        feature_cols = predictors
        # Features, ie prediction scores from predus, ispred and dockpred 
        X = test[feature_cols] 
        # Target variable, noninterface or interface 
        y = test.annotated
        params = (X,y, train,feature_cols,code,results_path,protein ,trees,depth,ccp,viz,data_path,test,print_out,count )
        param_list.append(params)
    frames =[]
    
    with concurrent.futures.ProcessPoolExecutor() as executor:
            param_list = param_list
            results = executor.map( Run, param_list)
            for count,i in enumerate(results):
                (totalframe ,treeparams,coefficients) = i
                frames.append(totalframe)
                if count == 1 and viz == True:
                    Treeviz.treeviz(treeparams,results_path,code,feature_cols)

    result_frame = pd.concat(frames)
    if print_out == True:
        result_frame.to_csv("{}/META_DPI_RESULTS{}/Meta_DPI_result.csv" .format(results_path,code), float_format='{:f}'.format)
    result_frame.to_csv("{}/META_DPI_RESULTS{}/Meta_DPI_result.csv" .format(results_path,code), float_format='{:f}'.format)
    Star.Star_Leave_one_out(result_frame,path,results_path,code)
    predictors += ["logreg","rfscore"]
    F_score_MCC_paralel.Main(predictors,result_frame,results_path,code)
    if protein_viz == True:
        pymol_visualization.Main(predictors,result_frame,results_path,code)
    params_list = [(i,result_frame) for i in predictors]
    # print(param_list)
    roc_cols = [[f"{key}_FPR",f"{key}_TPR"] for key in predictors]
    roc_excel = pd.DataFrame(columns = roc_cols)
    pr_cols = [[f"{key}_Recall",f"{key}_Precsion"] for key in predictors]
    pr_excel = pd.DataFrame(columns = pr_cols)
    result_list = []
    with concurrent.futures.ProcessPoolExecutor() as executor:
        params_list = params_list #<- take out 
        results = executor.map( ROC_wrapper, params_list)
        for i in results:
            (predictor, ROC_AUC,PR_AUC, PR_frame,results_frame) = i
            roc_excel[f"{predictor}_TPR"]=results_frame["TPR"]
            roc_excel[f"{predictor}_FPR"]=results_frame["FPR"]
            pr_excel[f"{predictor}_Precsion"] = PR_frame["Precision"]
            pr_excel[f"{predictor}_Recall"] = PR_frame["Recall"]
            results = (predictor, ROC_AUC,PR_AUC)
            result_list.append(results)
            # return ROC_AUC,PR_AUC,predictor
    return result_list,roc_excel,pr_excel
    
def Run(params):
    (X,y, train,feature_cols,code,results_path,protein ,trees,depth,ccp,viz,data_path,test,print_out,count) = params
    log_results , coefficients = LogReg(feature_cols,X,y,code,results_path,protein,test,print_out)
    totalframe, treeparams = RandomFor(X,y,protein,feature_cols,code,trees,depth,ccp,viz,results_path,data_path,log_results,train,test,print_out)
    # ROC_Star(totalframe,code,count,results_path,feature_cols)
    return totalframe ,treeparams,coefficients

def LogReg(feature_cols,X,y,code,results_path,protein,test,print_out):
        x = sm.add_constant(X)
        logit_model = sm.Logit(y,x)
        result = logit_model.fit(disp=0)
        coefficients = result.params
        # create folder for output data and save the coef in it 
        if print_out == True:
            folder = "{}/META_DPI_RESULTS{}/By_protein/result_{}" .format(results_path,code,protein)
            os.mkdir(folder)
        vals = []
        num = 1
        for pred in feature_cols:
            v1 = X[pred]
            v2 = coefficients[num]
            num += 1
            v3 = v1 * v2
            vals.append(v3)
        sum_pred = sum(vals)
        val = -1 *(coefficients[0] + sum_pred)
        exponent = np.exp(val)
        pval = (1/(1+exponent))
        log_results = test.assign(logreg = pval)
        return log_results , coefficients

def RandomFor(X,y,protein,feature_cols,code,trees,depth,ccp,viz,results_path,data_path,log_results,train,test,print_out):
        
        # X includes the predus, ispred and dockpred score 
        # y is a binary classifier, 0 is non interface 1 is interface 
        X_train = train[feature_cols]
        y_train = train.annotated
        # create the random forest model
        # n_estimators is the number of trees in each forest
        # random_state is a intiger that keeps the randomness in the RF teh same over multiple iterations
        # bootstrap, when false, means all the data in teh training set is used to produce each tree 
        model = RandomForestClassifier(n_estimators = trees, random_state = 0, bootstrap=False, max_depth=depth, ccp_alpha= ccp)
        model.fit(X_train, y_train)
        # save probability score for test set as a list with indeces [noninterface, interface]
        y_prob = model.predict_proba(X)
        # create a new variable with only the inetrface prediction for each residue 
        y_prob_interface = [p[1] for p in y_prob]
        # optional, set a decimal place cutoff, d, for the probability score 
        # d = 4
        # y_prob_intr_dec = [round(prob, d) for prob in y_prob_interface]
        # save the residue and probabilty score of the test set to the same folder as the logistic regresion
        df2 = test.assign(rfscore = y_prob_interface )
        if viz is True:        
            tree = model.estimators_[0]
            depth = tree.get_depth()
        else:
            tree = False  
        treeparams = (X, y, tree,depth)
        totalframe = df2.copy()
        logframe = log_results
        logs = logframe["logreg"]
        totalframe = totalframe.join(logs)
        if print_out == True:
            path="{}/META_DPI_RESULTS{}/By_protein/result_{}/vals{}.csv".format(results_path,code,protein, protein)
            totalframe.to_csv(path,sep=",", index=True, header=True)
        return totalframe ,treeparams 


def ROC_wrapper(params):
    (predictor,df) = params
    # print(predictor)
    predictor , ROC_AUC ,PR_AUC, PR_frame,results_frame = AUCscript.ROC(params)

    return predictor , ROC_AUC ,PR_AUC, PR_frame,results_frame
    
# kwargs should have tuple of form kwargs = (trees,depth, ccp,print_out,param_test,tree_viz,protein_viz) 
# or leave empty for user input
kwargs = (100,10,0,True,False,True,True,False)
if __name__ == '__main__':
    Main(*kwargs)
