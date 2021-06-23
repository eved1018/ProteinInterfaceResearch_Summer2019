from datetime import MAXYEAR
from numpy import column_stack, positive
import pandas as pd
from pathlib import Path
# cols = ["x","y","z","a","b"]
# df = pd.read_csv("/Users/evanedelstein/Desktop/PDBtest.csv")
# print(df.columns.tolist())
# if df.columns.tolist() != cols:
#     print("changing cols")
#     df.columns = cols
#     print(df.columns.tolist())
# else:
#     print("all good")

# proteinids = []
#     for resprot in proteinname: 
#         proteinid = resprot.split("_")[1]
#         if proteinid not in proteinids:
#              proteinids.append(proteinid)

# df = pd.read_csv("/Users/evanedelstein/Desktop/PDBtest.csv")
# for i in df.columns.tolist():
#     df = "apple"

# li = ["L","b","c"]
# K = "k"
# tup = [(i,K) for i in li]
# print(tup)
# path = Path(__file__).resolve().parent.parent.parent 
# path2 = Path(__file__).parents[2]
# if path == path2:
#     print("true")
# else:
# #     print("fasle")
# x = 5 
# y = 7
# if x == 5 and y ==7:
#     print("hello")
# df = pd.DataFrame(columns=["A","B"])
# df = df.rename(columns={"A":"C"})
# print(df.head())
# i = 7.8
# print(f"int:{int(i)}\nfloat:{float(i)}\nstring:{str(i)}")
#%%
predictors = ["hello","hi"]
cols = [[f"{key}_FPR",f"{key}_TPR"] for key in predictors]
import itertools
print(list(itertools.chain(*cols)))
# %%
import pandas as pd
df = pd.read_csv("/Users/user/Desktop/Research_Evan/Raji_Summer2019_atom/Meta_DPI/Results/CrossValidation/Crossvaltest2/PR_csv.csv")
cols = df.columns.tolist()
cols.remove()

# %%
li = []
li = [(x,x+1,x+2) for x in range(0,10)]
for i in li:
    (a,b,c) = i 
    print(a)
# %%
import pandas as pd
df = pd.read_csv("/Users/user/Desktop/Research_Evan/Raji_Summer2019_atom/Meta_DPI/Results/CrossValidation/Crossvaltest2/PR_csv.csv")
sortframe = df.sort_values(by=["predus_Recall"], inplace =False, ascending=True)
sortframe.head()
df.head()

# %%
import pandas as pd
df = pd.DataFrame()
df["num"] = [i for i in range(0,20)]
sort = df.sort_values(by=["num"], inplace = False, ascending=False)
head = sort.head(5)
print(len(head.index))

# %%
print(f"new \n line?")
# %%
import pandas as pd
final_sort = pd.read_csv("/Users/user/Des`k`top/Research_Evan/Raji_Summer2019_atom/Meta_DPI/Data/Test_data/final_sort.csv", names=["residue","predus","ispred","dockpred","annotated"])
# final_sort.head()
vorffip_frame = pd.read_csv("/Users/user/Desktop/Research_Evan/Raji_Summer2019_atom/Meta_DPI/Data/Test_data/vorffip_renumbered.txt")
# vorffip_frame.head()
print(f"final sort {final_sort.info()}\nvorffip {vorffip_frame.info()}")
# ann_list = final_sort["annotated"].values.tolist()
# final_proteins =[x.split('_')[1] for x in final_sort.residue]
# final_proteins = set(final_proteins)
# vorffip_proteins = set([x.split('_')[1] for x in vorffip_frame.residue])
# vorffip_proteins = set(vorffip_proteins)
# print(len(vorffip_proteins))
# print(len(final_proteins))
# non_overlap = [i for i in final_proteins if i in vorffip_proteins]
# len(non_overlap)
# print(f"ann len {len(ann_list)}\nvorffip res {len(vorffip_frame["residue"].values.tolist())} ")
# vorffip_frame['annotated'] = final_sort["annotated"]
# vorffip_updated_frame = pd.DataFrame()
# vorffip_updated_frame["residue"] = vorffip_frame["residue"]
# vorffip_updated_frame["vorffip"] = vorffip_frame["vorffip"]
# vorffip_updated_frame["annotated"] = ann_list
# vorffip_updated_frame.head()

# %%
from scipy import stats
import pandas as pd 
x= pd.read_csv("")      
stats.kstest(x, 'norm')


# #%%
# from sklearn.metrics import precision_recall_curve
# import pandas as pd 
# from pathlib import Path
# import matplotlib.pyplot as plt

