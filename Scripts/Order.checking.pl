#!/usr/bin/perl
my $PredUsdir = </Users/mordechaiwalder/Desktop/ProteinInterfaceResearch_Summer2019-E_Edelstein/PDB_Files/Predus_241_for_real/>;
for dir($PredUsdir) -> $file {
    my $Dbmark_filename = split('/', $file.IO.path)[7];
    my $Dbmark_protein = split('_', $Dbmark_filename)[1];
#    say $Dbmark_protein;
    my $predfile = open $file, :r;
    my $preddata = $predfile.slurp;
    for $preddata.lines(1) -> $prediction {
      if ($prediction.contains('501')) {
          say $Dbmark_protein;
      }
  #    my $res = split(' ', $prediction)[5];
  #    say $res;
    }
    $predfile.close;
  }
