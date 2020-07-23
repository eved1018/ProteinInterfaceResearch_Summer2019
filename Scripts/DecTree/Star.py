import pandas as pd
import numpy as np
import os 
import subprocess
import re
import streamlit as st


def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]

def color(val,lower_range):
    if val in lower_range: 
        if val <= 0.05:
            color = 'green'
        else:
            color = 'red'
    else:
        color = "black"
    return 'color: %s' % color



def Star(path):
    # path = "/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/CrossVal_logreg_RF/22train_ant_test/Crossvaltest1/Star"
    pathlist = os.listdir(path)
    pathlist.sort(key=natural_keys)
    for filename in pathlist:
        if filename.startswith("CV"):
            interface = f"{path}/{filename}/StarinterfaceCV.txt"
            non_int = f"{path}/{filename}/StarnoninterfaceCV.txt" 
            cmd ='./star --sort StarinterfaceCV.txt StarnoninterfaceCV.txt 0.05'
            subprocess.call(["cp",interface,"/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Scripts/star-v.1.0/"])
            subprocess.call(["cp",non_int,"/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Scripts/star-v.1.0/"])
            os.chdir("/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Scripts/star-v.1.0")
            subprocess.run(cmd, shell= True)
            data = pd.read_csv("/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Scripts/star-v.1.0/results_sorted.txt",header =1,engine='python',index_col = 0 , sep = '\t')
            pd.set_option('display.float_format', lambda x: '%.5f' % x)
            for col in data.columns:
                data[col] = pd.to_numeric(data[col], errors='coerce')
                data[col] = data[col].replace(np.nan, col , regex=True)
                # data[col] = data[col].round(3)
            values = data.values
        
            lower_triangular = values[np.tril_indices(values.shape[0], -1)]
            st.write(f"{filename}")
            st.dataframe(data.style.applymap(color,lower_range =lower_triangular))
            
            # html = data.style.applymap(color,lower_range =lower_triangular)
            # st.write()
            # html = html.render()
            # text_file = open(f"{path}/{filename}/data.html", "w")
            # text_file.write(html)
            # text_file.close()

        
Star("/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/CrossVal_logreg_RF/22train_ant_test/Crossvaltest1/Star")