# def PR(params):
#     predictor,data_path = params
#     path = Path(__file__).parents[2]
#     data_path = f"{path}/Meta_DPI/{data_path}"
#     frame = pd.read_csv(data_path)
#     frame= frame.fillna(method='ffill')
#     y_true = frame["annotated"]
#     y_scores = frame[f"{predictor}"]
#     # print(y_true,y_scores)
#     precision, recall, thresholds = precision_recall_curve(y_true, y_scores)
#     # print(precision, recall, thresholds)
#     pr_frame = pd.DataFrame()
#     pr_frame["precision"] = precision
#     pr_frame["recall"] = recall
#     max = pr_frame["precision"].max()
#     print(max)
#     plt.plot(recall,precision,label=f"{predictor}")
#     plt.legend()    

# params = [("rfscore","Results/MetaDPIResults/Meta_DPI_results6/Meta_DPI_result.csv"),("logreg","Results/MetaDPIResults/Meta_DPI_results6/Meta_DPI_result.csv"),("vorffip","Data/Test_data/vorffip_columns.txt"),("meta-ppisp","Data/Test_data/meta-ppisp-results-comma-new.txt")]
# for i in params:
#     PR(i)
# %%
from sklearn.metrics import precision_recall_curve
import pandas as pd 
from pathlib import Path
import matplotlib.pyplot as plt

def PR(params):
    predictor,data_path = params
    path = Path(__file__).parents[2]
    data_path = f"{path}/Meta_DPI/{data_path}"
    frame = pd.read_csv(data_path)
    frame= frame.fillna(method='ffill')
    y_true = frame["annotated"]
    y_scores = frame[f"{predictor}"]
    # print(y_true,y_scores)
    precision, recall, thresholds = precision_recall_curve(y_true, y_scores)
    # print(precision, recall, thresholds)
    pr_frame = pd.DataFrame()
    pr_frame["precision"] = precision
    pr_frame["recall"] = recall
    pr_frame = pr_frame[pr_frame.precision != 1]
    max = pr_frame["precision"].idxmax()
    pr_frame= pr_frame.head(max)
    pr_excel[f"{predictor}_Precsion"] = pr_frame["precision"]
    pr_excel[f"{predictor}_Recall"] = pr_frame["recall"]
    plt.plot(pr_frame["recall"] ,pr_frame["precision"],label=f"{predictor}")
    plt.legend()

pr_excel = pd.DataFrame()
params = [("rfscore","Results/MetaDPIResults/Meta_DPI_results6/Meta_DPI_result.csv"),("logreg","Results/MetaDPIResults/Meta_DPI_results6/Meta_DPI_result.csv"),("vorffip","Data/Test_data/vorffip_columns.txt"),("meta-ppisp","Data/Test_data/meta-ppisp-results-comma-new.txt")]
for i in params:
    PR(i)
pr_excel.to_csv("/Users/user/Desktop/Research_Evan/Raji_Summer2019_atom/Meta_DPI/Results/MetaDPIResults/Meta_DPI_Results7/PR_baseline.csv")

# %%
import pandas as pd 
from pathlib import Path
import os 
import subprocess

path = Path(__file__).parents[2]
Star_path = "/Users/user/Desktop/Research_Evan/MetaDPI/Meta_DPI/Data/star-v.1.0/"
meta_results = pd.read_csv("/Users/user/Desktop/Research_Evan/Raji_Summer2019_atom/Meta_DPI/Results/MetaDPIResults/Meta_DPI_results6/Meta_DPI_result.csv")
ppisp = pd.read_csv(f"{path}/Meta_DPI/Data/Test_data/meta-ppisp-results-comma-new.txt")
vorfip = pd.read_csv(f"{path}/Meta_DPI/Data/Test_data/vorffip_columns.txt")
vorfip = vorfip.drop(columns = ['annotated'])
ppisp = ppisp.drop(columns = ['annotated'])

results = pd.DataFrame()
results["residue"] = meta_results["residue"]
results["logreg"] = meta_results["logreg"]
results["rfscore"] = meta_results["rfscore"]
vorfip["residue"] = [i.split("_")[0]+ "_" +i.split("_")[1] for i in vorfip["residue"]]
results["annotated"] = meta_results["annotated"]
results = results.merge(vorfip,how="inner", on="residue")
results = results.merge(ppisp,how="inner", on="residue")
print(results)
results["protein"] = [x.split('_')[1] for x in results['residue']]
proteins = results["protein"].unique()
proteins = proteins[0:50]

