#!/usr/bin/perl
#declaration of file names as variables
my $dockdir = </Users/mordechaiwalder/Desktop/Research_Mordechai/Data_Files/Dock_freq/Unsorted_csv/>;
my $ispreddir = </Users/mordechaiwalder/Desktop/Research_Mordechai/Data_Files/ISPRED/ISPRED_DBMark_data_unsorted/>;
#shell('rm ~/Desktop/Research_Mordechai/Data_Files/ISPRED/ISPRED_DBMark_data_unsorted/.DS_Store');
my $Protein_Residues = </Users/mordechaiwalder/Desktop/Research_Mordechai/Data_Files/missing_residues.csv>;
if (my $Protein_Residues_Data = open $Protein_Residues, :w) {
  $Protein_Residues_Data.print("Protein", ",", "Ispred_residues", ",", "Dock_residues", ",", "Residue_difference", ",", "Missing_residues", ",", "Protein_Status");
}
for dir($ispreddir) -> $file {
  my $ispred_filename = split('/',$file.IO.path)[8];
  my $protein_ispred = split('_', $ispred_filename)[0];
  my $proteinid = split('.', $protein_ispred)[0];
  my $proteinchain = split('.', $protein_ispred)[1];
  my $protein = "$proteinid.$proteinchain";
  my $dock_file = "$dockdir$protein.docking_freq.csv";
  say $dock_file;
  my @ispredres;
  for $file.IO.lines -> $line {
    my ($res_num, $pred) = $line.split('_');
    @ispredres.push: $res_num;
  }
  my $I = @ispredres.elems;
  say "my ispred res = ", @ispredres;
  say "my ispred res # = ", $I;
  my $dockfile = open $dock_file, :r;
  my $dockdata = $dockfile.slurp;
  my @dockres;
  for $dockdata.lines -> $prediction {
    my ($res_num, $pred) = $prediction.split(',');
    @dockres.push: $res_num;
  }
  $dockfile.close;
  my $D = @dockres.elems;
  say "my dockres # = ", $D;
  say "my dockres = ", @dockres;
  my @Missingres;
  my %lookup = map { $_ => 1 }, @dockres;
  for ( @ispredres ) -> $res {
    unless (%lookup{ $res }) {
      @Missingres.push: $res;
   }
}
   my $M = @Missingres.elems;
   say "my missing res # = ", $M;
   say "my missing res = ", @Missingres;
   my $res_diff = $I - $D;
   say "my res diff = ", $res_diff;
   my $delta = $M - $res_diff;
   say "my delta = ", $delta;
   if (my $Protein_Residues_Data = open $Protein_Residues, :a) {
     $Protein_Residues_Data.print("\n", $protein, ",", $I, ",", $D, ",", $res_diff, ",", $M, ",");
   }
     if ($delta == 1) {
        if (my $Protein_Residues_Data = open $Protein_Residues, :a) {
       $Protein_Residues_Data.print("Extra Terminus Residue");
     }
   }
     if ($res_diff < 0) {
         if (my $Protein_Residues_Data = open $Protein_Residues, :a) {
       $Protein_Residues_Data.print("Extra Docking Chain");
     }
    }
}
