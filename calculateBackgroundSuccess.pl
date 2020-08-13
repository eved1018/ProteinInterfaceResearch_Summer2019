#!/usr/bin/perl

($#ARGV > 0) or die "usage: $0<total residues (sampled)><annotated interface residues (sampled)>><optional: number of draws (default=200)><optional: size of drawn set (default:15)>";

use strict;

my ($all, $interface, $numberOfDraws, $draw) = @ARGV;
if(!defined $numberOfDraws){ $numberOfDraws = 200; }
if(!defined $draw){ $draw = 15; }

my @residues;
for(my $i = 0; $i < $all; $i++){
  $residues[$i] = $i+1;
}

my @residuesCopy = @residues;
my @selection;
my ($interfaceSelected, $sumx, $sumx2, $n, $mean, $sd, $var);
#print "$interfaceSelected\n";

for(my $i = 0; $i < $numberOfDraws; $i++){
  @residuesCopy = @residues;
  @selection = makeRandomDraw(\@residuesCopy, $draw);
  $interfaceSelected = evaluateSelection(\@selection, $interface);
  $sumx += $interfaceSelected;
  $sumx2 += ($interfaceSelected**2);
  $n++;
}

$mean = $sumx/$n;
$var = (($n*$sumx2) - ($sumx**2)) / ($n*($n-1));
$sd = sqrt($var);
printf "%.2f\t%.2f\n", $mean,$sd;


sub makeRandomDraw{
  my ($array, $drawSize) = @_;
  my $arraySize = @$array;
  my @result;
  my ($currentDraw);
  for(my $i = 0; $i < $drawSize; $i++){
    $currentDraw = int(rand($arraySize));
    push(@result, $array->[$currentDraw]);
    swap(\$array->[$arraySize-1], \$array->[$currentDraw]);
    $arraySize--;
  }
  return @result;
}

sub swap{
  my ($one, $two) = @_;
  my $temp = $$one;
  $$one = $$two;
  $$two = $temp;
}

sub evaluateSelection{
  my ($array, $interf) = @_;
  my $result = 0;
  for(my $i = 0; $i <@{$array}; $i++){
    if($array->[$i] <= $interf){
      $result++;
    }
  }
  return $result;
}