results = results[results["protein"].isin(proteins)]
print(results)
df_interface  = results[results.annotated == 1]
non_interface = results[results.annotated == 0]
df_interface = df_interface.drop(columns = ['residue','annotated','protein'])
non_interface  =non_interface.drop(columns = ['residue','annotated','protein'])
# print(df_interface)
df_interface.to_csv(f"{Star_path}StarinterfaceCV.txt",index= False,sep="\t")
non_interface.to_csv(f"{Star_path}StarnoninterfaceCV.txt",index=False,sep="\t") 
print("made")
cmd ='./star --sort StarinterfaceCV.txt StarnoninterfaceCV.txt 0.05' #<- TODO makesure pval of 0.05 is actually working 
os.chdir(Star_path)
subprocess.run(cmd, shell= True)
print("done")

# %%
params = [("rfscore","Results/MetaDPIResults/Meta_DPI_results6/Meta_DPI_result.csv")]
from sklearn.metrics import precision_recall_curve
import pandas as pd 
from pathlib import Path
import matplotlib.pyplot as plt

def PR(params):
    predictor,data_path = params
    path = Path(__file__).parents[2]
    data_path = f"{path}/Meta_DPI/{data_path}"
    frame = pd.read_csv(data_path)
    frame= frame.fillna(method='ffill')
    y_true = frame["annotated"]
    y_scores = frame[f"{predictor}"]
    # print(y_true,y_scores)
    precision, recall, thresholds = precision_recall_curve(y_true, y_scores)
    # print(precision, recall, thresholds)
    pr_frame = pd.DataFrame()
    pr_frame["precision"] = precision
    pr_frame["recall"] = recall
    pr_frame = pr_frame[pr_frame.precision != 1]
    max = pr_frame["precision"].max()
    print(max)
for i in params:
    PR(i)
# %%
import pandas as pd 

l = [10,11,12,13,9,8,7]
m = [45,46,47,48,49,50,40]
df = pd.DataFrame()
df["low"] = l 
df["high"] = m 
max =df.low.idxmax()
df = df.head(max+1)
df
# df[f"{i}"]loc[2,:]
# %%

li = [0,1,2,3,4,5]
print(li[0:2])

# %%
import pandas as pd
import numpy as np 
import scipy.stats as ss

f_scores = pd.read_excel("/Users/user/Desktop/Research_Evan/Raji_Summer2019_atom/Notes/Spring2021/Fscore_results.xlsx")
mcc  = pd.read_excel("/Users/user/Desktop/Research_Evan/Raji_Summer2019_atom/Notes/Spring2021/MCC_results.xlsx")
predus = f_scores.predus
ispred = f_scores.ispred
dockpred = f_scores.dockpred 
rfscore = f_scores.rfscore
logreg = f_scores.logreg

df = f_scores
ind = ["meta-ppisp", "vorffip"]

# stats -> largest dist , pval > 0.05 we accept the HA ie are sig. dif. 
for i in ind:
    ks_test = ss.ks_2samp(df[f"{i}"], logreg)
    print(i,ks_test[1])

# # CI 95%
# df = f_scores
# # preds = ["predus","ispred","dockpred","rfscore","logreg"]
# preds = ["vorffip","meta-ppisp"]
# for i in preds:
#     mean = df[f"{i}"].mean()
#     stderr = df[f"{i}"].std()/(len(df[f"{i}"])**0.5)
#     upper = (ss.norm.ppf(0.975) * stderr )+ mean
#     lower = mean + (ss.norm.ppf(0.025) * stderr )
#     print(i,f"[{upper:.3f}:{lower:.3f}]")




# %%
import pandas as pd
df = pd.DataFrame(columns=["a","b"])
df =df.append({"a":1,"b":2},ignore_index=True)
print(df)

# %%
import pandas as pd 
df = pd.read_excel("/Users/evanedelstein/Desktop/prcurve.xlsx")
preds = ["rfscore", "logreg", "vorffip","meta-ppisp"]
for k in preds:
    # PR_frame = df.columns[df.columns.str.startswith(k)]
    distance = df[f"{k}_Recall"].diff()
    midpoint  = df[f"{k}_Precsion"].rolling(2).sum()
    distance = distance * -1
    PR_AUC = (distance) * (midpoint)
    PR_AUC = PR_AUC/2
    sum_AUC = PR_AUC.sum()
    PR_AUC = sum_AUC
    print(k, PR_AUC)
# %%
import pymol

