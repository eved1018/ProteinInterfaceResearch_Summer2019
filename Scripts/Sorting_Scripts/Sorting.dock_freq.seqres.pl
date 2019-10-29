#!/usr/bin/perl
#declaration of file names as variables
my $dockdir = </Users/mordechaiwalder/Desktop/Research_Mordechai/Data_Files/Dock_freq/Sorted_csv/>;
my $ispreddir = </Users/mordechaiwalder/Desktop/Research_Mordechai/Data_Files/ISPRED/ISPRED_DBMark_data_sorted/>;
#shell('rm ~/Desktop/Research_Mordechai/Data_Files/ISPRED/ISPRED_DBMark_data_sorted/.DS_Store');
for dir($ispreddir) -> $file {
  my @ispredres;
  for $file.IO.lines -> $line {
    my ($res_num, $pred) = $line.split('_');
    @ispredres.push: $res_num;
  }
  say "my ispred res = ", @ispredres;
  my $ispred_filename = split('/',$file.IO.path)[8];
  my $protein_ispred = split('_', $ispred_filename)[0];
  my $proteinid = split('.', $protein_ispred)[0];
  my $proteinchain = split('.', $protein_ispred)[1];
  my $protein = "$proteinid.$proteinchain";
  my $dock_file = "$dockdir$protein.docking_freq_sorted.csv";
  say $dock_file;
  my $dockfile = open $dock_file, :r;
  my $dockdata = $dockfile.slurp;
  my @dockres;
  for $dockdata.lines -> $prediction {
    my ($res_num, $pred) = $prediction.split(',');
    @dockres.push: $res_num;
    if (grep(/$res/, @predres)) {
    @TPres.push: $res;
    }
  }
}
