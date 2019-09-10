#!/usr/bin/perl
#shell ('cd /Users/mordechaiwalder/Desktop/Research_Mordechai/Data_Files/Dock_freq');
#my $predfiles = Q:x{cd ../../Data_Files/Dock_freq | ls -d $PWD/*};
#print "$predfiles";
for dir(</Users/mordechaiwalder/Desktop/Research_Mordechai/Data_Files/Dock_freq>) -> $file {
    say $file;
}
