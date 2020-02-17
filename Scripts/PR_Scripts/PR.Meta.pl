#!/usr/bin/perl
#declaration of file names as variables
my $Dbmark_preddir = </Users/mordechaiwalder/Desktop/Research_Mordechai/Data_Files/Meta/DBMark_sorted/>;
my $NOX_preddir = </Users/mordechaiwalder/Desktop/Research_Mordechai/Data_Files/Meta/NOX_sorted/>;
my $Dbmark_annotateddir = </Users/mordechaiwalder/Desktop/Research_Mordechai/Annotated_Residues/Dbmark_Annotated_Residues>;
my $NOX_annotateddir = </Users/mordechaiwalder/Desktop/Research_Mordechai/Annotated_Residues/NOX_Annotated_Residues>;
#shell('rm ~/Desktop/Research_Mordechai/Annotated_Residues/Dbmark_Annotated_Residues/.DS_Store');
my $PR_File = </Users/mordechaiwalder/Desktop/Research_Mordechai/Results/PR_Curves_Results/PR_Data/Meta/Meta.PR.thresholds.csv>;
if (my $PR_Data = open $PR_File, :w) {
  $PR_Data.print("Threshold", ",", "Global_Dbmark_Precision", ",", "Global_Dbmark_Recall", ",", "Global_NOX_Precision", ",", "Global_NOX_Recall", ",", "Global_Total_Precision", ",", "Global_Total_Recall", "\n");
}
#creating file w/ data table of Precision/Recall values for each protein at the 0 threshold mark
my $Zero_Threshold_File = </Users/mordechaiwalder/Desktop/Research_Mordechai/Results/PR_Curves_Results/PR_Data/Meta/Meta.PR.zero_threshold.proteins.csv>;
if (my $Zero_Data = open $Zero_Threshold_File, :w) {
  $Zero_Data.print("Protein", ",", "TP", ",", "Predicted_Residues", ",", "Annotated_Residues", ",", "Precision", ",", "Recall", "\n");
}
#looping through threshold values
for 0.00, 1.01, 0.01 -> $start, $stop, $inc
 {
   my @seq = flat ($start, *+$inc ... $stop);
   for (@seq) -> $threshold {
     #initializing values
     my $TP_Dbmark_sum = 0;
     my $TP_NOX_sum = 0;
     my $Pred_Dbmark_sum = 0;
     my $Pred_NOX_sum = 0;
     my $Ann_Dbmark_sum = 0;
     my $Ann_NOX_sum = 0;
     print $threshold;
     print "\n";
     #looping through Dbmark
     for dir($Dbmark_annotateddir) -> $file {
         my @annotatedres;
         my $Dbmark_filename = split('/', $file.IO.path)[7];
         my $Dbmark_protein = split('_', $Dbmark_filename)[0];
         say $Dbmark_protein;
         my $Dbmark_protein_meta = "$Dbmark_preddir$Dbmark_protein.meta_sorted.csv";
         for $file.IO.lines -> $line {
           my ($annres_num, $annres) = $line.split('_');
           @annotatedres.push: $annres_num;
         }
         my $N = @annotatedres.elems;
         my @predres;
         my $predfile = open $Dbmark_protein_meta, :r;
         my $preddata = $predfile.slurp;
         for $preddata.lines -> $prediction {
           my ($predres_num, $predval) = split ', ', $prediction;
           if ($predval >= $threshold) {
             @predres.push: $predres_num;
          }
         }
         $predfile.close;
         my @TPres;
  #       say "My predres = ", @predres;
        my %lookup = map { $_ => 1 }, @annotatedres;
        for (@predres) -> $res {
           if (%lookup{ $res }) {
           @TPres.push: $res;
           }
         }
  #       say "My tpres = ", @TPres;
         my $pred = @predres.elems;
         my $TP = @TPres.elems;
         my $Recall = $TP/$N;
         my $Precision = $TP/$pred;
         if ($threshold == 0) {
           if (my $Zero_Data = open $Zero_Threshold_File, :a) {
             $Zero_Data.print($Dbmark_protein, ",", $TP, ",", $pred, ",", $N, ",", $Precision, ",", $Recall, "\n");
           }
         }
         $TP_Dbmark_sum += $TP;
         $Ann_Dbmark_sum += $N;
         $Pred_Dbmark_sum += $pred;
         }
         say "my TP_Dbmark_sum = ", $TP_Dbmark_sum;
         say "my Ann_Dbmark_sum = ", $Ann_Dbmark_sum;
         say "my Pred_Dbmark_sum = ", $Pred_Dbmark_sum;
         my $Global_Dbmark_Precision = $TP_Dbmark_sum/$Pred_Dbmark_sum;
         my $Global_Dbmark_Recall = $TP_Dbmark_sum/$Ann_Dbmark_sum;
         say "my Global_Dbmark_Precision = ", $Global_Dbmark_Precision;
         say "my Global_Dbmark_Recall = ", $Global_Dbmark_Recall;
         for dir($NOX_annotateddir) -> $file {
             my @annotatedres;
             my $NOX_filename = split('/', $file.IO.path)[7];
             my $NOX_protein = split('_', $NOX_filename)[0];
             say $NOX_protein;
             my $NOX_protein_meta = "$NOX_preddir$NOX_protein.meta_sorted.csv";
             for $file.IO.lines -> $line {
               my ($annres_num, $annres) = $line.split('_');
               @annotatedres.push: $annres_num;
             }
             my $N = @annotatedres.elems;
             my @predres;
             my $predfile = open $NOX_protein_meta, :r;
             my $preddata = $predfile.slurp;
             for $preddata.lines -> $prediction {
               my ($predres_num, $predval) = split ', ', $prediction;
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
             my $pred = @predres.elems;
             my $TP = @TPres.elems;
             my $Recall = $TP/$N;
             my $Precision = $TP/$pred;
             if ($threshold == 0) {
               if (my $Zero_Data = open $Zero_Threshold_File, :a) {
                 $Zero_Data.print($NOX_protein, ",", $TP, ",", $pred, ",", $N, ",", $Precision, ",", $Recall, "\n");
               }
             }
             $TP_NOX_sum += $TP;
             $Ann_NOX_sum += $N;
             $Pred_NOX_sum += $pred;
             }
             say "my TP_NOX_sum = ", $TP_NOX_sum;
             say "my Ann_NOX_sum = ", $Ann_NOX_sum;
             say "my Pred_NOX_sum = ", $Pred_NOX_sum;
             my $Global_NOX_Precision = $TP_NOX_sum/$Pred_NOX_sum;
             my $Global_NOX_Recall = $TP_NOX_sum/$Ann_NOX_sum;
             say "my Global_NOX_Precision = ", $Global_NOX_Precision;
             say "my Global_NOX_Recall = ", $Global_NOX_Recall;
             my $TP_Total_sum = $TP_NOX_sum + $TP_Dbmark_sum;
             my $Pred_Total_sum = $Pred_NOX_sum + $Pred_Dbmark_sum;
             my $Ann_Total_sum = $Ann_NOX_sum + $Ann_Dbmark_sum;
             my $Global_Total_Precision = $TP_Total_sum/$Pred_Total_sum;
             my $Global_Total_Recall = $TP_Total_sum/$Ann_Total_sum;
         if (my $PR_Data = open $PR_File, :a) {
         $PR_Data.print($threshold, ",", $Global_Dbmark_Precision, ",", $Global_Dbmark_Recall, ",", $Global_NOX_Precision, ",", $Global_NOX_Recall, ",", $Global_Total_Precision, ",", $Global_Total_Recall, "\n");
         }
    }
}
