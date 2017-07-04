#!/usr/bin/perl

use Switch;
use JSON;
use Try::Tiny;


##########################################
# Check arguments
##########################################
$argc = @ARGV;

if ($argc < 1) {
  print "Usage: " . $0 . " [path]\n";
  exit 0;
}

$path = $ARGV[0];
$suffix = "_pro";
$path_pro = $path . $suffix;

print `mkdir $path_pro`;

$ls = `ls $path`;
@hars = split(/\n/, $ls);#array of files in  dir

foreach $har (@hars) {
  my $file = "$path/$har";
  print $file . "\n";
  open(FP, $file) || die("Couldn't open file!\n");

  # find timestamp
  @tmp = split(/\./, $har);#retreives timestamp from current files name
  @tmp = split(/\_/, $tmp[0]);
  $ts = $tmp[1];

  my $line;
  my $buf = "";
  my $page = "_";
  my %pages = ();

  my %jsAndCssTimes = ();

  while ($line = <FP>) {
	if(index($line, '{"') != -1) {
		$line = substr($line, index($line, '{"'));
	} else {
		next;
	}


    #$line = substr($line, 19, length($line) - 1);#Specific to Android logs. Removes "V/WProf.db"-Tyler
    @a = split(/\n/, $line);
    $line = $a[0];

    $line =~ s/'//g;
    $line =~ s/\?//g;
    if ($line =~ m/: "([^",]*("|')[^",]*)+"/) {
	@strings = split(", ", $line);
	for ($i = 0; $i < @strings; $i++) {
	    $string = @strings[$i];
	    if ($string =~ m/: "([^",]*("|')[^",]*)+"/) {
		@tmp = split(': ', $string);
		@tmp[1] =~ s/"//g;
		@tmp[1] = "\"" . @tmp[1] . "\"";
		$string = join(': ', @tmp);
		@strings[$i] = $string;
	    }
	}
	$line = join(", ", @strings);
    }

    $line =~ s/WprofHTMLTag/ObjectHash/g;

my $attempt = 1;
while(true) {
	try {
	    %h = %{decode_json($line)};
	    last;
	} catch {
	    $attempt++;
	    if(index($line, '{"', $attempt) != -1) {
		$line = substr($line, index($line, '{"', $attempt));
	    } elsif(index($line, '{', $attempt) != -1) {
		$line =~ s/{[^"]/{"p/g; #Make 'p' variable
		print $line . "\n";
	    } elsif(substr($line, length($line) - 3, 2) eq '}}') {
		$line = "{\"HOL\":" . $line; #Make HOL variable
	    } else {
	    	print "attempt $attempt with line: \"$line\" failed!\n";
		die;
	    }
	};
}




    #checks for and stores javascript and CSS objects
    #so that they aren't recorded and the times
    #are used in the corresponding resource objects
    if($h{"Javascript"}) {
	#store javascript or info
	my $key = $h{"Javascript"}{"url"};
	my $value = $h{"Javascript"}{"requestTime"};
	$jsAndCssTimes{$key} = $value;
    } elsif($h{"CSS"}) {
	#store css info
	my $key = $h{"CSS"}{"url"};
	my $value = $h{"CSS"}{"requestTime"};
	$jsAndCssTimes{$key} = $value;
    } else {
	if($h{"Resource"}) {
	    #check for javascript or CSS info and replace time if found
	    my $resUrl = $h{"Resource"}{"url"};

	    if(defined $jsAndCssTimes{$resUrl}) {
		my $newRequestTime = $jsAndCssTimes{$resUrl};
		$h{"Resource"}{"requestTime"} = $newRequestTime;
	    }
	    $line = encode_json \%h;
	}

	$buf .= $line . "\n";
    }






    if ($h{"page"}) {
      $page = $h{"page"};
    } elsif ($h{"Complete"}) {
      #print $h{"Complete"} . "\n";

      if ($pages{$page}) {
        $pages{$page} += 1;
      } else {
        $pages{$page} = 1;
      }

      $time = $pages{$page};
      # write to file
      $f = "$path_pro/$page^$ts^$time";
      open(FH, ">$f");
      print FH $buf;
      close FH;

      # clear buffer
      $buf = "";

      #clears javascript and CSS info since this
      #page is done
      %jsAndCssTimes = ();
    }
  }
  # write to file
  #$f = "$path_pro/$page";
  #open(FH, ">$f");
  #print FH $buf;
  #close FH;

  close FP;
}
