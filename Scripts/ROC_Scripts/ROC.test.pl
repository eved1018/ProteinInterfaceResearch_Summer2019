#!/usr/bin/perl
#declaration of file names as variables
my $preddir = </Users/mordechaiwalder/Desktop/Research_Mordechai/Data_Files/Dock_freq/Sorted_csv/>;
my $Dbmark_annotateddir = </Users/mordechaiwalder/Desktop/Research_Mordechai/Annotated_Residues/Dbmark_Annotated_Residues>;
my $NOX_annotateddir = </Users/mordechaiwalder/Desktop/Research_Mordechai/Annotated_Residues/NOX_Annotated_Residues>;
shell('rm ~/Desktop/Research_Mordechai/Annotated_Residues/Dbmark_Annotated_Residues/.DS_Store');
#creating file w/ data table of gloabal TPR/FPR values at each threshold
for dir($Dbmark_annotateddir) -> $file {
    my @annotatedres;
    my $Dbmark_filename = split('/', $file.IO.path)[7];
    my $Dbmark_protein = split('_', $Dbmark_filename)[0];
    say $Dbmark_protein;
   my $Dbmark_protein_dock = "$preddir$Dbmark_protein.docking_freq_sorted.csv";
    for $file.IO.lines -> $line {
      my ($annres_num, $annres) = $line.split('_');
      @annotatedres.push: $annres_num;
    }
    my $N = @annotatedres.elems;
    say @annotatedres;
    say $N;
    my @predres;
    my @seqres;
    my $predfile = open $Dbmark_protein_dock, :r;
    my $preddata = $predfile.slurp;
    for $preddata.lines -> $prediction {
      say "My prediction is ", $prediction;
      my ($predres_num, $predval) = $prediction.split(',');
      @seqres.push: $predres_num;
      say "My predres_num = ", $predres_num;
      say "My predval = ", $predval;
      if ($predval >= 0) {
        @predres.push: $predres_num;
     }
    }
    $predfile.close;
    say "My seqres = ", @seqres;
    say "My predres = ", @predres;
    my @TPres;
   for (@annotatedres) -> $res {
      if (grep(/$res/, @predres)) {
      @TPres.push: $res;
      }
    }
    say "My tpres = ", @TPres;
    my $pred = @predres.elems;
    my $TP = @TPres.elems;
    my $Seqres = @seqres.elems;
    say "my pred num = ", $pred;
    say "my seq num = ", $Seqres;
    my $TPR = $TP/$N;
    my $FP = $pred - $TP;
    my $neg = $Seqres - $N;
    my $FPR = $FP/$neg;
}
