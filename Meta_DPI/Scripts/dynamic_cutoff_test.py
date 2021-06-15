import pandas as pd 
import os 

def Main():
    output_df = pd.DataFrame(columns=["protein","cutoff"])
    folder_der = "/Users/evanedelstein/Downloads/ISPRED_30_protein_data/"
    for filename in os.listdir(folder_der):
        if filename.startswith("."):
            pass
        else:
            protein = filename.split("_")[0]
            surface_res_output  = Find_surface_res(filename,folder_der)
            dyn_cut_output = Dyn_cutoff(surface_res_output)
            output_df = output_df.append({'protein': protein,"cutoff": dyn_cut_output}, ignore_index=True)
    print(output_df)
    output_df.to_csv("/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Meta_DPI/Data/Test_data/dynamic_cutoff.csv")

def Find_surface_res(file_obj,folder):
    with open(f"{folder}{file_obj}","r+") as fo:
        for line in fo:
            if line.startswith(" Surface"):
                surface_res = int(line.split(":")[1])
                return surface_res

    # return surface_res

def Dyn_cutoff(surface_res):
    dyn_cut = 6.1* (surface_res ** 0.3)
    return dyn_cut


Main()
