#!/usr/bin/perl
#declaration of file names as variables
#shell('rm ~/Desktop/Research_Mordechai/Annotated_Residues/Dbmark_Annotated_Residues/.DS_Store');
my $Dbmark_preddir = </Users/mordechaiwalder/Desktop/Research_Mordechai/Data_Files/ISPRED/ISPRED_DBMark_data_sorted/>;
my $NOX_preddir = </Users/mordechaiwalder/Desktop/Research_Mordechai/Data_Files/ISPRED/ISPRED_NOX_data_sorted/>;
my $dockdir = </Users/mordechaiwalder/Desktop/Research_Mordechai/Data_Files/Dock_freq/Sorted_adjusted/>;
my $sequence_check_file = </Users/mordechaiwalder/Desktop/Research_Mordechai/Results/ispred_dock_sequence_check.csv>;
if (my $sequence_data = open $sequence_check_file, :w) {
  $sequence_data.print("Protein", ",", "dock_not_ispred", ",", "ispred_not_dock", ",", "ispred_res", ",", "dock_res", ",", "delta_ispred_dock", "\n");
}
for dir($Dbmark_preddir) -> $file {
  my $Dbmark_filename = split('/', $file.IO.path)[8];
  my $Dbmark = split('_', $Dbmark_filename)[0];
  my $Dbmark_protein = split('.', $Dbmark)[0];
  my $Dbmark_chain = split('.', $Dbmark)[1];
  my $Dbmark_pdb = "$Dbmark_protein.$Dbmark_chain";
  say $Dbmark_pdb;
  my @ispredseq;
  my $ispredfile = open $file, :r;
  my $ispreddata = $ispredfile.slurp;
  for $ispreddata.lines -> $prediction {
    my ($predres_num, $predval) = split ', ', $prediction;
    @ispredseq.push: $predres_num;
}
  $ispredfile.close;
  my @dockseq;
  my $dock = "$dockdir$Dbmark_pdb.docking_freq_sorted.csv";
  my $dockfile = open $dock, :r;
  my $dockdata = $dockfile.slurp;
  for $dockdata.lines -> $prediction {
    my ($predres_num, $predval) = split ',', $prediction;
    @dockseq.push: $predres_num;
}
  $dockfile.close;
  my @docknotispred;
  my @isprednotdock;
  my %ispredlookup = map { $_ => 1 }, @ispredseq;
  for (@dockseq) -> $res {
     unless (%ispredlookup{ $res }) {
     @docknotispred.push: $res;
     }
   }
   my %docklookup = map { $_ => 1 }, @dockseq;
   for (@ispredseq) -> $res {
      unless (%docklookup{ $res }) {
      @isprednotdock.push: $res;
      }
    }
    my $y = @ispredseq.elems;
    my $z = @dockseq.elems;
    my $deltaispreddock = $y - $z;
    if (my $sequence_data = open $sequence_check_file, :a) {
      $sequence_data.print($Dbmark_pdb, ",", @docknotispred, ",", @isprednotdock, ",", $y, ",", $z, ",", $deltaispreddock, "\n");
    }
}
for dir($NOX_preddir) -> $file {
  my $NOX_filename = split('/', $file.IO.path)[8];
  my $NOX = split('_', $NOX_filename)[0];
  my $NOX_protein = split('.', $NOX)[0];
  my $NOX_chain = split('.', $NOX)[1];
  my $NOX_pdb = "$NOX_protein.$NOX_chain";
  say $NOX_pdb;
  my @ispredseq;
  my $ispredfile = open $file, :r;
  my $ispreddata = $ispredfile.slurp;
  for $ispreddata.lines -> $prediction {
    my ($predres_num, $predval) = split ', ', $prediction;
    @ispredseq.push: $predres_num;
}
  $ispredfile.close;
  my @dockseq;
  my $dock = "$dockdir$NOX_pdb.docking_freq_sorted.csv";
  my $dockfile = open $dock, :r;
  my $dockdata = $dockfile.slurp;
  for $dockdata.lines -> $prediction {
    my ($predres_num, $predval) = split ',', $prediction;
    @dockseq.push: $predres_num;
}
  $dockfile.close;
  my @docknotispred;
  my @isprednotdock;
  my %ispredlookup = map { $_ => 1 }, @ispredseq;
  for (@dockseq) -> $res {
     unless (%ispredlookup{ $res }) {
     @docknotispred.push: $res;
     }
   }
   my %docklookup = map { $_ => 1 }, @dockseq;
   for (@ispredseq) -> $res {
      unless (%docklookup{ $res }) {
      @isprednotdock.push: $res;
      }
    }
    my $y = @ispredseq.elems;
    my $z = @dockseq.elems;
    my $deltaispreddock = $y - $z;
    if (my $sequence_data = open $sequence_check_file, :a) {
      $sequence_data.print($NOX_pdb, ",", @docknotispred, ",", @isprednotdock, ",", $y, ",", $z, ",", $deltaispreddock, "\n");
    }
}
