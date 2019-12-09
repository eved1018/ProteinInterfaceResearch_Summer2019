#!/usr/bin/perl
#declaration of file names as variables
my $dockdir = </Users/mordechaiwalder/Desktop/Research_Mordechai/Data_Files/Dock_freq/Sorted_csv/>;
my $ispreddir = </Users/mordechaiwalder/Desktop/Research_Mordechai/Data_Files/ISPRED/ISPRED_NOX_data_sorted/>;
my $adjusted_dockdir = </Users/mordechaiwalder/Desktop/Research_Mordechai/Data_Files/Dock_freq/Sorted_adjusted/>;
for dir($ispreddir) -> $file {
  my $ispred_filename = split('/',$file.IO.path)[8];
  my $protein_ispred = split('_', $ispred_filename)[0];
  my $proteinid = split('.', $protein_ispred)[0];
  my $proteinchain = split('.', $protein_ispred)[1];
  my $protein = "$proteinid.$proteinchain";
  my $dock_file = "$dockdir$protein.docking_freq_sorted.csv";
  say $protein;
  my @ispredres;
  for $file.IO.lines -> $line {
    my ($res_num, $pred) = $line.split(', ');
    @ispredres.push: $res_num;
  }
  my $dockfile = open $dock_file, :r;
  my $dockdata = $dockfile.slurp;
  my $adjusted_file = "$adjusted_dockdir$protein.docking_freq_sorted.csv";
  spurt $adjusted_file, $dockdata;
  my @dockres;
  for $dockdata.lines -> $prediction {
    my ($res_num, $pred) = $prediction.split(',');
    @dockres.push: $res_num;
  }
  $dockfile.close;
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
  for ( @Missingres ) -> $res {
    if ($res > 0) {
    if (my $missing_data = open $adjusted_file, :a) {
      $missing_data.print($res, ",", "0.00", "\n")
    }
    $missing_data.close;
  }
  }
}
