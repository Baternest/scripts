#!/usr/bin/perl -w
# Usage: cmd /c (start /b "%cd%" "C:\Program Files\Git\git-bash.exe" -i -c "perl UpdateVersion.pl your_resource_file.rc %VERSION%")

$num_args = $#ARGV + 1;
if ($num_args != 2) {
    print "\nUsage: your_resource_file.rc new_version\n";
    exit;
}

$infile = $ARGV[0];
$version = $ARGV[1];

$iVersion = $version;
$sVersion = $version;

if ($version =~ /((\d)+\,)+(\d)+/) {
    $iVersion = $version;
    $sVersion = $version =~ s/\,/\./rg;
    
    print "iVersion = ".$iVersion; 
    print "sVersion = ".$sVersion;
} elsif ($version =~ /((\d)+\.)+(\d)+/) {
    $iVersion = $version =~ s/\./\,/rg;
    $sVersion = $version;
    
    print "iVersion = ".$iVersion."\n"; 
    print "sVersion = ".$sVersion."\n";
}
else
{
    print "\nWrong new version format!\n";
    exit;    
}

$bFound = 0;
$bEnd = 0;

open(F, "+< $infile")       or die "can't read $infile: $!";
$out = '';
while (<F>) {
    if ($bFound == 0) {
        if ($_ =~ /VS_VERSION_INFO VERSIONINFO/) {
            $bFound = 1; 
        }
    }
    else 
    {
        if ($bEnd == 0) {
            if ($_ =~ /END/) {
                $bEnd = 1;
            }
            s/((\d)+\,)+(\d)+/$iVersion/eg;
            s/((\d)+\.)+(\d)+/$sVersion/eg;
            #s/(\d+),(\d+),(\d+).*\d/$version/eg;
            #s/(\d+).(\d+).(\d+).*\d/$version/eg;
        }        
    }
   #s/(\s*)FILEVERSION(\s+)(\d+),(\d+),(\d+).*/" FILEVERSION 3,3,3"/eg;
   $out .= $_;
}
seek(F, 0, 0)               or die "can't seek to start of $infile: $!";
print F $out                or die "can't print to $infile: $!";
truncate(F, tell(F))        or die "can't truncate $infile: $!";
close(F)                    or die "can't close $infile: $!";