
import os 
import multiprocessing
import subprocess
from typing import Reversible
import imgkit
import re 
import pandas as pd 
import numpy as np 

# def ROC_Star(data, code,timer,results_path,cols):
#     cols = cols + 'rfscore' +"logreg"
#     data = data.round(3)
#     Star_interface = data[data.annotated == 1] 
#     Star_non_interface = data[data.annotated == 0]
#     Star_interface = Star_interface.drop(columns="annotated")
#     Star_non_interface = Star_non_interface.drop(columns="annotated")
#     # Star_interface = Star_interface.rename(columns={'predus':"T1", 'ispred': "T2", 'dockpred':"T3", 'rfscore':"T4",'logreg': 'T5'})
#     # Star_non_interface =Star_non_interface.rename(columns={'predus':"T1", 'ispred': "T2", 'dockpred':"T3", 'rfscore':"T4",'logreg': 'T5'})
#     for count, pred in enumerate(cols):
#         Star_interface = Star_interface.rename(columns={f"{pred}":f"T{count}"})
#         Star_non_interface = Star_non_interface.rename(columns={f"{pred}":f"T{count}"})
#     os.mkdir("{}Crossvaltest{}/Star/".format(results_path,code))
#     path = "{}Crossvaltest{}/Star/CV{}/StarinterfaceCV.txt".format(results_path,code,timer)
#     Star_interface.to_csv(path,sep="\t", index=False, header=True)
#     path = "{}Crossvaltest{}/Star/CV{}/StarnoninterfaceCV.txt".format(results_path, code,timer)
#     Star_non_interface.to_csv(path,sep="\t", index=False, header=True)

# def Star(results_path,code,Star_path,cols):
#     path = "{}Crossvaltest{}/Star".format(results_path, code)
#     pathlist = os.listdir(path)
#     pathlist.sort(key=natural_keys)
#     for filename in pathlist:
#         if filename.startswith("CV"):
#             interface = f"{path}/{filename}/StarinterfaceCV.txt"
#             non_int = f"{path}/{filename}/StarnoninterfaceCV.txt" 
#             cmd ='./star --sort StarinterfaceCV.txt StarnoninterfaceCV.txt 0.05'
#             subprocess.call(["cp",interface,Star_path])
#             subprocess.call(["cp",non_int,Star_path])
#             os.chdir(Star_path)
#             subprocess.run(cmd, shell= True)
#             data = pd.read_csv("{}results_sorted.txt".format(Star_path),header =1,engine='python',index_col = 0 , sep = '\t')
#             pd.set_option('display.float_format', lambda x: '%.5f' % x)
#             # data = data.rename(columns={'T1':"predus", 'T2': "ispred", 'T3':"dockpred", 'T4':"rfscore",'T5': 'logreg'})
#             for count, pred in enumerate(cols):
#                 data = data.rename(columns={f"T{count}":f"{pred}"})
#             for col in data.columns:
#                 data[col] = pd.to_numeric(data[col], errors='coerce')
#                 data[col] = data[col].replace(np.nan, col , regex=True)
#             # data = data.rename({'T1':"predus", 'T2': "ispred", 'T3':"dockpred", 'T4':"rfscore",'T5': 'logreg'},axis = 'index')
#             for count, pred in enumerate(cols):
#                 data = data.rename(columns={f"T{count}":f"{pred}"},axis='index')
#             values = data.values
#             lower_triangular = values[np.tril_indices(values.shape[0], -1)]
#             html = data.style.applymap(Color,lower_range =lower_triangular)
#             html = html.render()
#             imgkit.from_string(html,'{}Crossvaltest{}/tests/{}/{}.jpg'.format(results_path,code,filename,filename))
            
def Color(val,lower_range):
    if val in lower_range: 
        if val <= 0.05:
            color = 'green'
        else:
            color = 'red'
    else:
        color = "black"
    return 'color: %s' % color  

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]

