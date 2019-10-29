#!/usr/bin/perl
#declaration of file names as variables
my $preddir = </Users/mordechaiwalder/Desktop/Research_Mordechai/Data_Files/ISPRED/ISPRED_DBMark_data_sorted/>;
my $Dbmark_annotateddir = </Users/mordechaiwalder/Desktop/Research_Mordechai/Annotated_Residues/Dbmark_Annotated_Residues>;
my $NOX_annotateddir = </Users/mordechaiwalder/Desktop/Research_Mordechai/Annotated_Residues/NOX_Annotated_Residues>;
#creating data table file
my $F_Score_File = </Users/mordechaiwalder/Desktop/Research_Mordechai/Results/Fscores_Results/Ispred.Fscores.csv>;
#creating arrays for calculations
my $TP_DBmark_sum = 0;
my $TP_NOX_sum = 0;
my $Ressum_DBmark = 0;
my $Ressum_NOX = 0;
my @F_Score_DBmark;
my @F_Score_NOX;
if (my $F_Score_Data = open $F_Score_File, :w) {
  $F_Score_Data.print("DBmark_proteins", ",", "TP", ",", "Interface_residues", ",","F_Score", "\n");
}
#looping through annotated residue files
for dir($Dbmark_annotateddir) -> $file {
    my @annotatedres;
    my $Dbmark_filename = split('/', $file.IO.path)[7];
    my $Dbmark_protein = split('_', $Dbmark_filename)[0];
    say $Dbmark_protein;
    my $Dbmark_protein_ispred = "$preddir$Dbmark_protein.ispred_sorted";
    for $file.IO.lines -> $line {
      my ($annres_num, $annres) = $line.split('_');
      @annotatedres.push: $annres_num;
    }
    my $N = @annotatedres.elems;
    my @predres;
    my $predfile = open $Dbmark_protein_ispred, :r;
    my $preddata = $predfile.slurp;
    for $preddata.lines($N) -> $prediction {
      my ($predres_num, $predres) = $prediction.split(' ');
      @predres.push: $predres_num;
    }
    $predfile.close;
    my @TPres;
    for (@predres) -> $res {
      if (grep(/$res/, @annotatedres)) {
      @TPres.push: $res;
      }
    }
    my $TP = @TPres.elems;
    my $F_Score = ($TP/$N);
    say $F_Score;
    if (my $F_Score_Data = open $F_Score_File, :a) {
      $F_Score_Data.print($Dbmark_protein, ",", $TP, ",", $N, ",", $F_Score, "\n");
    }
    @F_Score_DBmark.push: $F_Score;
    $TP_DBmark_sum += $TP;
    $Ressum_DBmark += $N;
}

if ($F_Score_Data = open $F_Score_File, :a) {
  $F_Score_Data.print("NOX_proteins", ",", "TP", ",", "Interface_residues", ",","F_Score", "\n");
}
for dir($NOX_annotateddir) -> $file {
    my @annotatedres;
    my $NOX_filename = split('/', $file.IO.path)[7];
    my $NOX_protein = split('_', $NOX_filename)[0];
    say $NOX_protein;
    my $NOX_protein_ispred = "$preddir$NOX_protein.ispred_sorted";
    for $file.IO.lines -> $line {
      my ($annres_num, $annres) = $line.split('_');
      @annotatedres.push: $annres_num;
    }
    my $N = @annotatedres.elems;
    my @predres;
    my $predfile = open $NOX_protein_ispred, :r;
    my $preddata = $predfile.slurp;
    for $preddata.lines($N) -> $prediction {
      my ($predres_num, $predres) = $prediction.split(' ');
      @predres.push: $predres_num;
    }
    $predfile.close;
    my @TPres;
    for (@annotatedres) -> $res {
      if (grep(/$res/, @predres)) {
      @TPres.push: $res;
      }
    }
    my $TP = @TPres.elems;
    my $F_Score = ($TP/$N);
    say $F_Score;
    if (my $F_Score_Data = open $F_Score_File, :a) {
      $F_Score_Data.print($NOX_protein, ",", $TP, ",", $N, ",", $F_Score, "\n");
    }
    @F_Score_NOX.push: $F_Score;
    $TP_NOX_sum += $TP;
    $Ressum_NOX += $N;
}
my $TP_Total = $TP_DBmark_sum + $TP_NOX_sum;
my $ResTotal = $Ressum_DBmark + $Ressum_NOX;
my $DBmark_F_Score = $TP_DBmark_sum/$Ressum_DBmark;
my $NOX_F_Score = $TP_NOX_sum/$Ressum_NOX;
my $F_Score_Total = $TP_Total/$ResTotal;
say $TP_Total;
say $ResTotal;
say $DBmark_F_Score;
say $NOX_F_Score;
say $F_Score_Total;
my $F_Score_Global = </Users/mordechaiwalder/Desktop/Research_Mordechai/Results/Fscores_Results/Ispred.Fscores.Totals.csv>;
if (my $F_Score_Data_Totals = open $F_Score_Global, :w) {
  $F_Score_Data_Totals.print("DBmark_Global_F_Score", ",", "NOX_Global_F_Score", ",", "Total_Global_F_Score", "\n");
  $F_Score_Data_Totals.print($DBmark_F_Score, ",", $NOX_F_Score, ",", $F_Score_Total);
}
