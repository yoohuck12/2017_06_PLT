#!/usr/bin/perl
# ------------------------------------------------------
# This script analyzes .log files into .json files.
# See config to change directory paths.
# ------------------------------------------------------

#use ProcessAdapter;
use JSON;
use lib 'tests_analysis_t/';
use ProcessMain;

$num_experiments = 5;

##########################################
# Check arguments
##########################################
$argc = @ARGV;
#print "argc = ", $argc , "\n"; #1

if ($argc < 0) {
  print "Usage: " . $0 . " [min | max | median | 0.1 | 0.9]\n";
  exit 0;
}
$type = $ARGV[0];
#print "type = ", $ARGV[0], "\n"; # min | max ...
#print "type = ", $type, "\n";

$adapter = new ProcessMain($type);
print "[YOO] after initialization\n";
#$adapter->run();
