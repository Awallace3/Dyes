#!/usr/bin/perl
use warnings;
use strict;

my @strs;
for (@ARGV) {
    chomp;
    push @strs, $_;
}

my @proc;
my $max = 0;
$_ = $strs[0];
while(s/(\d+)//) {
    $max = $1 > $max ? $1 : $max
}

for (@strs[1..$#strs]) {
    my $times = 0;
    s/%?(\d+)/$times++; sprintf "%s%d", $1+$max<10?"":"%", $1+$max/ge;
    $max += $times;
}
my $full = join(".", @strs);
$full =~ s/BBA/sprintf "%s%d", ($max+1)<10?"":"%", $max+1/ge;
$full =~ s/BBD/sprintf "%s%d", ($max+2)<10?"":"%", $max+2/ge;
print $full;
