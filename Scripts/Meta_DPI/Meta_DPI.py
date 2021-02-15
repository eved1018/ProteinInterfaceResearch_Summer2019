import pandas as pd
import numpy as np
import os 
import time 
import statsmodels.api as sm
from sklearn.ensemble import RandomForestClassifier
import concurrent.futures
import multiprocessing


def Main():
    start = time.perf_counter()
    code = 1
    trees = 100
    depth  = 10 
    ccp = 0.0000400902332
    viz = False 
    # set col names
    col_names = ['residue', 'predus', 'ispred', 'dockpred', 'annotated']

    # which columns to look at (ie which dependent variables to use)
    var_col_names =['predus', 'ispred', 'dockpred']
    # change to where u need it to to go 
    results_path = "/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Meta_DPI"
    
    data_path = "/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/final_sort.csv"
    # data_path = "/Users/evanedelstein/Desktop/PDBtest.csv"
    folder = "{}/META_DPI_RESULTS{}" .format(results_path,code)
    while os.path.isdir(folder) is True:
        code = code + 1 
        folder = "{}/META_DPI_RESULTS{}" .format(results_path,code)


    Meta_DPI(data_path,viz, code, trees, depth, ccp, start,results_path,col_names,var_col_names)
    finish = time.perf_counter()
    print(f"finished in {round((finish - start)/60,2 )} minutes(s)")


def Meta_DPI(data_path,viz, code, trees, depth, ccp, start,results_path,col_names,var_col_names):
    folder = "{}/META_DPI_RESULTS{}" .format(results_path,code)
    os.mkdir(folder)
    folder = "{}/META_DPI_RESULTS{}/tests" .format(results_path,code)
    os.mkdir(folder)
    os.mkdir( "{}/META_DPI_RESULTS{}/Trees".format(results_path,code))
    # set up DataFrame 
    # col_names = ['residue', 'predus', 'ispred', 'dockpred', 'annotated']
    # load dataset which is a csv file containing all the residues in Nox and Benchmark as well as predus, ispred, and dockpred scores. 
    # The last column is a binary annotated classifier, 0 is noninetrface 1 is interface. 
    df = pd.read_csv("{}".format(data_path), header=None, names=col_names)
    # df = pd.read_csv("/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Antogen/predictionvalue/res_pred/test.csv", header=0)
    # set the residue_protein ID as the index of the DataFrame 
    df["protein"] = [x.split('_')[1] for x in df['residue']]
    proteins = df["protein"].unique()
    df.set_index('residue', inplace= True )
    # remove any null or missing data from the dataset
    df.isnull().any()
    data = df.fillna(method='ffill')
    data = data[data['annotated'] != "ERROR"]
    data["annotated"] = pd.to_numeric(data["annotated"])

    param_list = []
    cpus = multiprocessing.cpu_count()
    print("starting parellel \n number of cpus {}".format(cpus))

    for protein in proteins:
        test = data[data["protein"] == protein] 
        train = data[data["protein"] != protein] 
        col_namestest = var_col_names + ["annotated"]
        test = test[col_namestest]
        feature_cols = var_col_names
        # Features, ie prediction scores from predus, ispred and dockpred 
        X = test[feature_cols] 
        # Target variable, noninterface or interface 
        y = test.annotated
        params = (X,y, train,feature_cols,code,results_path,protein ,trees,depth,ccp,viz,data_path,test )
        param_list.append(params)
    frames =[]
    with concurrent.futures.ProcessPoolExecutor() as executor:
            param_list = param_list
            results = executor.map( Run, param_list)
            for i in results:
                (totalframe ,treeparams,coefficients) = i
                frames.append(totalframe)
    result_frame = pd.concat(frames)
    result_frame.to_csv("{}/META_DPI_RESULTS{}/Meta_DPI_result.csv" .format(results_path,code))

                

    
def Run(params):
    (X,y, train,feature_cols,code,results_path,protein ,trees,depth,ccp,viz,data_path,test ) = params
    log_results , coefficients = LogReg(feature_cols,X,y,code,results_path,protein,test )
    totalframe, treeparams = RandomFor(X,y,protein,feature_cols,code,trees,depth,ccp,viz,results_path,data_path,log_results,train,test)
    return totalframe ,treeparams,coefficients

def LogReg(feature_cols,X,y,code,results_path,protein,test):
        x = sm.add_constant(X)
        logit_model = sm.Logit(y,x)
        result = logit_model.fit()
        coefficients = result.params
        # create folder for output data and save the coef in it 
        folder = "{}/META_DPI_RESULTS{}/tests/result_{}" .format(results_path,code,protein)
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


def RandomFor(X,y,protein,feature_cols,code,trees,depth,ccp,viz,results_path,data_path,log_results,train,test):
        
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
            # for i in range(0,100):
            #     tree = model.estimators_[i]
            #     print(tree.get_depth())
            tree = model.estimators_[0]
        else:
            tree = False  
        treeparams = (X, y, tree)
        totalframe = df2.copy()
        logframe = log_results
        logs = logframe["logreg"]
        totalframe = totalframe.join(logs)
        path="{}/META_DPI_RESULTS{}/tests/result_{}/vals{}.csv".format(results_path,code,protein, protein)
        totalframe.to_csv(path,sep=",", index=True, header=True)
        return totalframe ,treeparams 



if __name__ == '__main__':
    Main()