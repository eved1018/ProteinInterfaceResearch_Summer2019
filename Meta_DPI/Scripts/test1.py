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
final_sort = pd.read_csv("/Users/user/Desktop/Research_Evan/Raji_Summer2019_atom/Meta_DPI/Data/Test_data/final_sort.csv", names=["residue","predus","ispred","dockpred","annotated"])
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
