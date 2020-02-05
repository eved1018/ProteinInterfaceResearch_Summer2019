#!/usr/bin/perl
my $RSAdir = </Users/mordechaiwalder/Desktop/Research_Mordechai/Data_Files/ISPRED/ISPRED_DBMark_data_RSA/>;
#shell('rm ~/Desktop/Research_Mordechai/Data_Files/ISPRED/ISPRED_NOX_data_RSA/.DS_Store');
my $surface_file = </Users/mordechaiwalder/Desktop/Research_Mordechai/Data_Files/ISPRED/DBMark_surfaceres.csv>;
if (my $surface_data = open $surface_file, :w) {
  $surface_data.print("Protein", ",", "surface_res", ",", "cutoff_res", "\n");
}
for dir($RSAdir) -> $file {
  my $RSA_filename = split('/',$file.IO.path)[8];
  my $protein = split('_', $RSA_filename)[0];
  say $protein;
  my @surfaceres;
  my $RSAdata = $file.slurp;
  for $RSAdata.lines -> $line {
    my ($res_num, $RSA) = $line.split(', ');
    if ($RSA >= 0.05) {
      @surfaceres.push: $res_num;
    }
  }
  say @surfaceres;
  my $s = @surfaceres.elems;
  my $c = 6.1 * ($s**0.3);
  my $rc = round($c);
  if (my $surface_data = open $surface_file, :a) {
    $surface_data.print($protein, ",", $s, ",", $rc, "\n");
  }
}
