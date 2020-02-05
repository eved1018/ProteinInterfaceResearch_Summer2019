#!/usr/bin/perl
#declaration of file names as variables
my $PredUsdir = </Users/mordechaiwalder/Desktop/ProteinInterfaceResearch_Summer2019-E_Edelstein/Data_Files/Logistic_regresion/predus/>;
my $Dbmark_annotateddir = </Users/mordechaiwalder/Desktop/Research_Mordechai/Annotated_Residues/Dbmark_Annotated_Residues>;
my $NOX_annotateddir = </Users/mordechaiwalder/Desktop/Research_Mordechai/Annotated_Residues/NOX_Annotated_Residues>;
#creating file w/ data table of gloabal TPR/FPR values at each threshold
my $ROC_File = </Users/mordechaiwalder/Desktop/Research_Mordechai/Results/ROC_Curves_Results/ROC_Data/PredUs/PredUs.ROC.thresholds.csv>;
if (my $ROC_Data = open $ROC_File, :w) {
  $ROC_Data.print("Threshold", ",", "Global_Dbmark_TPR", ",", "Global_Dbmark_FPR", ",", "Predicted_Total", ",", "Annotated_Total", ",", "Global_NOX_TPR", ",", "Global_NOX_FPR", ",", "Global_Total_TPR", ",", "Global_Total_FPR", "\n");
}
#creating file w/ data table of TPR/FPR values for each protein at the 0 threshold mark
my $Zero_Threshold_File = </Users/mordechaiwalder/Desktop/Research_Mordechai/Results/ROC_Curves_Results/ROC_Data/PredUs/PredUs.ROC.zero_threshold.proteins.csv>;
if (my $Zero_Data = open $Zero_Threshold_File, :w) {
  $Zero_Data.print("Protein", ",", "TP", ",", "Annotated_Residues", ",", "TPR", ",", "FP", ",", "Non-Annotated_Residues", ",", "FPR", "\n");
}
my $Missing_predus = </Users/mordechaiwalder/Desktop/Research_Mordechai/Results/ROC_Curves_Results/ROC_Data/PredUs/PredUs.missing_proteins.csv>;
if (my $missing = open $Missing_predus, :w) {
  $missing.print("Missing Protein", ",", "Database", "\n")
}
#looping through threshold values
for 0.00, 0.00, 0.01 -> $start, $stop, $inc
 {
   my @seq = flat ($start, *+$inc ... $stop);
   for (@seq) -> $threshold {
     #initializing values
     my $TP_Dbmark_sum = 0;
     my $TP_NOX_sum = 0;
     my $FP_Dbmark_sum = 0;
     my $FP_NOX_sum = 0;
     my $Ressum_Dbmark = 0;
     my $Ressum_NOX = 0;
     my $Neg_Dbmark_sum = 0;
     my $Neg_NOX_sum = 0;
     print $threshold;
     print "\n";
     #looping through Dbmark
     for dir($Dbmark_annotateddir) -> $file {
         my @annotatedres;
         my $Dbmark_filename = split('/', $file.IO.path)[7];
         my $Dbmark_protein = split('_', $Dbmark_filename)[0];
         say $Dbmark_protein;
         my $Dbmark_protein_PredUs = "$PredUsdir$Dbmark_protein.predus.csv";
         if ($Dbmark_protein_PredUs.IO.e) {
         for $file.IO.lines -> $line {
           my ($annres_num, $annres) = $line.split('_');
           @annotatedres.push: $annres_num;
         }
         my $N = @annotatedres.elems;
         my @predres;
         my @seqres;
         my $predfile = open $Dbmark_protein_PredUs, :r;
         my $preddata = $predfile.slurp;
           for $preddata.lines -> $prediction {
             my ($predres_num, $predval) = split ',', $prediction;
             @seqres.push: $predres_num;
             if ($predval >= $threshold) {
               @predres.push: $predres_num;
            }
           }
           $predfile.close;
           my @TPres;
          my %lookup = map { $_ => 1 }, @annotatedres;
          for (@predres) -> $res {
             if (%lookup{ $res }) {
             @TPres.push: $res;
             }
           }
           say "My tpres = ", @TPres;
           say "My annotatedres = ", @annotatedres;
           my $pred = @predres.elems;
           my $TP = @TPres.elems;
           my $Seqres = @seqres.elems;
           my $TPR = $TP/$N;
           my $FP = $pred - $TP;
           my $neg = $Seqres - $N;
           my $FPR = $FP/$neg;
           if ($threshold == 0) {
             if (my $Zero_Data = open $Zero_Threshold_File, :a) {
               $Zero_Data.print($Dbmark_protein, ",", $TP, ",", $N, ",", $TPR, ",", $FP, ",", $neg, ",", $FPR, "\n");
             }
           }
         } else {
            if ($threshold == 0) {
           if (my $missing = open $Missing_predus, :a) {
             $missing.print($Dbmark_protein, ",", "DBMark", "\n")
           }
         }
       }
    }
  }
}