# %%
h= "hello"
g = "goodbye"
f = h+g 
f
# %%
import os 
folder_der = "/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Code/PDB_Files/Predus_241_for_real"
for filename in os.listdir(folder_der):
    if filename.startswith("predus"): 
        # print(filename)
        old = f'{folder_der}/{filename}'
        new_name = filename.split("_")[1]
        chain = filename.split("_")[2]
        chain = chain.split(".")[0]
        new_name = new_name.split(".")[0]
        new_name = new_name.upper()
        new_name  = "predus_" + new_name + "_" + chain + ".pdb"
        new = f'{folder_der}/{new_name}'
        print(new_name)
        os.rename(old, new)
# %%
total_script=f"""delete all 
        load {load_file}
        color blue 
        set cartoon_transparency,0.75
        select ann, resi {annotated_res_list}
        indicate bycalpha ann
        create annotated, indicate
        select pred, resi {resi}
        indicate bycalpha pred
        create pred_res, indicate
        show sphere, annotated
        color pink, annotated
        set sphere_transparency, 0.5,annotated
        show sphere, pred_res
        set sphere_scale,0.5,pred_res
        color green, pred_res
        set sphere_transparency,0,pred_res
        set cartoon_transparency,1,pred_res
        remove resn hoh
        zoom complete=1
        set ray_opaque_background, 1
        set ray_trace_mode, 3;
        png {filename},width=900, height=900,ray=1
        quit"""


#%%
dic ={}
key = "key"
val = "val"
dic[val] =key 
dic[val]
# %%
import pandas as pd 
from pathlib import Path


# filename ="/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Meta_DPI/Data/Test_data/PDBtest.csv"
filename = "/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Meta_DPI/Data/Test_data/final_sort_headers.csv"
df = pd.read_csv(filename)

df.columns =['index','residue', 'predus', 'ispred', 'dockpred',"annotated"]
df = df.drop(["index"], axis=1)
df.to_csv("/Users/evanedelstein/Desktop/Research_Evan/MetaDPI/Meta_DPI/Data/Test_data/final_sort_headers.csv")
print("done")
# %%
import os.path
from pathlib import Path
path = Path(__file__).parents[2]

file_exists = False
while file_exists is False:
    data_filename = input("file name of predictor csv with columns first column as res_proterin and last columns whetehr teh residue is annotated(1:yes, 0:no):  ")
    data_path = f"{path}/Meta_DPI/Data/Test_data/final_sort_headers.csv" if data_filename == "test" else f"{path}/Meta_DPI/Data/Test_data/{data_filename}"
    file_exists = os.path.isfile(data_path)
print("done")
# %%
def fun(**kwagrs):
    if len(kwagrs)==0:
        print("no args")
    else:
        print(kwagrs)
fun(1,2,3)


# %%
t = "h.e.l.l.o"
print(".".join(t.split(".")[1:]))



# %%
import pandas as pd 
from pathlib import Path
path = "/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom"
filename = "/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Meta_DPI/Results/MetaDPIResults/Meta_DPI_results3/Meta_DPI_result.csv"
df = pd.read_csv(filename)
meta_results = pd.read_csv(filename)
ppisp = pd.read_csv(f"{path}/Meta_DPI/Data/Test_data/meta-ppisp-results-comma-new.txt")
vorfip = pd.read_csv(f"{path}/Meta_DPI/Data/Test_data/vorffip_columns.txt")
vorfip = vorfip.drop(columns = ['annotated'])
ppisp = ppisp.drop(columns = ['annotated'])

results = pd.DataFrame()
results["residue"] = meta_results["residue"]
results["logreg"] = meta_results["logreg"]
results["predus"] = meta_results["predus"]
results["ispred"] = meta_results["ispred"]
results["dockpred"] = meta_results["dockpred"]
results["rfscore"] = meta_results["rfscore"]
vorfip["residue"] = [i.split("_")[0]+ "_" +i.split("_")[1] for i in vorfip["residue"]]
results["annotated"] = meta_results["annotated"]
results = results.merge(vorfip,how="inner", on="residue")
results = results.merge(ppisp,how="inner", on="residue")
print(results)
# df = df.drop(columns=['Unnamed:'])
results["protein"] = [x.split('_')[1] for x in results.residue]
proteins = results["protein"].unique()
# print(proteins)
df_1 = results[results.protein == "1FC2.D"]
df_2 = results[results.protein == "1BUH.A"]


# print(df_2)
df_3 = df_1.append(df_2,ignore_index=True)

df_3.drop(columns=["protein"],inplace=True)
print(df_3)
df_3.to_csv("/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Meta_DPI/Data/Test_data/final_sort_headers_images.csv")

# %%
