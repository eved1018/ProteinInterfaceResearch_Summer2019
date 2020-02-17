#!/usr/bin/perl
#declaration of file names as variables
my $PredUsdir = </Users/mordechaiwalder/Desktop/ProteinInterfaceResearch_Summer2019-E_Edelstein/Data_Files/Logistic_regresion_corrected/predus/>;
my $Dbmark_annotateddir = </Users/mordechaiwalder/Desktop/Research_Mordechai/Annotated_Residues/Dbmark_Annotated_Residues>;
my $NOX_annotateddir = </Users/mordechaiwalder/Desktop/Research_Mordechai/Annotated_Residues/NOX_Annotated_Residues>;
shell('rm ~/Desktop/Research_Mordechai/Annotated_Residues/Dbmark_Annotated_Residues/.DS_Store');
#creating file w/ data table of gloabal TPR/FPR values at each threshold
my $ROC_File = </Users/mordechaiwalder/Desktop/Research_Mordechai/Results/ROC_Curves_Results/ROC_Data/PredUs/PredUs.ROC.thresholds.csv>;
if (my $ROC_Data = open $ROC_File, :w) {
  $ROC_Data.print("Threshold", ",", "Global_Dbmark_TPR", ",", "Global_Dbmark_FPR", ",", "Global_NOX_TPR", ",", "Global_NOX_FPR", ",", "Global_Total_TPR", ",", "Global_Total_FPR", "\n");
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
for 0.00, 1.01, 0.01 -> $start, $stop, $inc
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
    #     say $Dbmark_protein_PredUs;
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
    #      say "My seqres = ", @seqres;
    #      say "My predres = ", @predres;
           my @TPres;
          my %lookup = map { $_ => 1 }, @annotatedres;
          for (@predres) -> $res {
             if (%lookup{ $res }) {
             @TPres.push: $res;
             }
           }
      #     say "My tpres = ", @TPres;
      #     say "My annotatedres = ", @annotatedres;
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
           $TP_Dbmark_sum += $TP;
           $FP_Dbmark_sum += $FP;
           $Ressum_Dbmark += $N;
           $Neg_Dbmark_sum += $neg;
         } else {
            if ($threshold == 0) {
           if (my $missing = open $Missing_predus, :a) {
             $missing.print($Dbmark_protein, ",", "DBMark", "\n")
           }
         }
       }
    }
    my $Seq_Dbmark_sum = $Neg_Dbmark_sum + $Ressum_Dbmark;
    my $Pred_Dbmark_sum = $TP_Dbmark_sum + $FP_Dbmark_sum;
    say "my TP_Dbmark_sum = ", $TP_Dbmark_sum;
    say "my FP_Dbmark_sum = ", $FP_Dbmark_sum;
    say "my Ressum_Dbmark = ", $Ressum_Dbmark;
    say "my Neg_Dbmark_sum = ", $Neg_Dbmark_sum;
    my $Global_Dbmark_TPR = $TP_Dbmark_sum/$Ressum_Dbmark;
    my $Global_Dbmark_FPR = $FP_Dbmark_sum/$Neg_Dbmark_sum;
    say "my Global_Dbmark_TPR = ", $Global_Dbmark_TPR;
    say "my Global_Dbmark_FPR = ", $Global_Dbmark_FPR;
  for dir($NOX_annotateddir) -> $file {
      my @annotatedres;
      my $NOX_filename = split('/', $file.IO.path)[7];
      my $NOX_protein = split('_', $NOX_filename)[0];
      say $NOX_protein;
      my $NOX_protein_PredUs = "$PredUsdir$NOX_protein.predus.csv";
       if ($NOX_protein_PredUs.IO.e) {
      for $file.IO.lines -> $line {
        my ($annres_num, $annres) = $line.split('_');
        @annotatedres.push: $annres_num;
      }
      my $N = @annotatedres.elems;
      my @predres;
      my @seqres;
      my $predfile = open $NOX_protein_PredUs, :r;
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
       $Zero_Data.print($NOX_protein, ",", $TP, ",", $N, ",", $TPR, ",", $FP, ",", $neg, ",", $FPR, "\n");
     }
   }
   $TP_NOX_sum += $TP;
   $FP_NOX_sum += $FP;
   $Ressum_NOX += $N;
   $Neg_NOX_sum += $neg;
  } else {
      if ($threshold == 0) {
     if (my $missing = open $Missing_predus, :a) {
       $missing.print($NOX_protein, ",", "DBMark", "\n")
     }
   }
  }
  }
   my $Seq_NOX_sum = $Neg_NOX_sum + $Ressum_NOX;
   my $Pred_NOX_sum = $TP_NOX_sum + $FP_NOX_sum;
   say "my TP_NOX_sum = ", $TP_NOX_sum;
   say "my FP_NOX_sum = ", $FP_NOX_sum;
   say "my Ressum_NOX = ", $Ressum_NOX;
   say "my Neg_NOX_sum = ", $Neg_NOX_sum;
   my $Global_NOX_TPR = $TP_NOX_sum/$Ressum_NOX;
   my $Global_NOX_FPR = $FP_NOX_sum/$Neg_NOX_sum;
   say "my Global_NOX_TPR = ", $Global_NOX_TPR;
   say "my Global_NOX_FPR = ", $Global_NOX_FPR;
   my $TP_Total_sum = $TP_NOX_sum + $TP_Dbmark_sum;
   my $FP_Total_sum = $FP_NOX_sum + $FP_Dbmark_sum;
   my $Ressum_Total = $Ressum_NOX + $Ressum_Dbmark;
   my $Neg_Total_sum = $Neg_NOX_sum + $Neg_Dbmark_sum;
   my $Global_Total_TPR = $TP_Total_sum/$Ressum_Total;
   my $Global_Total_FPR = $FP_Total_sum/$Neg_Total_sum;
   say "my Global_Total_TPR = ", $Global_Total_TPR;
   say "my Global_Total_FPR = ", $Global_Total_FPR;
  if (my $ROC_Data = open $ROC_File, :a) {
  $ROC_Data.print($threshold, ",", $Global_Dbmark_TPR, ",", $Global_Dbmark_FPR, ",", $Global_NOX_TPR, ",", $Global_NOX_FPR, ",", $Global_Total_TPR, ",", $Global_Total_FPR, "\n");
  }
 }
}