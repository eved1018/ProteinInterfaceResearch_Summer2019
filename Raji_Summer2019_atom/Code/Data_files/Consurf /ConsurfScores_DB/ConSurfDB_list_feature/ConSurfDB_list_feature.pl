#!/usr/bin/perl -w   
##############################################################################
# ConSurfDB_list_final.pl
#
# 
# Steps: 
#   - Read the list input file and covert to uppercase.
#   - Split and seperate the chains from the PDB id's. 
#   - Look for the representative pdb ib and chain for each entry
#	- Retrieve each chain from the ConSurfDB website 
#
# Notes:
#   - the program take a single command line paramter, all other parameters
#   - the working directory for the script is the directory of the given input
#     file. all files are created there.
#   - a log file ConSurfDB_list.log is created in the working directory
#   - a corrected list file - Corrected_list.dat (with representative chains) is created in the working directory
#
# Usage:
#   ConSurfDB_list_final.pl input_file
#       input_file - List of PDB id's and chains for example - 2DU3 A,B,C,D
#
#   Changelog:
#       2013-Mar-22, Ofir Goldenberg - Created
##############################################################################

use LWP::Simple;
no warnings ;

$user_list_file = $ARGV[0];

open IN, "$user_list_file" or die $!;
open LOG, ">ConSurfDB_list.log" or die $!;
open Crlist, ">Corrected_list.dat" or die $!;



$i=0;

while (<IN>) 
{
	chomp;
	$string=$_; 
	$string =~ tr/a-z/A-Z/;
	@text= split(/\ /,$string);
	
	#print $string ."\n";
	#print  $text[0].$text[1]."\n";

	@chains_text= split(/,/,$text[1]);

	foreach $cell (@chains_text)
		{
			@chains[$i]= $cell;			
			@pdb_id[$i]= $text[0];
			$i++;
		}

}


$arraySize = @pdb_id;

#$cmd="mkdir ConSurfDB_list_grades_output_files";
#`$cmd`;


for  ($k=0;$k<$arraySize;$k++)
	{
		print     $k.". ".$pdb_id[$k]."/".$chains[$k]." -> ";
		print     Crlist $k.". ".$pdb_id[$k]."/".$chains[$k]." -> ";
		$search_id=&look_for_NR($pdb_id[$k],$chains[$k]);
		print  $search_id."\n";
		print  Crlist $search_id."\n";
		retrieve_grades_from_web($search_id,$pdb_id[$k]."_".$chains[$k]."_ConSurfDB_grades");
		print $pdb_id[$k]."_".$chains[$k]."_ConSurfDB_grades\n";
		#print "$cell $chains[$g]: ".$search_id ."\n";
		
	}	



#print look_for_NR("2VG5","A")."\n";
#http://bental.tau.ac.il/new_ConSurfDB/DB/3LZG/A/consurf.grades

#print_input(pdb_id, chain)
sub print_input($$)
{
	my $pdb_id=$_[0];
	my $chain=$_[1];

	print $pdb_id." ".$chain."\n";

}

#look_for_NR(pdb_id, chain)
sub look_for_NR($$)
{
	my $pdb_id=$_[0];
	my $chain=$_[1];
	my $combined=$pdb_id."_".$chain;
	#print "input $combined\n";
	open IN_LIST, "pdbaa_list.nr" or die $!;
	 
	while (<IN_LIST>)
	{
		chomp;

		 if ($_ =~m/$combined/) 
		 {
	#	 		print " Got you:".$combined."\n";

	  			@pdb_nr_str = split(/:/,$_);
				$first_pdb=$pdb_nr_str[0];
				$rest_pdbs=$pdb_nr_str[1];
		
				@pdb_first_str = split(/_/,$first_pdb);
				$pdb_id_first=$pdb_first_str[0];
				$chain_first=$pdb_first_str[1];
				$output = $pdb_id_first."/".$chain_first;
	#			print "Output: ".$output."\n";
		 } 
	        
	}
	close (IN_LIST);
 return $output;

}


sub retrieve_grades_from_web($$) 
{
	my $pdb_with_chain=$_[0];
	my $OutputName=$_[1];
	open OUT, ">".$OutputName."_ConSurfDB_grades";
    my $content = get('http://bental.tau.ac.il/new_ConSurfDB/DB/'.$pdb_with_chain.'/consurf.grades') or print LOG $OutputName." -> Unable to find the grades page on ConSurfDB site\n";
    print OUT $content;
    close(OUT);

}
