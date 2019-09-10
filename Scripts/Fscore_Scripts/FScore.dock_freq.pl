#!/usr/bin/perl
#declaration of file names as elements in an array
my $preddir = </Users/mordechaiwalder/Desktop/Research_Mordechai/Data_Files/Dock_freq/Sorted/>;
my $Dbmark_annotateddir = </Users/mordechaiwalder/Desktop/Research_Mordechai/Annotated_Residues/Dbmark_Annotated_Residues>;
my $NOX_annotateddir = </Users/mordechaiwalder/Desktop/Research_Mordechai/Annotated_Residues/NOX_Annotated_Residues>;
my $F_Score_Dir = </Users/mordechaiwalder/Desktop/Research_Mordechai/Results/Fscores_Results>;
#creating data table file
my $F_Score_File = <Dock_freq.Fscores.txt>;
for dir($F_Score_Dir) {
  spurt "$F_Score_File", "DB-protein TP N F-Score\n";
}
#closedir <~/Desktop/Research_Mordechai/Results/Fscores_Results>;
#looping through annotated residue files
for dir($Dbmark_annotateddir) -> $file {
    say $file;
    my @annotatedres;
    my $Dbmark_filename = split('/', $file.IO.path)[7];
    say $Dbmark_filename;
    my $Dbmark_protein = split('_', $Dbmark_filename)[0];
    say $Dbmark_protein;
    my $Dbmark_protein_dock = "$preddir$Dbmark_protein.docking_freq_sorted";
    say $Dbmark_protein_dock;
    for $file.IO.lines -> $line {
      my ($annres_num, $annres) = $line.split('_');
      @annotatedres.push: $annres_num;
    }
    my $N = @annotatedres.elems;
    say @annotatedres;
    say $N;
    my @predres;
    my $predfile = open $Dbmark_protein_dock, :r;
    my $preddata = $predfile.slurp;
    for $preddata.lines($N) -> $prediction {
      my ($predres_num, $predres) = $prediction.split(' ');
      @predres.push: $predres_num;
    }
    $predfile.close;
    say @predres;
    my @TPres;
    for (@predres) -> $res {
      if (grep(/$res/, @annotatedres)) {
      @TPres.push: $res;
      }
    }
    say @TPres;
    my $TP = @TPres.elems;
    my $F_Score = ($TP/$N);
    say $F_Score;
    for dir($F_Score_Dir) {
      spurt "$F_Score_File", "$Dbmark_protein $TP $N $F_Score\n";
    }
    #closedir <~/Desktop/Research_Mordechai/Results/Fscores_Results>;
    #open $Dbmark_protein_dock, :r;
    #while (<$Dbmark_protein_dock.lines($N>)) -> $line {
    #  say $line;
    #}
  #  my $predfile = open $Dbmark_protein_dock, :r;
  #  my $preddata = $predfile.lines($N).slurp;
  #  say $preddata;
  #  $predfile.close;
}
