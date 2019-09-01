#!/usr/bin/perl
#
# use the rankings for each residue (allresidue_rank_docking_avg13) 
# and the rankings of all annotated residues (rankings_allres_docking_avg13)
# to calculate the TP, FP, TN,anf FN for wach uery based on the assigned
# cutoff value.  Then calculate teh TPR and FPR and average over all queries.
# #
($#ARGV >0 ) or die "usage: 0<filename containing pdb names><filename containing docking frequency of all residues><filename containing the rankings of annotated residues>";

use strict;
use warnings;

# Specify HOME Directory
#
my $data_dir = "/home/raji/biolip/peptideBinding/nox";
#my $data_dir = "/home/raji/biolip/peptideBinding/dockb/alldockb";
my $results_dir = "/home/raji/biolip/peptideBinding/plos_review/roc";
my %res_rank;
my %int_res_rank;
my $TPR;
my $FPR;
my $query;

if (!-d $results_dir){
  mkdir  "$results_dir";
}
open OUT, ">>$results_dir/rocdata";
foreach (my $ic=0; $ic<=100; $ic++){
$query=0;
my $avg_TPR;
my $avg_FPR;
   my $allpos=0;
   my $allneg=0;
   my $TP=0;
   my $TN=0;
   my $FP=0;
   my $FN=0;
open IN, $ARGV[0];
while(my $line = <IN>){
  chomp($line);
   if ($line !~ "#") {
   my $current_dir = "$data_dir/$line";
   $query++;
   my $line1;
   open IN1, "$current_dir/$ARGV[1]";
   my $total_res = `cat $current_dir/$ARGV[1]|grep -v "-" |wc -l`; 
   my $cutoff = ($ic/100)*$total_res;
   while($line1 = <IN1>){
    chomp $line1;
    my @data;
    @data = split(/\s+|_/, $line1);
    my $res_num = $data[1];
    my $rank= $data[0];
    if ($rank !~ "-" && $rank <= $cutoff) {$allpos++};
    if ($rank !~ "-" && $rank > $cutoff) {$allneg++};
    $res_rank{$res_num} = $rank;
   }  #  finish reading allresidue rank file
   my $line2;
   open IN2, "$current_dir/$ARGV[2]";
   while($line2 = <IN2>){
    chomp $line2;
    my @data2;
    @data2 = split(/\s+|_/, $line2);
    my $res_num2 = $data2[1];
    my $rank2= $data2[0];
    if ($rank2 !~ "-" && $rank2 <= $cutoff) {$TP++};
    if ($rank2 !~ "-" && $rank2 > $cutoff) {$FN++};
     $int_res_rank{$res_num2} = $rank2;
   }  #  finish reading nterface residue rank file
#
}
}  #  finish loop over all pdb files
    $FP = $allpos - $TP;
    $TN = $allneg - $FN;
    $TPR = $TP/($TP + $FN);
    $FPR = $FP/($FP + $TN);
#   $avg_TPR=average(@TPR);
#   $avg_FPR=average(@FPR);
   printf OUT "%-5d %-5d %-5d %-5d %-5d %10.3f %10.3f \n", $ic, $TP, $FP, $FN, $TN, $FPR, $TPR;
} # finish loop over the cutoff values

sub average{
# Find the average value of TPR and FPR
  my @array = @_;
  my $sum;
  foreach (@array){$sum += $_};
  return $sum/@array;
}

