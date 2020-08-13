#!/bin/tcsh
#
set suffix="allres"
set interfaceResidueDir="$HOME/SuperSites/residues"
set pdbDir="$HOME/SuperSites/pdbs"
set scriptDir="$HOME/SuperSites/script"

foreach x (`cat queryNames|grep -v "#"`)
set interfaceResidueFile = `echo $x`
set pdbfile = $pdbDir/$interfaceResidueFile
set pdb_res_max = `cat $pdbfile | awk '{if ($1 == "ATOM") print $6}' | tail -1`
set pdb_res_min = `cat $pdbfile | awk '{if ($1 == "ATOM") print $6}' | head -1`
   @ pdb_length = ( $pdb_res_max - $pdb_res_min + 1 )
  set iprobe=0
  mkdir -p $x
  cd $x
  cat $interfaceResidueDir/$interfaceResidueFile | awk '{print $1"_"$2}' > interfaceResidues
  cd ..
  foreach y (`cat probeNames`)
  set iprobe=`expr $iprobe + 1`
  cd $x"_"$y
  cd results/models/res_models
  
  #find the residue numbers for each model
  $scriptDir/makeModel_${suffix}Table.pl > model_${suffix}.table
  
  cat model_${suffix}.table  | cut -f2,3 -d':' | sed 's/\-/ /g' | awk '{for(i=1;i<=NF;i++){ printf $i"\t""\n"}}' | sort >> ../../../../$x/redundant_allResidues
  cat model_${suffix}.table  | cut -f2,3 -d':' | sed 's/\-/ /g' | awk '{for(i=1;i<=NF;i++){ printf $i"\t""\n"}}' | sort >> ../../../../$x/redundant_"$iprobe"_allResidues
  cd ../../../../$x
  cat redundant_allResidues |sort|uniq -c|sort -nr -k1 |awk '{print NR"\t"$2"\t"$1}' > allresidue_rank_docking_avg$iprobe
  $scriptDir/joinFiles allresidue_rank_docking_avg$iprobe 2 interfaceResidues 1 | sort -g > rankings_allres_docking_avg$iprobe
  set total_res_$iprobe=`cat allresidue_rank_docking_avg$iprobe|wc -l`
  set int_res_$iprobe=`cat interfaceResidues |wc -l`
  set dock_int_$iprobe=`cat rankings_allres_docking_avg$iprobe | awk '{if($1 != "-") print}' | wc -l`
  set found_$iprobe = `cat rankings_allres_docking_avg$iprobe |awk '{if($1 != "-" && $1 <= 15 && $3 > 0) print}' | wc -l`
  set Ntot=`cat interfaceResidues |wc -l`
  set TP=`cat rankings_allres_docking_avg$iprobe |awk -v myvar="$Ntot" '{if($1 != "-" && $1 <= myvar && $3 > 0) print}' | wc -l`
  set Fscore_$iprobe=`printf "${TP} ${Ntot}" | awk '{print $1/$2}'`
  cat redundant_"$iprobe"_allResidues |sort|uniq -c|sort -nr -k1 |awk '{print NR"\t"$2"\t"$1}' > allresidue_rank_docking_each_$iprobe
  $scriptDir/joinFiles allresidue_rank_docking_each_$iprobe 2 interfaceResidues 1 | sort -g > rankings_allres_docking_each_$iprobe
  set total_res_each=`cat allresidue_rank_docking_each_$iprobe|wc -l`
  set int_res_each=`cat interfaceResidues |wc -l`
  set dock_int_each=`cat rankings_allres_docking_each_$iprobe | awk '{if($1 != "-") print}' | wc -l`
  set found_each = `cat rankings_allres_docking_each_$iprobe |awk '{if($1 != "-" && $1 <= 15 && $3 > 0) print}' | wc -l`
$scriptDir/calculateBackgroundSuccess.pl $total_res_each $dock_int_each >temp
set found_random=`cat temp|awk '{print $1}'`
set random_std=`cat temp|awk '{print $2}'`
set z=`printf "${found_each} ${found_random}" | awk '{print $1 - $2}'`
set zscore_$iprobe=`printf "$z $random_std" |awk '{print $1 / $2}'`
set total_res_each_$iprobe=$total_res_each
set dock_int_each_$iprobe=$dock_int_each
set found_each_$iprobe=$found_each
set int_res_each_$iprobe=$int_res_each
cd ..
 end
rm $x/redundant_*allResidues
  $scriptDir/calculateBackgroundSuccess.pl $total_res_13 $dock_int_13 >temp
set found_random=`cat temp|awk '{print $1}'`
set random_std=`cat temp|awk '{print $2}'`
set z=`printf "${found_13} ${found_random}" | awk '{print $1 - $2}'`
set zscore_avg13=`printf "$z $random_std" |awk '{print $1 / $2}'`
set Ntot_avg13=`cat $x/interfaceResidues |wc -l`
set TP_avg13 = `cat $x/rankings_allres_docking_avg13 |awk -v var="$Ntot_avg13" '{if($1 != "-" && $1 <= var && $3 > 0) print}' | wc -l`
set Fscore_avg13=`printf "${TP_avg13} ${Ntot_avg13}" | awk '{print $1/$2}'`
mkdir -p stats
printf "$x\t$int_res_6\t$dock_int_13\t$found_1\t$found_2\t$found_3\t$found_4\t$found_5\t$found_6\t$found_7\t$found_8\t$found_9\t$found_10\t$found_11\t$found_12\t$found_13\t$found_random\t$random_std\t$zscore_avg13\t$Fscore_avg13\n" >> stats/found_avgprobes_$suffix
printf "$x\t$zscore_1\t$zscore_2\t$zscore_3\t$zscore_4\t$zscore_5\t$zscore_6\t$zscore_7\t$zscore_8\t$zscore_9\t$zscore_10\t$zscore_11\t$zscore_12\t$zscore_13\n" >> stats/zscore_$suffix
printf "$x\t$Fscore_1\t$Fscore_2\t$Fscore_3\t$Fscore_4\t$Fscore_5\t$Fscore_6\t$Fscore_7\t$Fscore_8\t$Fscore_9\t$Fscore_10\t$Fscore_11\t$Fscore_12\t$Fscore_13\n" >> stats/Fscore_$suffix
printf "$x\t$int_res_each_6\t$dock_int_each_1\t$dock_int_each_6\t$found_each_1\t$found_each_2\t$found_each_3\t$found_each_4\t$found_each_5\t$found_each_6\t$found_each_7\t$found_each_8\t$found_each_9\t$found_each_10\t$found_each_11\t$found_each_12\t$found_13\t$found_random\t$random_std\n" >> stats/found_eachprobe_$suffix
end
