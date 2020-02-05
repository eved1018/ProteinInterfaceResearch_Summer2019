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
