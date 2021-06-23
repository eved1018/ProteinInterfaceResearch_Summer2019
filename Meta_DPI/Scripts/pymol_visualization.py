import os 
import sys
import subprocess
import pandas as pd
from pathlib import Path
import sys


def test():
    predictors = ['predus', "ispred","dockpred","rfscore","logreg","vorffip","meta-ppisp"]
    df = pd.read_csv("/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Meta_DPI/Data/Test_data/final_sort_headers_images.csv")
    df.set_index('residue', inplace= True )
    results_path = "/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Meta_DPI/Pymol/images_350dpi"
    code = 1
    Main(predictors,df,results_path,code)


def Main(predictors,df,results_path,code):
    try:
        cmd = f"pymol -c -q -Q " # <- add in location to pymol ex. "~/Application/"
        subprocess.run(cmd, shell= True)

    except:
        print("pymol is not available, it can be downloaded from homebrew using: brew install brewsci/bio/pymol")
        return

    path = Path(__file__).parents[2]
    results_folder = f"{results_path}/Meta_DPI_results{code}/Pymol"
    # results_folder = f"{results_path}/"
    folder = "Images"
    # df = Df_maker(path)
    df = df.reset_index().rename({'index':'residue'}, axis = 'columns')
    df["protein"] = [x.split('_')[1] for x in df.residue]
    proteins = df["protein"].unique()
    cutoff_path = f"{path}/Meta_DPI/Data/Test_data/All_protein_cutoffs.csv"
    cutoff_csv = pd.read_csv(cutoff_path)

    # proteins= ["1ACB.I","1AT3.A","1DE4.E","1BUH.A","1FC2.D"]
    # proteins= ["7CEI.A","1QOR.A","1B34.A"]
    # proteins= ["4XXH.A","2UTG.A","1KXP.D"]
    os.mkdir(f"{results_folder}")
    os.mkdir(f"{results_folder}/{folder}")
    os.mkdir(f"{results_folder}/scripts")
    for protein in proteins:
        os.mkdir(f"{results_folder}/{folder}/{protein}")
        pml_maker(protein,df,cutoff_csv,folder,path,predictors,results_folder)

def Df_maker(path):
    meta_results = pd.read_csv(f"{path}/Meta_DPI/Results/MetaDPIResults/Meta_DPI_results6/Meta_DPI_result.csv")
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
    return df
        
def pml_annotated(protein,df,folder):
    frame = df[df["protein"] == protein]
    annotated_frame = frame[frame['annotated'] == 1]
    annotated_res_prot = annotated_frame.residue.tolist()  
    annotated_res = [x.split('_')[0] for x in annotated_res_prot] 
    annotated_res_list = "+".join(annotated_res)
    return(annotated_res_list)

def pml_predicted(protein,cutoff_csv,df,predictor):
    frame = df[df["protein"] == protein]
    cutoff_row = cutoff_csv[cutoff_csv["Protein"] == protein]
    threshhold = cutoff_row["cutoff res"].values[0]
    predictedframesort = frame.sort_values(by=[predictor], inplace =False, ascending=False)
    thresholdframe = predictedframesort.head(threshhold) 
    predicted_res = thresholdframe.residue.values.tolist()
    predicted_res = [str(i) for i in predicted_res]
    pred_res = [i.split("_")[0] for i in predicted_res]
    pred_res_list = "+".join(pred_res)
    return pred_res_list
    
def image_wrapper(args):
    (path, protein,predictor,folder,protein_name,chain_name,annotated_res_list,pred_res_list,results_folder) = args
    # load_file = f"{path}/Code/PDB_Files/Predus_241_for_real/predus_{protein_name}_{chain_name}.pdb"
    filename = f"{results_folder}/{folder}/{protein}/{protein}_{predictor}.png"
    total_script=f"""delete all 
    fetch {protein_name}.{chain_name}
    color blue 
    set cartoon_transparency,0.75
    select ann, resi {annotated_res_list}
    indicate bycalpha ann
    create annotated, indicate
    select pred, resi {pred_res_list}
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
    bg_color white 
    set ray_opaque_background, 1
    png {filename},width=900, height=900,dpi = 350,ray=1
    quit"""

    filename_2 = f"{protein}_{predictor}"
    file_path = f'{results_folder}/scripts/{filename_2}.pml'
    with open(file_path, 'w') as f:
        f.write(total_script)
    cmd = f"pymol -c -q -Q {file_path}" # <- add in location to pymol ex. "~/Application/"
    subprocess.run(cmd, shell= True)

def pml_maker(protein,df,cutoff_csv,folder,path,predictors,results_folder):
    protein_name = protein.split(".")[0]
    chain_name = protein.split(".")[1]
    # predictors = ['predus', "ispred","dockpred","rfscore","logreg","vorffip","meta-ppisp"]
    for predictor in predictors:
        annotated_res_list = pml_annotated(protein,df,folder)
        pred_res_list= pml_predicted(protein,cutoff_csv,df,predictor)
        args = (path, protein,predictor,folder,protein_name,chain_name,annotated_res_list,pred_res_list,results_folder)
        image_wrapper(args)
        


test()