def Star_Leave_one_out(df,path,results_path,code):
    Star_path = f"{path}/Meta_DPI/Data/star-v.1.0/"
    results_folder = f"{results_path}/Meta_DPI_results{code}"
    df_interface = df[df["annotated"] ==1]
    df_interface_non_interface = df[df["annotated"] == 0 ]
    cols = df_interface.columns.tolist()
    cols.remove('annotated')
    cols.remove('residue')
    df_interface = df_interface.drop(columns = ['residue','annotated'])
    df_interface_non_interface  =df_interface_non_interface.drop(columns = ['residue','annotated'])
    df_interface.to_csv(f"{Star_path}StarinterfaceCV.txt",index= False,sep="\t")
    df_interface_non_interface.to_csv(f"{Star_path}StarnoninterfaceCV.txt",index=False,sep="\t") 
    # interface = f"{folder}/StarnoninterfaceCV.txt"
    # non_int = f"{folder}/StarnoninterfaceCV.txt" 
    cmd ='./star --sort StarinterfaceCV.txt StarnoninterfaceCV.txt 0.05' #<- TODO makesure pval of 0.05 is actually working 
    # cmd =f"./star --sort {interface} {non_int} 0.05"
    # subprocess.call(["cp",interface,Star_path])
    # subprocess.call(["cp",non_int,Star_path])
    os.chdir(Star_path)
    subprocess.run(cmd, shell= True)
    star_file_collecter(Star_path,path,results_folder,code)
    # data = pd.read_csv("{}results_sorted.txt".format(Star_path),header =1,engine='python',index_col = 0 , sep = '\t')
    # # pd.set_option('display.float_format', lambda x: '%.2E' % x)
    
    # for count, pred in enumerate(cols):
    #     data = data.rename(columns={f"T{count}":f"{pred}"})
    # for col in data.columns:
    #     data[col] = pd.to_numeric(data[col], errors='coerce')
    #     data[col] = data[col].replace(np.nan, col , regex=True)
    # for count, pred in enumerate(cols):
    #     # data = data.rename(columns={f"T{count}":f"{pred}"},axis='index')
    #     data = data.rename(columns={f"T{count}":f"{pred}"})
    # values = data.values
    # lower_triangular = values[np.tril_indices(values.shape[0], -1)]
    # html = data.style.applymap(Color,lower_range =lower_triangular)
    # html = html.render()
    # # imgkit.from_string(html,f'{results_path}/Star_{code}.jpg')
    # imgkit.from_string(html,f'{folder}/Star_test_2.jpg')
    # # TODO print out AUC values from AUC_sorted.txt in star folder

def star_file_collecter(Star_path,path,results_folder,code):
    os.chdir(Star_path)
    cmd = "cat auc_sorted.txt >> Star_results.txt" #<- collect all the output files from star and put them in the right place, specificly "results_sorted.txt" and "auc_sorted.txt"
    cmd_2 = "cat results_sorted.txt >> Star_results.txt"
    cm_3 = f"mv Star_results.txt {results_folder}"
    subprocess.run(cmd, shell= True)
    subprocess.run(cmd_2, shell= True)
    subprocess.run(cm_3, shell= True)
    return 


def test_wrapper():
    df =pd.read_csv("/Users/user/Desktop/Research_Evan/Raji_Summer2019_atom/Meta_DPI/Results/MetaDPIResults/Meta_DPI_results6/Meta_DPI_result.csv")
    path = "/Users/user/Desktop/Research_Evan/Raji_Summer2019_atom"
    code = 6    
    results_path = "/Users/user/Desktop/Research_Evan/Raji_Summer2019_atom/Meta_DPI/Results/MetaDPIResults"
    Star_Leave_one_out(df,path,results_path, code)

def meta_methods_comparison():
    Star_path = "/Users/user/Desktop/Research_Evan/MetaDPI/Meta_DPI/Data/star-v.1.0/"
    meta_results = pd.read_csv("/Users/user/Desktop/Research_Evan/Raji_Summer2019_atom/Meta_DPI/Results/MetaDPIResults/Meta_DPI_results6/Meta_DPI_result.csv")
    vorfip = pd.read_csv("/Users/user/Desktop/Research_Evan/Raji_Summer2019_atom/Meta_DPI/Data/Test_data/vorffip_columns.txt")
    ppisp = pd.read_csv("/Users/user/Desktop/Research_Evan/Raji_Summer2019_atom/Meta_DPI/Data/Test_data/meta-ppisp-results-comma-new.txt")
    results = pd.DataFrame()
    results["residue"] = meta_results["residue"]
    results["logreg"] = meta_results["logreg"]
    results["rfscore"] = meta_results["rfscore"]
    results["vorffip"] = vorfip["vorffip"]
    results["meta_ppisp"] = ppisp["meta-ppisp"]
    results["annotated"] = meta_results["annotated"]

    df_interface  = results[results.annotated == 1]
    non_interface = results[results.annotated == 0]

    df_interface = df_interface.drop(columns = ['residue','annotated'])
    non_interface  =non_interface.drop(columns = ['residue','annotated'])
    df_interface.to_csv(f"{Star_path}StarinterfaceCV.txt",index= False,sep="\t")
    non_interface.to_csv(f"{Star_path}StarnoninterfaceCV.txt",index=False,sep="\t") 

    cmd ='./star --sort StarinterfaceCV.txt StarnoninterfaceCV.txt 0.05' #<- TODO makesure pval of 0.05 is actually working 
    os.chdir(Star_path)
    subprocess.run(cmd, shell= True)


    

meta_methods_comparison()


# test_wrapper()
    
# if __name__ == '__main__':
    # Star_Leave_one_out()
    