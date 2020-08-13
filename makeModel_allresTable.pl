#!/usr/bin/perl
#  my @files = <docked_model*.allres>;
my @files = <docked_model*.allres.gz>;
my ( $modelNumber, $printLine );
my @residues;
foreach my $file (@files) {
    $modelNumber = ( split( "docked_model", $file ) )[1];

    #  $modelNumber =~ s/\.allres$//; # get rid of .allres at the end
    $modelNumber =~ s/\.allres.gz$//;    # get rid of .allres.gz at the end
    $printLine = "$modelNumber:";

    #  @residues = `cat $file | awk '{print \$1"_"\$2}' | sort -u`;
    @residues = `gzip -dc $file | awk '{print \$1"_"\$2}' | sort -u`;
    foreach my $residue (@residues) {
        chomp($residue);
        $printLine .= "${residue}-";
    }                                    # end foreach $residue
    if (@residues) {
        chop($printLine);                # remove trailing "-"
    }
    print "$printLine\n";
}
