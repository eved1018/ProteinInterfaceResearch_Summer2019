import os 
import sys
import subprocess
import pandas as pd

from pathlib import Path

def Pymol_wrapper():
    path = Path(__file__).parents[2]
    folder = "Images_sphere"
    meta_results = pd.read_csv("/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Meta_DPI/Results/MetaDPIResults/Meta_DPI_results6/Meta_DPI_result.csv")
    ppisp = pd.read_csv(f"{path}/Meta_DPI/Data/Test_data/meta-ppisp-results-comma-new.txt")
    vorfip = pd.read_csv(f"{path}/Meta_DPI/Data/Test_data/vorffip_columns.txt")
    vorfip = vorfip.drop(columns = ['annotated'])
    ppisp = ppisp.drop(columns = ['annotated'])
    results = pd.DataFrame()
    results["residue"] = meta_results["residue"]
    results["logreg"] = meta_results["logreg"]
    results["rfscore"] = meta_results["rfscore"]
    results["dockpred"] = meta_results["dockpred"]
    results["predus"] = meta_results["predus"]
    results["ispred"] = meta_results["ispred"]
    vorfip["residue"] = [i.split("_")[0]+ "_" +i.split("_")[1] for i in vorfip["residue"]]
    results["annotated"] = meta_results["annotated"]
    results = results.merge(vorfip,how="inner", on="residue")
    df = results.merge(ppisp,how="inner", on="residue")
    print(df)
    # data_path = "/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Meta_DPI/Results/MetaDPIResults/Meta_DPI_results6/Meta_DPI_result.csv"
    # df = pd.read_csv(data_path)
    df["protein"] = [x.split('_')[1] for x in df['residue']]
    cutoff_path = "/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Meta_DPI/Data/Test_data/All_protein_cutoffs.csv"
    cutoff_csv = pd.read_csv(cutoff_path)
    proteins= ["1AT3.A","1DE4.E","1BUH.A","1FC2.D"]
    for i in proteins:
        total_script = pml_annotated(i,df,folder)
        pml_maker(i,cutoff_csv, df,folder,total_script)


# 1) fetch protein and run
def pml_maker(protein,cutoff_csv,df,folder,total_script):
    colors = ["red","yellow","blue","olive","orange","brown","violetpurple"]
    predictors = ['predus', "ispred","dockpred","rfscore","logreg","vorffip","meta-ppisp"]
    frame = df[df["protein"] == protein]
    cutoff_row = cutoff_csv[cutoff_csv["Protein"] == protein]
    threshhold = cutoff_row["cutoff res"].values[0]
    for color,predictor in enumerate(predictors):
        predictedframesort = frame.sort_values(by=[predictor], inplace =False, ascending=False)
        thresholdframe = predictedframesort.head(threshhold) 
        predicted_res = thresholdframe.residue.values.tolist()
        predicted_res = [str(i) for i in predicted_res]
        pred_res = [i.split("_")[0] for i in predicted_res]
        protein_name = protein.split(".")[0]
        chain_name = protein.split(".")[1]
        load_file = f"/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Code/PDB_Files/Predus_241_for_real/predus_{protein_name}_{chain_name}.pdb"
        filename = f"/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Meta_DPI/Pymol/{folder}/{protein}/{protein}_{predictor}.png"
        total_script = total_script + f"load {load_file}\ncolor white\n"
        for i in pred_res:
            # script = f"fetch {protein}\nselect toBecolored, resi {i}\ncolor {colors[color]}, toBecolored\n"
            script = f"select toBecolored, resi {i}\ncolor {colors[color]}, toBecolored\n"

            total_script = total_script + script
        total_script = total_script + f"select color {colors[color]}; show spheres,SEL\nset sphere_scale, 0.25, (all)\n"
        # set transparency off all non green to 1 
        total_script = total_script + f"\nremove resn hoh\nzoom complete=1\nset cartoon_transparency, 1\npng {filename},width=900, height=900,ray=1, dpi=500\nquit"
        filename_2 = f"{protein}_{predictor}"
        file_path = f'/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Meta_DPI/Pymol/scripts/{filename_2}.pml'
        with open(file_path, 'w') as f:
            f.write(total_script)
        cmd = f"pymol -cqQ {file_path}"    
        subprocess.run(cmd, shell= True)

def pml_annotated(protein,df,folder):
    frame = df[df["protein"] == protein]
    annotated_frame = frame[frame['annotated'] == 1]
    annotated_res_prot = annotated_frame.residue.tolist()  
    annotated_res = [x.split('_')[0] for x in annotated_res_prot] 
    total_script = f"fetch {protein}\ncolor white\n" #<- add transperency 
    os.mkdir(f"/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Meta_DPI/Pymol/{folder}/{protein}")
    # filename = f"/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Meta_DPI/Pymol/{folder}/{protein}/{protein}_annotated.png"
    for i in annotated_res:
        script = f"select toBecolored, resi {i}\ncolor pink, toBecolored\n"
        total_script = total_script + script
    total_script = total_script + f"select color pink; show spheres, SEL\nset sphere_transparency, 0.5" #<- add less transperency 
    total_script = total_script + f"\nremove resn hoh\nzoom complete=1"
    # total_script = total_script +"\npng {filename},width=900, height=900,ray=1, dpi=500\n"
    return total_script
    # filename = f"{protein}_annotated"
    # file_path = f'/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Meta_DPI/Pymol/scripts/{filename}.pml'
    # with open(file_path, 'w') as f:
    #     f.write(total_script)
    # cmd = f"pymol -cqQ {file_path}"    
    # subprocess.run(cmd, shell= True)



Pymol_wrapper()