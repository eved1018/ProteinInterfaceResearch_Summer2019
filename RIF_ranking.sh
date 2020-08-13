#!/bin/tcsh
#
set suffix="allres"
set suffix2="gz"
# This script is run after the docking of the receptor and a ligand probe 
# followed by a CSU calculation to identify the interface residues. 
# This script calcualtes the ranking of receptor residues for one ligand probe. 
# Multiple probes can be analyzed in a similar manner and averaged.

# Files needed to run this script:
# queryProbeNames -- queryname.chain_probename.chain
# calcualteBackgroundSuccess -- calculates the number of annotated residues in 
# top 15 if chosen randomly from all the residues of the receptor protein.
# It also calculates the random standard deviation.

# makeModel_allresTable -- uses the residues at the interface returned by CSU 
# and write it out in a specific format for allt he 2000 models per receptor-ligand probe pair.

# interfaceResidueDir is the folder that contain the annotated residues for 
# each receptor.
# pdbDir is the folder that contains the pdb file of the receptor protein.
# scriptDir is the folder where the required codes to run this script can be found.
#
# The interface residues obtained after docking and CSU calculations are stored in 
# "receptorname"/results/models/res_models. These files are zipped and have the suffix allres.gz

set interfaceResidueDir="$HOME/SuperSites/residues"
set pdbDir="$HOME/SuperSites/pdbs"
set scriptDir="$HOME/SuperSites/script"

foreach x (`cat queryProbeNames | grep -v "#"`)
set interfaceResidueFile = `echo $x|cut -f1 -d\_`
set pdbfile = $pdbDir/$interfaceResidueFile
set pdb_res_max = `cat $pdbfile | awk '{if ($1 == "ATOM") print $6}' | tail -1`
set pdb_res_min = `cat $pdbfile | awk '{if ($1 == "ATOM") print $6}' | head -1`
   @ pdb_length = ( $pdb_res_max - $pdb_res_min + 1 )

cd $x
 cat $interfaceResidueDir/$interfaceResidueFile | awk '{print $1"_"$2}' > interfaceResidues
 cd results/models/res_models
   foreach y (`ls *.$suffix.$suffix2`)
    set num_res=`gzip -dc $y|awk '{print $1 $2}'|sort|uniq|wc -l`
   end
#

 #find the residue numbers for each model
  
$scriptDir/makeModel_${suffix}Table.pl > model_${suffix}.table
#
cat model_${suffix}.table  | cut -f2,3 -d':' | sed 's/\-/ /g' | awk '{for(i=1;i<=NF;i++){ printf $i"\t""\n"}}' | sort > redundant_allResidues
cat redundant_allResidues |sort|uniq -c|sort -nr -k1 |awk '{print NR"\t"$2"\t"$1}' > ../../../allresidue_rank_docking
cd ../../..
 $scriptDir/joinFiles allresidue_rank_docking 2 interfaceResidues 1 | sort -g > rankings_allres_docking
set total_res=`cat allresidue_rank_docking|wc -l`
set int_res=`cat interfaceResidues |wc -l`
set dock_int=`cat rankings_allres_docking | awk '{if($1 != "-") print}' | wc -l`
set found = `cat rankings_allres_docking |awk '{if($1 != "-" && $1 <= 15 && $3 > 0) print}' | wc -l`
$scriptDir/calculateBackgroundSuccess.pl $total_res $dock_int >temp
set found_random=`cat temp|awk '{print $1}'`
set random_std=`cat temp|awk '{print $2}'`
#  This script calculates the number of annotated residues in the top15 ranks for each receptor-ligandprobe and compares that with the random prediction and standard deviation.
#
printf "$x\t$pdb_length\t$total_res\t$int_res\t$dock_int\t$found\t$found_random\t$random_std\n" >> ../rank_docking_${suffix}
cd ..
end

