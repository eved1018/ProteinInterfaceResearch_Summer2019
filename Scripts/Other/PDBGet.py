
import subprocess

# we use pdb-tools to get pdb files from list of pdb ids, if id contains chain only that chain is dowloaded 
 
def pdb_get():
    proteinfile = "/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Antogen/Antigen_300/proteins.txt"
    with open(proteinfile) as f:
        pdbs= f.read().splitlines()
        
    path = "/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Antogen/Antigen_300/antigen_list_test/"
    for pdb in pdbs:
        if len(pdb) == 4:
            cmd = f"pdb_fetch {pdb} > {path}{pdb}.pdb "
            subprocess.run(cmd, shell= True)
            
            
        else:
            ids = pdb.split("_")
            pdb =ids[0]
            chain = ids[1]
            
            cmd = f"pdb_fetch {pdb} > {path}{pdb}.pdb "
            cmd2 = f"pdb_selchain -{chain} {path}{pdb}.pdb > {path}{pdb}_{chain}.pdb"
            cmd3 = f"rm {path}{pdb}.pdb"
            subprocess.run(cmd, shell= True)
            subprocess.run(cmd2, shell= True)
            subprocess.run(cmd3, shell= True)
            
            
            
pdb_get()